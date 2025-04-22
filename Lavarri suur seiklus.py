
import pygame
from pygame import *
from PIL import *
from random import randint

init()
# värvid
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
pink = [255, 153, 255]
lGreen = [153, 255, 153]
lBlue = [153, 204, 255]

font = font.Font("Fortnite.ttf", 50)
ekraanX = 1200
ekraanY = 675
screen = display.set_mode([ekraanX, ekraanY])
screen.blit(image.load("cbj-hornetsfloor5_1200xx5184-2916-0-270.jpg"),(0,0))
display.set_caption("LaVarri suur seiklus")
clock = time.Clock()
posX,posY = 120, 320
score = 0
pygame.key.set_repeat(1,6)
#LaVar

lavar = Rect(posX,posY,120,170)
playerimage = image.load("LaVar.png")
playerImage = transform.scale(playerimage, [lavar.width, lavar.height])

#korvpallid
enemies = []
totalEnemies = 1000
for i in range(1000):
    enemies.append(pygame.Rect(randint(0, ekraanX - 100), randint(0, ekraanY - 100), 60, 73))

pallImage = image.load("Basketball.png")
enemyImage = transform.scale(pallImage, [enemies[0].width, enemies[0].height])

gameover = False
while not gameover:

    timer = font.render("Timer:", True, (255, 255, 255))
    time_text = font.render(str(round((time.get_ticks()/1000),1)),True, (255,255,255))
    screen.blit(time_text, (400, 10))
    screen.blit(timer,(270,10))
    for event in pygame.event.get():
        if event.type == QUIT:
            gameover = True
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                posY += -3
            elif event.key == K_DOWN:
                posY += 3
            posY = pygame.math.clamp(posY,0,505)
        elif event.type ==KEYUP:
            if event.key == K_UP or event.key == K_DOWN:
                speedY = 0

    lavar = Rect(posX, posY, 70, 335)
    screen.blit(playerImage, lavar)

    display.flip()
    screen.blit(image.load("cbj-hornetsfloor5_1200xx5184-2916-0-270.jpg"), (0, 0))
    if gameover == True:
        quit()
quit()
