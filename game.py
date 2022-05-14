# Import the pygame module
import pygame
import random



vec = pygame.math.Vector2  # will be used as a position vector

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_UP
)  # keys that will be pressed by the user


pygame.init()  # Start the game (initializing)



# Create a custom event for adding a new enemy  source: https://realpython.com/lessons/custom-events/
ADDBULLET = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBULLET, 3000)

ADDROLL = pygame.USEREVENT + 0
pygame.time.set_timer(ADDROLL, 4000)

ADDRASPBERRY = pygame.USEREVENT + 2
pygame.time.set_timer(ADDRASPBERRY, 3500)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((50, 50))  # square 30 by 30 pix

        image_not_scaled = pygame.image.load("./cat.png")
        self.image = pygame.transform.scale(image_not_scaled, (50, 50))

        self.pos = vec((SCREEN_WIDTH/2, SCREEN_HEIGHT))  # initial position of the player
        self.rect = self.surf.get_rect()  
        self.vel = vec(0,0)  # velocity
        self.acc = vec(0,0)  # acceleration 
        self.is_jumping = False  # if it is True, the player can't jump again

    def move(self, pressed_keys):
        self.acc.y = 0.003  # gravity
        self.pos += self.vel + 0.002 * self.acc        

        if pressed_keys[K_UP]:
            if self.is_jumping == False:
                self.vel = vec(0,0)
                self.is_jumping = True
                while self.pos.y >= SCREEN_HEIGHT - 150:
                    self.vel += self.acc  # velocity relation (so the jump is faster then the fall)
                    self.pos += -self.vel + 0.001 * self.acc  # jump (so the gravity but opposite sign)
                if self.pos.y >= SCREEN_HEIGHT -50:  # upper constraint for jumping 
                    self.rect.bottomleft = SCREEN_HEIGHT -50  
             
        # move left
        if pressed_keys[K_LEFT]:
            self.pos.x += -5

        # move right
        if pressed_keys[K_RIGHT]:
            self.pos.x += 5

        #stay on the ground
        if self.pos.y >= SCREEN_HEIGHT - 10:
            self.pos.y = SCREEN_HEIGHT - 10
            self.is_jumping = False
        
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
        self.surf = pygame.Surface((40, 40))

        image_not_scaled = pygame.image.load("./fire_up.png")
        self.image = pygame.transform.scale(image_not_scaled, (40, 40))

        self.rect = self.surf.get_rect()
        self.pos = vec((random.randint(0, SCREEN_WIDTH), 0))
        self.speed = random.randint(1, 5)  # random speed between 1 and 5
    
    def move(self):  # moving top - down 
        self.pos.y += self.speed
        self.rect.center = self.pos 
        


# bullets right - left
class Rollers(pygame.sprite.Sprite):
    def __init__(self):
        super(Rollers, self).__init__()
        
        self.surf = pygame.Surface((40, 40))

        image_not_scaled = pygame.image.load("./roll.png")
        self.image = pygame.transform.scale(image_not_scaled, (40, 40))

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



class Raspberries(pygame.sprite.Sprite):
    def __init__(self):
        super(Raspberries, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255,105,180))  # set the color of the rec
        self.rect = self.surf.get_rect()
        image_not_scaled = pygame.image.load("./rasp.png")
        self.image = pygame.transform.scale(image_not_scaled, (40, 40))
        self.pos = vec((random.randint(0, SCREEN_WIDTH), 0))
        self.speed = random.randint(1, 5)  # random speed between 1 and 5
    
    def move(self):  # moving top - down 
        self.pos.y += self.speed
        self.rect.center = self.pos 
        
        
    


SCREEN_WIDTH = 900.0
SCREEN_HEIGHT = 500.0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

shot_not_scaled = pygame.image.load("./back.jpg")  # bg image load
shot =  pygame.transform.scale(shot_not_scaled, (SCREEN_WIDTH, SCREEN_HEIGHT))  # bg image rescaled

go_not_scaled = pygame.image.load("./go.jpg")  # setting up game over screen image
go =  pygame.transform.scale(go_not_scaled, (SCREEN_WIDTH, SCREEN_HEIGHT))  # bg image rescaled

screen.fill((0,0,0))

# Lives
lives = 5  # number of lives at the beginning
points = 0 # number of points at the beginning
font= pygame.font.SysFont('Arial', 50)  # setting up font

def show_lives_and_points(lives, points):
    lives_value = pygame.font.Font.render(font, "Lives: " + str(lives), True, (225,223,225))  # render the text
    points_value = pygame.font.Font.render(font, "Points: " + str(points), True, (255,192,203))
    screen.blit(lives_value, (50, 50))  # show it on screen 
    screen.blit(points_value, (550, 50))  # show it on screen 

# Game over function
def game_over_fun (points):
    screen.blit(go, (0,0))
    screen.blit(pygame.font.Font.render(font, "Game Over", True, (225,225,225)), (100, 100))
    screen.blit(pygame.font.Font.render(font, "Points: " + str(points) + "!", True, (225,225,225)), (150, 150))
    screen.blit(pygame.font.Font.render(font, "Press space to play again", True, (225,225,225)), (300, 300))
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
raspberries = pygame.sprite.Group()  # raspberries as a group

players = pygame.sprite.Group()  # players as a group (only for comparison later)
players.add(player)





running = True  # Variable to keep the main loop running
game_over = False
# Main loop
while running:

    if game_over == True:
        game_over_fun(points)  # call the game over function
        lives = 5  # set lives to 5 back
        points = 0 # set points to 0 
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

    elif event.type == ADDRASPBERRY:   # create new roll in the time set by ADDRASPBERRY
        new_rasp = Raspberries()
        raspberries.add(new_rasp)


    # Set the image on screen (if you don't do it enemies and players will replace it)
    screen.blit(shot, (0,0))

    # Set player on the screen 
    screen.blit(player.image, player.rect)
    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()
    # Update the player sprite based on user keypresses
    player.move(pressed_keys)

    # Show the lives score by calling the function
    show_lives_and_points(lives, points) 
    
    for bullet in bullets:
        screen.blit(bullet.image, bullet.rect)
        bullet.move()  # move bullets (both types have the function move)

        coll = pygame.sprite.groupcollide(bullets, players, True, False)  # check wheter there was a collision
        
        if coll:
            lives -= 1

            # game over at lives = 0
            if lives == 0:
                game_over = True
        
    for rasperry in raspberries:
        screen.blit(rasperry.image, rasperry.rect)
        rasperry.move()

        catch = pygame.sprite.groupcollide(raspberries, players, True, False)  # check wheter raspberry was cought
        if catch:
            points += 1

    
   
    pygame.display.flip()

