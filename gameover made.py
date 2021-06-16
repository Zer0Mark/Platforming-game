import pygame
import time
from pygame.locals import * #allows the use of pygame local
import sys
import random 


pygame.init() #initialises pygame
vec = pygame.math.Vector2 #2 for two dimensional
#constants for the game
HEIGHT = 450 #screen height 
WIDTH = 400 #screen width
ACC = 0.5 #player acceleration
FRIC = -0.12 #player friction
FPS = 60 #framerate of the game
 
FramePerSec = pygame.time.Clock() #creates a clock object to keep time | #used to control frame rate
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT)) #draw the window
pygame.display.set_caption("Game") #sets the title bar caption
 
class Player(pygame.sprite.Sprite): #player object, a sprite is needed to move an object.
    def __init__(self):
        super().__init__() 
        #self.image = pygame.image.load("character.png")
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255,255,0)) #colour for the player
        self.rect = self.surf.get_rect() #makes it visible for us as the player (prints out the player)
   
        self.pos = vec((10, 360)) #horizontal acceleration and vertical acceleration
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
 
    def move(self): #movement for the player
        self.acc = vec(0,0.5) # Gravity function 0.5 vertical function
    
        pressed_keys = pygame.key.get_pressed() # Key press 
                
        if pressed_keys[K_LEFT]: #Arrow key left
            self.acc.x = -ACC # negative acceleration to the left <-
        if pressed_keys[K_RIGHT]: #Arrow key right
            self.acc.x = ACC # postive acceleration to the right ->
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc #equation for friction to slow the player down
         
        if self.pos.x > WIDTH: #screen warping allows the player to gotowards a wall and end up on the other side
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos #screen warping
 
    def jump(self): 
        hits = pygame.sprite.spritecollide(self, platforms, False) # This gives the ability for the spirtes to collide with each (collison)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15 #jump height vertical velocity, its negative to be able to give the player jump height
 
    def cancel_jump(self): # cancel jump is used for short jumps in the game/ or the ability to control what kind of jump you want. since not all platforms will be as high as possilbe.
        if self.jumping: #if we were to speedrun a platform to regain the ability to jump again then we'd have to short jump to just reach it//make contact with it.
            if self.vel.y < -3: #this adds a new element of jump to the current one instead of fully jumping to -15, its a lower value so the jump has the ability to short jump
                self.vel.y = -3
 
    def update(self):
        hits = pygame.sprite.spritecollide(self ,platforms, False) #contact with the platform/ Sprites collide
        if self.vel.y > 0:        
            if hits: #if hits makes it so there isn't so you can double jump or have multple jumps, so what we want is a single jump
                if self.pos.y < hits[0].rect.bottom:               
                    self.pos.y = hits[0].rect.top +1 #relocates the player to the top of platform using the variable y-coordinate
                    self.vel.y = 0 #velocity playey =0 to stop the vertical gravity
                    self.jumping = False
 
 
class platform(pygame.sprite.Sprite): #Sprites for the platforms/class
    def __init__(self):
        super().__init__() # init builds the platform
        self.surf = pygame.Surface((random.randint(50,100), 12)) #random spawn generation
        self.surf.fill((0,255,0)) #Colour of the platforms
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10), random.randint(0, HEIGHT-30))) #puts the platform around the screen in a random location.
        
 
    def move(self):
        pass
 
 
def check(platform, groupies): # randomly generated grouped platforms together 
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False
 
def plat_gen(): #random level generation, it creates future platforms when the player moves up the screen
    while len(platforms) < 6: # the platform generation
        width = random.randrange(50,100)
        p  = platform()      
        C = True
         
        while C:
             p = platform()
             p.rect.center = (random.randrange(0, WIDTH - width), # randomize the width/size of the platform, 
                              random.randrange(-50, 0)) # between -50 and 0
             C = check(p, platforms)
        platforms.add(p) # adds platforms and generates them
        all_sprites.add(p) #sprites are also added
 
 
        
PT1 = platform() #platform 1
P1 = Player() #player entity
 
PT1.surf = pygame.Surface((WIDTH, 20)) # the begining platform spawn
PT1.surf.fill((255,0,70)) #the colour is set to red
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT -10)) # 
 
all_sprites = pygame.sprite.Group()  #defines the group as = pygame.sprite.Group
all_sprites.add(PT1) #adds platform 1
all_sprites.add(P1) #adds player 1 
 
platforms = pygame.sprite.Group() # splitting the platform sprites from all_sprites
platforms.add(PT1) #adds platform to it
 
for x in range(random.randint(4,5)): 
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)
 
 
while True: #game loop, it updates when the player presses a button 
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE: # Space bar hold (Charges the jump)
                P1.jump()
        if event.type == pygame.KEYUP:    
            if event.key == pygame.K_SPACE: # Releases the jump/ cancel jump this makes variable jumping heights
                P1.cancel_jump()  
 
    if P1.rect.top <= HEIGHT / 3: #platform killing for the game.
        P1.pos.y += abs(P1.vel.y) 
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT: # If platform reaches 0/height since height is place at the bottom
                plat.kill()  #it kills the platform once it reaches so and so height
    if P1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            displaysurface.fill((255,0,0))
            pygame.display.update()
            time.sleep(1)
            pygame.quit()
            sys.exit()

 
    plat_gen()
    displaysurface.fill((0,0,0))
     
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()
 
    pygame.display.update()
    FramePerSec.tick(FPS) #frames per second of the game, the games fps


#check 108 and 107 again
#whats after 137 I dont understand it yet