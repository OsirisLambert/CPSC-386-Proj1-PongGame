import pygame, time, sys, math, random
from pygame.locals import *
from random import randint
from typing import Any

pygame.init()

WINDOWWIDTH,WINDOWHEIGHT  = 1024, 600

# Clock
clock = pygame.time.Clock()
FPS = 60

player_win = False
ai_win = False
is_play_again = True

# Color
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
LIGHTGREEN = (124,252,0)
TEXTCOLOR = WHITE

ball_moveSpeed = 5
paddle_moveSpeed = 15
ai_moveSpeed = 0


# Paddle Setting
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
NO_MOVEMENT = True


# Ball Setting
angle_q1 = random.randint(30, 60)
angle_q2 = random.randint(120, 150)
angle_q3 = random.randint(210, 240)
angle_q4 = random.randint(300,330)
angle_list = [angle_q1,angle_q2,angle_q3,angle_q4]

# Set up sounds.
hitSound = pygame.mixer.Sound('sounds/hit.wav')
lose = pygame.mixer.Sound('sounds/lose.wav')
win = pygame.mixer.Sound('sounds/win.wav')
pygame.mixer.music.load('sounds/bgm.wav')
resultSound = True


# Set up the fonts.
font = pygame.font.SysFont(None, 48)
score_font = pygame.font.SysFont(None, 30)

backgroundImage = pygame.image.load('images/bg.png')
backgroundImage = pygame.transform.scale(backgroundImage, (1024, 600))

paddle_image_A = pygame.image.load('images/paddle_verti.png')
paddle_image_A = pygame.transform.scale(paddle_image_A, (20, 80))

paddle_image_B = pygame.image.load('images/paddle_horizon.png')
paddle_image_B = pygame.transform.scale(paddle_image_B, (100, 20))

ball_image = pygame.image.load('images/ball.png')
ball_image = pygame.transform.scale(ball_image, (30, 30))

# Set up pygame, the window, and the mouse cursor.
pygame.display.set_caption('PONG w/o walls')
pygame.mouse.set_visible(False)
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
surface_rect = windowSurface.get_rect()
half_center = windowSurface.get_rect().centerx / 2 # half of the center

class Paddle(pygame.sprite.Sprite):
    def __init__(self, position):
        # Creating the paddle
        pygame.sprite.Sprite.__init__(self)
        self.paddle = position
        self.speed = paddle_moveSpeed

        # Establishing the location of each paddle

        if self.paddle == 'player_left':    # real player left paddle
            self.image = paddle_image_A
            self.rect = self.image.get_rect()
            self.rect.left = windowSurface.get_rect().left
            self.rect.y = windowSurface.get_rect().centerx
        elif self.paddle == 'player_top':  # real player top paddle
            self.image = paddle_image_B
            self.rect = self.image.get_rect()
            self.rect.top = windowSurface.get_rect().top
            self.rect.x = windowSurface.get_rect().centerx / 2
        elif self.paddle == 'player_bot':  # real player bot paddle
            self.image = paddle_image_B
            self.rect = self.image.get_rect()
            self.rect.x = windowSurface.get_rect().centerx / 2
            self.rect.bottom = windowSurface.get_rect().bottom
        elif self.paddle == 'ai_right':  # computer player right paddle
            self.image = paddle_image_A
            self.rect = self.image.get_rect()
            self.rect.right = windowSurface.get_rect().right
            self.rect.y = windowSurface.get_rect().centerx
        elif self.paddle == 'ai_top':  # computer player top paddle
            self.image = paddle_image_B
            self.rect = self.image.get_rect()
            self.rect.top = windowSurface.get_rect().top
            self.rect.x = windowSurface.get_rect().centerx + half_center
        elif self.paddle == 'ai_bot':  # computer player bot paddle
            self.image = paddle_image_B
            self.rect = self.image.get_rect()
            self.rect.x = windowSurface.get_rect().centerx + half_center
            self.rect.bottom = windowSurface.get_rect().bottom

    def move(self):
        if self.paddle == 'player_left':
            if moveUp:
                self.rect.y -= self.speed
            elif moveDown:
                self.rect.y += self.speed
            elif NO_MOVEMENT:
                pass
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= WINDOWHEIGHT:
                self.rect.bottom = WINDOWHEIGHT
        elif self.paddle == 'player_top' or self.paddle == 'player_bot':
            if moveLeft:
                self.rect.x -= self.speed
            elif moveRight:
                self.rect.x += self.speed
            elif NO_MOVEMENT:
                pass
            if self.rect.left <= 0:
                self.rect.left = 0
            if self.rect.right >= surface_rect.centerx:
                self.rect.right = surface_rect.centerx

class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ball_image
        self.rect = self.image.get_rect()
        self.rect.centerx = surface_rect.centerx
        self.rect.centery = surface_rect.centery
        self.angle = random.choice(angle_list) * math.pi / 180
        self.speed_x = ball_moveSpeed
        self.speed_y = ball_moveSpeed

    def move(self):
        self.rect.x += (self.speed_x * math.cos(self.angle))
        self.rect.y += (self.speed_y * math.sin(self.angle))

    def reset(self):
        self.angle = random.choice(angle_list)
        self.speed_x = ball_moveSpeed
        self.speed_y = ball_moveSpeed
        self.rect.x = surface_rect.centerx - 15
        self.rect.y = surface_rect.centery - 15


player_paddle_left = Paddle('player_left')
player_paddle_top = Paddle('player_top')
player_paddle_bot = Paddle('player_bot')
player_paddle = [player_paddle_left, player_paddle_top, player_paddle_bot]
ai_paddle_right = Paddle('ai_right')
ai_paddle_top = Paddle('ai_top')
ai_paddle_bot = Paddle('ai_bot')
ai_paddle = [ai_paddle_right, ai_paddle_top, ai_paddle_bot]

ball = Ball()

all_sprites = pygame.sprite.RenderPlain(player_paddle, ai_paddle, ball)


def has_hit_ball():
    if pygame.sprite.collide_rect(ball, ai_paddle[0]):
        if ball.rect.right > ai_paddle[0].rect.left:
            ball.rect.right = ai_paddle[0].rect.left
        ball.speed_x = ball.speed_x + 0.1
        ball.speed_x = -ball.speed_x
        if ball.speed_y > 0:
            ball.speed_y = ball.speed_y + 0.1
        else:
            ball.speed_y = ball.speed_y - 0.1
        hitSound.play()

    elif pygame.sprite.collide_rect(ball, ai_paddle[1]):
        if ball.rect.top < ai_paddle[1].rect.bottom:
            ball.rect.top = ai_paddle[1].rect.bottom
        if ball.speed_x > 0:
            ball.speed_x = ball.speed_x + 0.1
        else:
            ball.speed_x = ball.speed_x - 0.1
        ball.speed_y = ball.speed_y - 0.1
        ball.speed_y = -ball.speed_y
        hitSound.play()

    elif pygame.sprite.collide_rect(ball, ai_paddle[2]):
        if ball.rect.bottom > ai_paddle[2].rect.top:
            ball.rect.bottom = ai_paddle[2].rect.top
        if ball.speed_x > 0:
            ball.speed_x = ball.speed_x + 0.1
        else:
            ball.speed_x = ball.speed_x - 0.1
        ball.speed_y = ball.speed_y + 0.1
        ball.speed_y = -ball.speed_y
        hitSound.play()

    elif pygame.sprite.collide_rect(ball, player_paddle[0]):
        if ball.rect.left < player_paddle[0].rect.right:
            ball.rect.left = player_paddle[0].rect.right
        ball.speed_x = ball.speed_x - 0.1
        ball.speed_x = -ball.speed_x
        if ball.speed_y > 0:
            ball.speed_y = ball.speed_y + 0.1
        else:
            ball.speed_y = ball.speed_y - 0.1
        hitSound.play()

    elif pygame.sprite.collide_rect(ball, player_paddle[1]):
        if ball.rect.top < player_paddle[1].rect.bottom:
            ball.rect.top = player_paddle[1].rect.bottom
        if ball.speed_x > 0:
            ball.speed_x = ball.speed_x + 0.1
        else:
            ball.speed_x = ball.speed_x - 0.1
        ball.speed_y = ball.speed_y - 0.1
        ball.speed_y = -ball.speed_y
        hitSound.play()

    elif pygame.sprite.collide_rect(ball, player_paddle[2]):
        if ball.rect.bottom > player_paddle[2].rect.top:
            ball.rect.bottom = player_paddle[2].rect.top
        if ball.speed_x > 0:
            ball.speed_x = ball.speed_x + 0.1
        else:
            ball.speed_x = ball.speed_x - 0.1
        ball.speed_y = ball.speed_y + 0.1
        ball.speed_y = -ball.speed_y
        hitSound.play()

def ai_move(ai_paddle, ball):
    if ball.rect.x >= surface_rect.centerx:
        # ai right paddle move
        if not ai_paddle[0].rect.y + 40 == ball.rect.y:
            if ai_paddle[0].rect.y + 40 < ball.rect.y:
                ai_paddle[0].rect.y += ai_moveSpeed
            if ai_paddle[0].rect.y + 40 > ball.rect.y:
                ai_paddle[0].rect.y -= ai_moveSpeed

        if ai_paddle[0].rect.top <= 0:
            ai_paddle[0].rect.y = 0
        if ai_paddle[0].rect.bottom >= WINDOWHEIGHT:
            ai_paddle[0].rect.y = WINDOWHEIGHT - 80
        #ai top paddle move
        if not ai_paddle[1].rect.x + 50 == ball.rect.x:
            if ai_paddle[1].rect.x+50 < ball.rect.x:
                ai_paddle[1].rect.x += ai_moveSpeed
            if ai_paddle[1].rect.x+50 > ball.rect.x:
                ai_paddle[1].rect.x -= ai_moveSpeed

        if ai_paddle[0].rect.top <= 0:
            ai_paddle[0].rect.y = 0
        if ai_paddle[0].rect.bottom >= WINDOWHEIGHT:
            ai_paddle[0].rect.y = WINDOWHEIGHT - 80
        if ai_paddle[1].rect.left <= surface_rect.centerx:
            ai_paddle[1].rect.left = surface_rect.centerx
        # ai bot paddle move
        ai_paddle[2].rect.x = ai_paddle[1].rect.x

def terminate():
    pygame.quit()
    sys.exit()

def level_choose():
    pygame.mixer.music.play(-1)
    ready_to_play = False
    while not ready_to_play:
        pygame.mouse.set_visible(1)
        windowSurface.fill(BLACK)

        # set text
        title = font.render("PONG GAME", True, WHITE, BLACK)
        easy_level = font.render("Easy Level", True, WHITE, BLACK)
        hard_level = font.render("Hard Level", True, WHITE, BLACK)

        title_rect = title.get_rect()
        title_rect.centerx = surface_rect.centerx
        title_rect.centery = 100

        easy_level_rect = easy_level.get_rect()
        easy_level_rect.centerx = surface_rect.centerx
        easy_level_rect.centery = 250

        hard_level_rect = hard_level.get_rect()
        hard_level_rect.centerx = surface_rect.centerx
        hard_level_rect.centery = 400

        windowSurface.blit(title, title_rect)
        windowSurface.blit(easy_level, easy_level_rect)
        windowSurface.blit(hard_level, hard_level_rect)
        pygame.display.update()
        ball.speed_x += 0.01
        ball.speed_y += 0.01

        while not ready_to_play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if easy_level_rect.collidepoint(mouse_pos):
                        speed = 3
                        ready_to_play = True
                        break
                    elif hard_level_rect.collidepoint(mouse_pos):
                        speed = 15
                        ready_to_play = True
                        break
    return speed

while is_play_again:
    is_play_again = False
    ai_moveSpeed = level_choose()

    game_is_on = True
    player_score = 0
    ai_score = 0
    player_win_round = 0
    ai_win_round = 0
    current_round = 0

    while game_is_on:
        clock.tick(FPS)
        pygame.mouse.set_visible(0)
        if ball.rect.x > WINDOWWIDTH:
            ball.rect.centerx = surface_rect.centerx
            ball.rect.centery = surface_rect.centery
            ball.direction = randint(0, 1)
            ball.speed = ball_moveSpeed
        elif ball.rect.x < 0:
            ball.rect.centerx = surface_rect.centerx
            ball.rect.centery = surface_rect.centery
            ball.direction = randint(2, 3)
            ball.speed = ball_moveSpeed

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                # Change the keyboard variables.

                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

        score_board_player = score_font.render(
            ("Win Round: " + str(player_win_round) + "   Current Score: " + str(player_score)), True, WHITE,
            backgroundImage)
        score_board_player_rect = score_board_player.get_rect()
        score_board_player_rect.centerx = half_center
        score_board_player_rect.y = 30

        score_board_ai = score_font.render(("Win Round: " + str(ai_win_round) + "   Current Score: " + str(ai_score)),
                                           True, WHITE, backgroundImage)
        score_board_ai_rect = score_board_player.get_rect()
        score_board_ai_rect.centerx = half_center + surface_rect.centerx
        score_board_ai_rect.y = 30

        windowSurface.blit(backgroundImage, (0, 0))
        pygame.draw.line(windowSurface, WHITE, (surface_rect.centerx, 0), (surface_rect.centerx, WINDOWHEIGHT,))
        windowSurface.blit(score_board_player, score_board_player_rect)
        windowSurface.blit(score_board_ai, score_board_ai_rect)
        all_sprites.draw(windowSurface)

        pygame.display.update()

        player_paddle[0].move()
        player_paddle[1].move()
        player_paddle[2].move()
        ball.move()
        ai_move(ai_paddle, ball)
        has_hit_ball()

        if ball.rect.right > WINDOWWIDTH:
            player_score += 1
            ball.reset()
        elif ball.rect.top < 0:
            if ball.rect.centerx > surface_rect.centerx:
                player_score += 1
            elif ball.rect.centerx < surface_rect.centerx:
                ai_score += 1
            ball.reset()
        elif ball.rect.left < 0:
            ai_score += 1
            ball.reset()
        elif ball.rect.bottom > WINDOWHEIGHT:
            if ball.rect.centerx > surface_rect.centerx:
                player_score += 1
            elif ball.rect.centerx < surface_rect.centerx:
                ai_score += 1
            ball.reset()

        difference = abs(player_score - ai_score)
        if player_score >= 11 and difference > 1:
            current_round += 1
            player_win_round += 1
            player_score = 0
            ai_score = 0

        elif ai_score >= 11 and difference > 1:
            current_round += 1
            ai_win_round += 1
            ai_score = 0
            player_score = 0

        if player_win_round >= 3:
            player_win = True
            game_is_on = False
            break
        elif ai_win_round >= 3:
            ai_win = True
            game_is_on = False
            break

    while not game_is_on:
        pygame.mouse.set_visible(1)
        windowSurface.fill(BLACK)
        pygame.mixer.music.stop()

        play_again = font.render("Play Again?", True, WHITE, BLACK)
        play_again_rect = play_again.get_rect()
        play_again_rect.centerx = surface_rect.centerx
        play_again_rect.centery = 500
        windowSurface.blit(play_again, play_again_rect)

        if player_win:
            if resultSound:
                win.play()
                resultSound = False
            game_over = font.render("GAME OVER", True, WHITE, BLACK)
            game_over1 = font.render("Player Wins", True, WHITE, BLACK)
        elif ai_win:
            if resultSound:
                lose.play()
                resultSound = False
            game_over = font.render("GAME OVER", True, WHITE, BLACK)
            game_over1 = font.render("You Lose", True, WHITE, BLACK)

        game_over_rect = game_over.get_rect()
        game_over_rect.centerx = surface_rect.centerx
        game_over_rect.centery = surface_rect.centery - 50
        game_over1_rect = game_over1.get_rect()
        game_over1_rect.centerx = game_over_rect.centerx
        game_over1_rect.centery = game_over_rect.centery + 75

        windowSurface.blit(game_over, game_over_rect)
        windowSurface.blit(game_over1, game_over1_rect)
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(mouse_pos):
                    is_play_again = True
                    game_is_on = True
                    win.stop()
                    lose.stop()
                    resultSound = True
                    break

