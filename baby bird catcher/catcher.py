import pygame, sys, random,time 
from pygame.locals import *

class Basket(pygame.sprite.Sprite):
    def __init__(self):
        super(Basket, self).__init__()
        self.index = 0
        self.x = 500
        self.y = 650
        self.direction = "left"
        self.image = pygame.image.load("baby bird catcher/picnic_basket.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200,140))
        self.pics = [[self.image,pygame.transform.flip(self.image,True,False)]]
        self.rect = self.image.get_rect(center = (500,670))

    def move(self,deltax):
        if deltax>0:
            self.direction = "right"
            self.image = self.pics[0][1]
        else:
            self.direction = "left"
            self.image = self.pics[0][0]
        
        self.rect.centerx += deltax

    def collide(self,deltax): #first collide function
        if self.rect.left<-40 or self.rect.right>1040:
            deltax *= -1

        self.rect.centerx += deltax


class Birdfall(pygame.sprite.Sprite):
    def __init__(self,randombird):
        super(Birdfall, self).__init__()
        self.index = 0
        self.pics = [[pygame.image.load("baby bird catcher/brownbird.png").convert_alpha(),pygame.image.load("baby bird catcher/redheadbird.png").convert_alpha(),pygame.image.load("baby bird catcher/yellowbelliedbird.png").convert_alpha(),pygame.image.load("baby bird catcher/yellowbluebird.png").convert_alpha()]]
        self.image = self.pics[0][randombird] #set second [] to random and add random argument into class, max3
        if randombird == 0:
            self.image = pygame.transform.scale(self.image, (75,50))
        if randombird == 1:
            self.image = pygame.transform.scale(self.image, (75,75))
        if randombird == 2:
            self.image = pygame.transform.scale(self.image, (50,50))
        if randombird == 3:
            self.image = pygame.transform.scale(self.image, (125,50))
        self.rect = self.image.get_rect(center = (random.randint(30,970), random.randint(-500,75)))

    def fall(self):
        if self.rect.bottom>740:
            self.rect = self.image.get_rect(center = (random.randint(20,980),random.randint(-100,0)))
        self.rect.centery += 3
    
    def relocate(self):
        self.rect = self.image.get_rect(center = (random.randint(20,980),random.randint(-250,-50)))


class Spikey(pygame.sprite.Sprite):
    def __init__(self):
        super(Spikey,self).__init__()
        self.image = pygame.image.load("baby bird catcher/spikeball.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (75,75))
        self.rect = self.image.get_rect(center = (random.randint(30,970), random.randint(-500,75)))

    def fall(self):
        if self.rect.bottom>740:
            self.rect = self.image.get_rect(center = (random.randint(20,980),random.randint(-100,0)))
        self.rect.centery += 3

#-------------------------------------------------------------------------------------------------------------#
pygame.init()
pygame.font.init()

screen_width = 1000
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Baby bird catcher")
clock = pygame.time.Clock()

# difficulty = input("Select difficulty: Easy(1), Medium(2), Hard(3), Impossible(4)\n")
# if difficulty == "1":
#     num_of_spikes = 3
# if difficulty == "2":
#     num_of_spikes = 8
# if difficulty == "3":
#     num_of_spikes = 15
# if difficulty == "4":
#     num_of_spikes = 30

basket = Basket()

birds = pygame.sprite.Group()
for i in range(10):
    number = random.randint(0,3)
    birds.add(Birdfall(number))

spikes = pygame.sprite.Group()
for i in range(8):
    spikes.add(Spikey())

birdsneeded = "100"

t0 = time.time()
font = pygame.font.SysFont(None, 48)
fonts = pygame.font.get_fonts()

display_surface = pygame.display.set_mode((1000, 750))
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render(birdsneeded, True, (0,0,0), (255,255,255))
textRect = text.get_rect()

win = font.render("You WIN!", True, (255,255,255), (0,0,0))
winrect = win.get_rect(center = (250,250))

lose = font.render("You Lost!", True, (255,255,255), (0,0,0))
loserect = lose.get_rect(center = (250,250))



running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if birdsneeded == "0":
        running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        basket.move(5)
        basket.collide(5)
    if keys[pygame.K_a]:
        basket.move(-5)
        basket.collide(-5)

    for bird in birds:
        bird.fall()
        if pygame.sprite.collide_mask(bird,basket): #second collision
            bird.relocate()
            birdsneeded = int(birdsneeded)
            birdsneeded -= 1
            birdsneeded = str(birdsneeded) 
            text = font.render(birdsneeded, True, (0,0,0), (255,255,255))

    for spike in spikes:
        spike.fall()
        if pygame.sprite.collide_mask(spike,basket):
            running = False
            
    screen.fill((255,255,255))

    screen.blit(basket.image, basket.rect.topleft)
    birds.draw(screen)
    spikes.draw(screen)
    
    display_surface.blit(text, textRect)

    pygame.display.flip()
    clock.tick(60)

running = True #win or lose
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    if birdsneeded == "0":
        screen = pygame.display.set_mode((500,500))
        display_surface.blit(win, winrect)
        pygame.display.set_caption("You WIN!")

    if birdsneeded != "0":
        screen = pygame.display.set_mode((500,500))
        display_surface.blit(lose,loserect)
        pygame.display.set_caption("You Lost!")


    pygame.display.flip() 
    clock.tick(60)



pygame.quit()
sys.exit()