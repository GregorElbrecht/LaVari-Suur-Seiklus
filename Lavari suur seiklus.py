import pygame
from pygame import *
from random import randint

pygame.init()

# Värvid
white = (255, 255, 255)

# Ekraani suurus
ekraanX, ekraanY = 1200, 675
screen = pygame.display.set_mode([ekraanX, ekraanY])
pygame.display.set_caption("LaVarri suur seiklus")
clock = pygame.time.Clock()

#muusika
pygame.mixer.init()
muusika = pygame.mixer.Sound("G3 (LiAngelo Ball) - Tweaker (Official Audio) (1).mp3")
muusika.set_volume(0.6)
muusika.play()

# Laadi taustapilt
bg_image = pygame.image.load("cbj-hornetsfloor5_1200xx5184-2916-0-270.jpg")

# Font
font = pygame.font.Font("Fortnite.ttf", 50)

pygame.key.set_repeat(1,6)

# LaVar
posX, posY = 120, 320
lavar = pygame.Rect(posX, posY, 70, 120)
playerImage = pygame.image.load("LaVar.png")
playerImage = pygame.transform.scale(playerImage, [lavar.width, lavar.height])

# Korvpallid
enemies = []
pallImage = pygame.image.load("Basketball.png")

# Taimeri algus
start_time = pygame.time.get_ticks()

gameover = False


# Start Screen
def start_screen():
    screen.fill((0, 0, 0))
    start_text = font.render("VAJUTA SPACE, ET ALUSTADA", True, white)
    screen.blit(start_text, (ekraanX // 2 - 350, ekraanY // 2 - 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                waiting = False


# Käivitame stardiekraani
start_screen()

# Taimeri algus
start_time = pygame.time.get_ticks()
gameover = False
while not gameover:
    screen.blit(bg_image, (0, 0))  # Tausta uuesti joonistamine

    # Mänguaeg ekraanile
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Sekundites
    time_text = font.render(f"Timer: {round(elapsed_time, 1)}s", True, white)
    screen.blit(time_text, (400, 10))

    # Pallide genereerimine
    if randint(1, 50) == 1:  # Väike tõenäosus uue palli tekkeks
        enemy_rect = pygame.Rect(ekraanX, randint(50, ekraanY - 70), 60, 73)
        enemies.append(enemy_rect)
        boing =  pygame.mixer.Sound("Basketball Bounce - Sound Effect.mp3")
        boing.play()

    # Pallide liikumine
    for enemy in enemies:
        enemy.x -= 5  # Liiguvad vasakule
        screen.blit(pygame.transform.scale(pallImage, (enemy.width, enemy.height)), enemy)

        # Kontrolli, kas pall tabab LaVarit
        if lavar.colliderect(enemy):
            gameover = True
            pygame.time.delay(1000)


    # Mängija juhtimine (liikumine nooleklahvidega)
    for event in pygame.event.get():
        if event.type == QUIT:
            gameover = True
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                posY += -4
            elif event.key == K_DOWN:
                posY += 4
            posY = pygame.math.clamp(posY, 0, 555)
        elif event.type == KEYUP:
            if event.key == K_UP or event.key == K_DOWN:
                speedY = 0

    # Piira liikumine ekraani sees
    posY = max(0, min(ekraanY - lavar.height, posY))
    lavar.y = posY  # Uuenda LaVari positsiooni
    screen.blit(playerImage, lavar)

    pygame.display.flip()
    clock.tick(60)


# "Game Over" ekraan
screen.fill((0, 0, 0))
gameover_text = font.render("GAME OVER", True, white)
time_text = font.render(f"Ellu jaid: {round(elapsed_time, 1)}s", True, white)
screen.blit(gameover_text, (ekraanX // 2 - 150, ekraanY // 2 - 50))
screen.blit(time_text, (ekraanX // 2 - 150, ekraanY // 2 + 20))
pygame.display.flip()

pygame.time.delay(2000)  # Näita ekraani 3 sekundit
pygame.quit()
