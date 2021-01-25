import pygame
import random
import os
import math
import time
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
snd_folder = os.path.join(game_folder, "snd")

#BULLET CLASS
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, dest_x, dest_y):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "bullet_img.jpg")).convert()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.image.set_colorkey(BLACK)

        #ESTABLISH RECT, STARTING POSITION
        self.rect = self.image.get_rect()
        self.rect.left = start_x
        self.rect.bottom = start_y

        #MAKE STARTING POINT MORE ACCURATE
        self.floating_point_x = start_x
        self.floating_point_y = start_y

        #DIFFERENCE BTW START AND DEST PTS
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        #APPLY VELOCITY
        self.speedx = 20
        self.change_x = math.cos(angle) * self.speedx
        self.change_y = math.sin(angle) * self.speedx

    def update(self):

        # The floating point x and y hold our more accurate location.
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x
 
        # The rect.x and rect.y are converted to integers.
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)

        #DELETE LASER ONCE OFF SCREEN
        # If the bullet flies of the screen, get rid of it.
        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()

            
#PLAYER CLASS
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "jumper1.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 1, HEIGHT / 1)
        self.y_speed = 5
        
        self.pos = vec(10, GROUND - 60)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.centerx = WIDTH /2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0 #user-built speed var
        self.shoot_delay = 25
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

            
        #WRAP PLATFORM
        if (self.rect.x == 30):
                    self.rect.x = 0
     
        self.speedx = 0 #always stationary
        
        #MOUSE EVENTS
        mouseState = pygame.mouse.get_pressed()
        if mouseState[0] == 1:
            pos = pygame.mouse.get_pos()
            mouse_x = pos[0]
            mouse_y = pos[1]
            self.shoot(mouse_x, mouse_y)
            
      
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

        #SET THE NEW PLAYER POSITION BASED ON ABOVE
        self.rect.midbottom = self.pos
        
    def shoot(self, mouse_x, mouse_y):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            bullet = Bullet(self.rect.right, self.rect.centery, mouse_x, mouse_y)
            self.last_shot = now
            
            all_sprites.add(bullet)
            bullets.add(bullet)

          
          
#ENEMY PROJECTILE
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((20,20))
        self.image.fill(GREEN)
        self.rect=self.image.get_rect()
        self.rect.center = (x, y)
        self.speedy=speed
        
    def update(self):
        self.rect.y+=self.speedy
        if self.rect.top > HEIGHT:
            self.rect.bottom=0
#START SCREEN FUNCTION






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
shoot_sound = pygame.mixer.Sound(os.path.join(snd_folder, "laser3.wav"))
clock = pygame.time.Clock()
#RANDOM PROJECTILE GENERATOR
def newProjectile():
    x = random.randint(10, WIDTH - 10)
    y = random.randint(-200, -20 )
    speed = random.randint(5 ,50)
    

    projectile = Projectile(x, y, speed)
    all_sprites.add(projectile)






#SPRITE GROUPS
all_sprites = pygame.sprite.Group()
player = Player()
platform = Platform()
all_sprites.add(player)
all_sprites.add(platform)
bullets = pygame.sprite.Group()
#GAME loop :
#   Process Events
#   Update
#   Draw

running = True

start = True



#DRAW TEXT FUNCTION
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, GREEN)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


#Start Screen Function
def show_start_screen():
    screen.fill(BLACK)
    draw_text(screen, "Enter the Void", 64,  WIDTH / 2, HEIGHT / 4)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                print("Key pressed to start game!")
                waiting = False
                
while running:
    #Start Screen
    if start:
        show_start_screen()
        start = False
        
    clock.tick(FPS)

    #process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    newProjectile()

    #UPDATE
    all_sprites.update()

    #DRAW
    screen.fill(BLACK)
    all_sprites.draw(screen)

    #FLIP AFTER DRAWING
    pygame.display.flip()

pygame.quit()


#_________________________________________________________________________________
