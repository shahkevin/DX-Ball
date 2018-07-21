# DX Ball Game
import pygame


# import random
from os import path

img_dir = path.join(path.dirname(__file__), 'Images')

WIDTH = 600
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (70, 8))

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = +8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ball_img, (15,15))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 18
        self.speedx = 0
        self.speedy = 0

    def update(self):
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speedx *= -1
        elif self.rect.left < 0:
            self.rect.left = 0
            self.speedx *= -1
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speedy = 0
            self.speedx = 0
        elif self.rect.top < 0:
            self.rect.top = 0
            self.speedy *= -1
        keystate = pygame.key.get_pressed()
        if self.speedx == 0 and self.speedy == 0 and keystate[pygame.K_SPACE]:
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 18
            self.speedx = 8
            self.speedy = -8
        self.rect.x += self.speedx
        self.rect.y += self.speedy

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(brick_img, (60, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Load all game graphics
background = pygame.image.load(path.join(img_dir, "bg_1_1.png")).convert()
background_rect = background.get_rect()
ball_img = pygame.image.load(path.join(img_dir, "sphere-00.png")).convert()
brick_img = pygame.image.load(path.join(img_dir, "brick.png")).convert()
player_img = pygame.image.load(path.join(img_dir, "PlayerDisc.png")).convert()

all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
bricks = pygame.sprite.Group()
brickslayer1 = pygame.sprite.Group()
brickslayer2 = pygame.sprite.Group()
brickslayer3 = pygame.sprite.Group()
player = Player()
ball = Ball()
for i in range(9):
    brick = Brick(30+(60*i), 20)
    all_sprites.add(brick)
    bricks.add(brick)
    brickslayer1.add(brick)
for i in range(8):
    brick = Brick(60+(60*i), 45)
    all_sprites.add(brick)
    bricks.add(brick)
    brickslayer2.add(brick)
for i in range(7):
    brick = Brick(90+(60*i), 70)
    all_sprites.add(brick)
    bricks.add(brick)
    brickslayer3.add(brick)
all_sprites.add(player)
all_sprites.add(ball)
balls.add(ball)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()
    # check to see if the ball hit the player
    collision_player_ball = pygame.sprite.spritecollide(player, balls, False)
    keystate = pygame.key.get_pressed()
    if collision_player_ball:
        if keystate[pygame.K_UP]:
            if ball.speedy < 16:
                ball.speedy *= -2
            else:
                ball.speedy = -16
        elif keystate[pygame.K_DOWN]:
            if ball.speedy > 4:
                ball.speedy /= -2
            else:
                ball.speedy = -4
        else:
            ball.speedy = -1 * ball.speedy
        # adding friction
        if player.speedx > 0:
            ball.speedx = 8
        elif player.speedx < 0:
            ball.speedx = -8
    # check to see if ball hit the brick
    collision_brick_ball = pygame.sprite.groupcollide(bricks, balls, True, False)
    if collision_brick_ball:
        ball.speedy = -1 * ball.speedy
        ball.speedx = -1 * ball.speedx
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
