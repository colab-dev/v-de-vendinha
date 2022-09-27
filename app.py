# -*- coding: utf-8 -*-
# This magic commend above solves the error that is raising on MacOS when trying
# to execute the game:
#
#  File "app.py", line 26
#  SyntaxError: Non-ASCII character '\xc3' in file app.py on line 26, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details

import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

### Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

### Creating colors
BLACK = (0, 0, 0)
GRAY = (103, 103, 143)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 450
SPEED = 0
SCORE = 0
START = 0
LIFES = 3

### Setting up Fonts
font = pygame.font.SysFont("Verdana", 20)
start_instruction = font.render("Aperte Espaço para começar...", True, GRAY)
font_small = pygame.font.SysFont("Verdana", 20)

### Laoding Game Over image
game_over = pygame.image.load("./resources/images/gameover.png")

image_not_scaled = pygame.image.load("./resources/images/GroceryShelf.png")
background = pygame.transform.scale(image_not_scaled, (SCREEN_WIDTH, SCREEN_HEIGHT))

### Create a white screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("V de Vendinha")

### Life icon
image_not_scaled = pygame.image.load("./resources/images/brocolis.png")
life_icon = pygame.transform.scale(image_not_scaled, (32, 32))


vegan_products_list = ["./resources/images/onion.png", "./resources/images/eggplant.png", "./resources/images/bell-pepper.png"]

class VeganProducts(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()

        self.update()

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30,SCREEN_WIDTH-30),-30)

      def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            self.update()
            self.reappear()

      def reappear(self):
        self.rect.top = 0 + random.randint(0, 50)
        self.rect.center = (random.randint(30, SCREEN_WIDTH-30), 0)

      def update(self):
        image_not_scaled = pygame.image.load(random.choice(vegan_products_list))
        self.image = pygame.transform.scale(image_not_scaled, (64, 64))

      def draw(self, surface):
        surface.blit(self.image, self.rect)


enemies_list = ["./resources/images/beef.png", "./resources/images/cheese.png", "./resources/images/chicken.png"]

class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.update()

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH-30), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            self.update()
            self.reappear()
    def reappear(self):
        self.rect.top = 0 + random.randint(0, 50)
        self.rect.center = (random.randint(30, SCREEN_WIDTH-30), 0)

    def update(self):
        image_not_scaled = pygame.image.load(random.choice(enemies_list))
        self.image = pygame.transform.scale(image_not_scaled, (64, 64))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./resources/images/Basket.png")

        self.rect = self.image.get_rect()
        self.rect.center = (160, 400)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

### Setting up Sprites
P1 = Player()
VP1 = VeganProducts()
VP2 = VeganProducts()
VP3 = VeganProducts()
VP4 = VeganProducts()
E1 = Enemies()
E2 = Enemies()

### Creating Sprites Groups
veganProducts = pygame.sprite.Group()
veganProducts.add(VP1)

enemies = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(VP1)

### Adding a new User event
INC_SPEED = pygame.USEREVENT + 1       # Makes the event unique
pygame.time.set_timer(INC_SPEED, 1000) # Fires the event every 1000 ms (this will increase the speed later in the code)


pygame.mixer.music.load('./resources/audio/background.wav')
pygame.mixer.music.play(-1)  # -1 makes music play in a loop

events = pygame.event.get()
for event in events:
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            START = 1

while True:

    ### Cycles through all events occuring
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and START == 0:
                START = 1
                SPEED = 5

        if event.type == INC_SPEED and START == 1:
              SPEED += 0.05

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0,0))

    if START == 0:
        DISPLAYSURF.blit(start_instruction, (120,50))

    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (SCREEN_WIDTH/2, 10))

    for i in range(LIFES):
        DISPLAYSURF.blit(life_icon, ((10 + 40*i), 10))


    ### Set levels
    if SCORE == 20:
        veganProducts.add(VP2)
        all_sprites.add(VP2)

    if SCORE == 30:
        enemies.add(E1)
        all_sprites.add(E1)

    if SCORE == 60:
        veganProducts.add(VP3)
        all_sprites.add(VP3)

    if SCORE == 100:
        enemies.add(E2)
        all_sprites.add(E2)


    ### Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    ### To be run if collision occurs between Player and VeganProducts
    if pygame.sprite.spritecollideany(P1, veganProducts):

        pygame.sprite.spritecollideany(P1, veganProducts).update()
        pygame.sprite.spritecollideany(P1, veganProducts).reappear()

        SCORE += 1

    ### To be run if collision occurs between Player and Enemies
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('./resources/audio/fail.wav').play()

        pygame.sprite.spritecollideany(P1, enemies).update()
        pygame.sprite.spritecollideany(P1, enemies).reappear()

        LIFES -= 1

    if LIFES == 0:
        pygame.mixer.music.stop()
        pygame.mixer.Sound('./resources/audio/gameover.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(game_over, (0,0))

        pygame.display.update()

        for entity in all_sprites:
            entity.kill()

        print(SCORE)

        time.sleep(3)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
