# Import the pygame module
import pygame
import random
import time


vec = pygame.math.Vector2  # will be used as a position vector

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_SPACE
)  # keys that will be pressed by the user


pygame.init()  # Start the game (initializing)



# Create a custom event for adding a new enemy  source: https://realpython.com/lessons/custom-events/
ADDBULLET = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBULLET, 3000)

ADDROLL = pygame.USEREVENT + 0
pygame.time.set_timer(ADDROLL, 4000)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((30, 30))  # square 30 by 30 pix
        self.pos = vec((SCREEN_WIDTH/2, SCREEN_HEIGHT))  # initial position of the player
        self.rect = self.surf.get_rect()  
        self.vel = vec(0,0)  # velocity
        self.acc = vec(0,0)  # acceleration 

    def move(self, pressed_keys):
        self.acc = vec(0,0.003)  # gravity
        self.acc.x += self.vel.x
        self.vel += self.acc
        self.pos += self.vel + 0.002 * self.acc        

        if pressed_keys[K_UP]:
            while self.pos.y >= SCREEN_HEIGHT - 150:
                self.acc = vec(0,0.003)
                self.acc.x += self.vel.x
                self.vel += self.acc
                self.pos += -self.vel + 0.002 * self.acc

            if self.pos.y >= SCREEN_HEIGHT -50:  # upper constraint for jumping 
                self.rect.bottomleft = SCREEN_HEIGHT -50  

            
        # move left
        if pressed_keys[K_LEFT]:
            self.pos.x += -5

        # move right
        if pressed_keys[K_RIGHT]:
            self.pos.x += 5

        #stay on the ground
        if self.pos.y >= SCREEN_HEIGHT -50:
            self.pos.y = SCREEN_HEIGHT 
        
        # stay between right and left
        if self.pos.x >= SCREEN_WIDTH:
            self.pos.x = SCREEN_WIDTH

        if self.pos.x <= 0:
            self.pos.x = 0

        self.rect.center = self.pos  # pass position vector to rect




# bullets top-down
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((5, 255, 255))  # set the color of the rec
        self.rect = self.surf.get_rect()
        self.pos = vec((random.randint(0, SCREEN_WIDTH), 0))
        self.speed = random.randint(1, 5)  # random speed between 1 and 5
    
    def move(self):  # moving top - down 
        self.pos.y += self.speed
        self.rect.center = self.pos 
        


# rollers right - left
class Rollers(pygame.sprite.Sprite):
    def __init__(self):
        super(Rollers, self).__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((80, 100, 255))
        self.rect = self.surf.get_rect()
        self.side = random.choice([0, SCREEN_WIDTH])  # randomly starting from the left or from the right
        self.pos = vec(self.side, SCREEN_HEIGHT - 20)
        self.speed = random.randint(1, 5)
    
    def move(self):  # moving right - left 
        if self.side == 0:
            self.pos.x += self.speed
        elif self.side == SCREEN_WIDTH:
            self.pos.x -= self.speed
        
        self.rect.center = self.pos



SCREEN_WIDTH = 900.0
SCREEN_HEIGHT = 500.0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
shot = pygame.image.load("Desktop/Teacher Assistant/pygame/back.jpg")  # setting up bg image
go = pygame.image.load("Desktop/Teacher Assistant/pygame/go.jpg")  # setting up game over screen image
screen.fill((0,0,0))

# Lives
lives = 5  # number of lives at the beginning
font= pygame.font.SysFont('Arial', 100)  # setting up font

def show_lives(lives):
    lives_value = pygame.font.Font.render(font, "Lives: " + str(lives), True, (225,223,225))  # render the text
    screen.blit(lives_value, (50, 50))  # show it on screen 

# Game over function
def game_over_fun ():
    screen.blit(go, (0,0))
    screen.blit(pygame.font.Font.render(font, "Game Over", True, (225,225,225)), (100, 100))
    pygame.display.flip()


    user_reset = False
    while not user_reset:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                user_reset = True
            if event.type == pygame.KEYDOWN:  # if any key is pressed 
                if event.key == pygame.K_SPACE:  # if space key is pressed
                    user_reset = True



player = Player()  # main player

bullets = pygame.sprite.Group()  # bullets as a group 

players = pygame.sprite.Group()  # players as a group (only for comparison later)
players.add(player)



running = True  # Variable to keep the main loop running
game_over = False
# Main loop
while running:

    if game_over == True:
        game_over_fun()  # call the game over function
        lives = 5  # set lives to 5 back
        game_over = False  # end game over

        
    event = pygame.event.poll()  # get an event

    if event.type == pygame.QUIT:
        running=0

    elif event.type == ADDBULLET:  # create new bullet in the time set by ADDBULLET
        new_bullet = Bullet()
        bullets.add(new_bullet)

    elif event.type == ADDROLL:   # create new roll in the time set by ADDBULLET
        new_roll = Rollers()
        bullets.add(new_roll)


    # Set the image on screen (if you don't do it enemies and players will replace it)
    screen.blit(shot, (0,0))

    # Set player on the screen 
    screen.blit(player.surf, player.rect)
    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()
    # Update the player sprite based on user keypresses
    player.move(pressed_keys)

    # Show the lives score by calling the function
    show_lives(lives) 
    
    for bullet in bullets:
        screen.blit(bullet.surf, bullet.rect)
        bullet.move()  # move bullets (both types have the function move)

        coll = pygame.sprite.groupcollide(bullets, players, True, False)  # check wheter there was a collision
        if coll:
            lives -= 1

            # game over at lives = 0
            if lives == 4:
                game_over = True
                              

    
   
    pygame.display.flip()

