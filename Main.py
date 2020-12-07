import pygame
import random
import os

WIDTH = 800
HEIGHT = 600
FPS = 30
#CONSTANTS - PHYSICS
PLAYER_ACC = 0.9
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.9
vec = pygame.math.Vector2
GROUND = HEIGHT - 50

#DEFINE COLORS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0 ,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#ASSET FOLDERS
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

#BULLET CLASS
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "bullet_img")).convert()
        self.image = bullet_img
        
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
#PLAYER CLASS
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "jumper1.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.y_speed = 5
        
        self.pos = vec(10, GROUND - 60)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.centerx = WIDTH /2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0 #user-built speed var
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
    def update(self):
        #Acceleration
        self.acc = vec(0, PLAYER_GRAV)
        # RETURNS A LIST, keystate, OF ALL KEYS PRESSED
        keystate = pygame.key.get_pressed()
        # CHECKS TO SEE WHICH KEYS WERE I THE LIST
        if keystate[pygame.K_RIGHT]:
            self.acc.x += PLAYER_ACC
        if keystate [pygame.K_LEFT]:
            self.acc.x += -PLAYER_ACC
        if keystate [pygame.K_UP]:
            self.rect.y += -5
        if keystate[pygame.K_DOWN]:
            self.rect.y += 5
        if self.vel.y == 0 and keystate[pygame.K_SPACE]:
            self.vel.y = -20
        if keystate[pygame.K_SPACE]:
            self.shoot()
        #Wrap platform
        if (self.rect.x == 30):
                    self.rect.x = 0
     
        self.speedx = 0 #always stationary

        

    

      
        #EQUATIONS OF MOTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #APPLY FRICTION IN THE X DIRECTION
        self.acc.x += self.vel.x * PLAYER_FRICTION


        #EQUATIONS OF MOTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #SIMULATE THE GROUND
        if self.pos.y > GROUND:
            self.pos.y = GROUND + 1
            self.vel.y = 0

        #SET THE NEW PLAYER POSTIION BASED ON ABOVE
        self.rect.midbottom = self.pos
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            

#PLATFORM CLASS
class Platform(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.y_speed = 5
    def update(self):
        self.rect.x += -5
        if self.rect.right < 0:
            self.rect.left = WIDTH

#INITIALIZE VARIBLES
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enter the void")

clock = pygame.time.Clock()

#SPRITE GROUPS
all_sprites = pygame.sprite.Group()
player = Player()
platform = Platform()
all_sprites.add(player)
all_sprites.add(platform)


#GAME loop:
#   Process Events
#   Update
#   Draw

running = True
while running:
    clock.tick(FPS)

    #process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #UPDATE
    all_sprites.update()

    #DRAW
    screen.fill(BLACK)
    all_sprites.draw(screen)

    #FLIP AFTER DRAWING
    pygame.display.flip()

pygame.quit()


#_________________________________________________________________________________
