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
pygame.display.set_icon(pygame.image.load("LaVar.png"))
clock = pygame.time.Clock()

# Mute/unmute pildid ja algne olek
mute_icon = pygame.image.load("mute.png")
unmute_icon = pygame.image.load("unmute.png")
mute_icon = pygame.transform.scale(mute_icon, (40, 40))
unmute_icon = pygame.transform.scale(unmute_icon, (40, 40))
heli_sees = True
mute_rect = pygame.Rect(ekraanX - 50, 10, 40, 40)

# Muusika
pygame.mixer.init()
muusika = pygame.mixer.Sound("G3 (LiAngelo Ball) - Tweaker (Official Audio) (1).mp3")
muusika.set_volume(0.6)
muusika.play()

# Taustapilt
bg_image = pygame.image.load("cbj-hornetsfloor5_1200xx5184-2916-0-270.jpg")

# Font
font = pygame.font.Font("Fortnite.ttf", 50)

pygame.key.set_repeat(1, 6)

# LaVar
posX, posY = 120, 320
lavar = pygame.Rect(posX, posY, 70, 120)
playerImage = pygame.image.load("LaVar.jpg")
playerImage = pygame.transform.scale(playerImage, [lavar.width, lavar.height])

# Korvpallid
enemies = []
pallImage = pygame.image.load("Basketball.png")

# Punktid ja pallide kiirus
score = 0
pallide_arv = 31
palli_kiirus = 7
viimane_kiirendus = 0

#Helieffektid
speedup = pygame.mixer.Sound("Sonic Spin Dash - Sound Effect.mp3")
speedup.set_volume(0.1  if heli_sees else 0)
boing = pygame.mixer.Sound("Basketball Bounce - Sound Effect.mp3")
boing.set_volume(0.4 if heli_sees else 0)
boo = pygame.mixer.Sound("Crowd Booing with a Boo You Suck! at the End  Funny.mp3")
boo.set_volume(0.3 if heli_sees else 0)

# Start Screen
def start_screen():
    screen.fill((0, 0, 0))
    info = pygame.image.load("keys.png")
    screen.blit(info, (780, 250))
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

# Heli mute/unmute
def toggle_mute():
    global heli_sees
    heli_sees = not heli_sees
    volume = 0.6 if heli_sees else 0
    muusika.set_volume(volume)
    boing.set_volume(volume)
    speedup.set_volume(volume)
    boo.set_volume(volume)

# Käivitame stardiekraani
start_screen()

# Taimeri algus
start_time = pygame.time.get_ticks()
gameover = False

while not gameover:
    screen.blit(bg_image, (0, 0))  # Taust

    # Aeg ja skoor
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    time_text = font.render(f"Timer: {round(elapsed_time, 1)}s", True, white)
    screen.blit(time_text, (500, 10))
    score_text = font.render(f"Punktid: {score}", True, white)
    screen.blit(score_text, (200, 10))

    # Kiiruse suurendamine iga 10 punkti järel
    if score >= viimane_kiirendus + 10:
        palli_kiirus += 2
        pallide_arv -= 1
        viimane_kiirendus = score
        speedup.play()
        kiirus_text = font.render(f"Speed up!", True, white)
        screen.blit(kiirus_text, (0,300))

    # Korvpallide genereerimine
    if randint(1, pallide_arv) == 1:
        enemy_rect = pygame.Rect(ekraanX, randint(50, ekraanY - 70), 60, 73)
        enemies.append(enemy_rect)
        boing.play()

    # Korvpallide liikumine
    for enemy in enemies[:]:
        enemy.x -= palli_kiirus

        if lavar.colliderect(enemy):
            gameover = True

            boo.play()
            pygame.time.delay(1000)
        elif enemy.x + enemy.width < 0:
            enemies.remove(enemy)
            score += 1
        else:
            screen.blit(pygame.transform.scale(pallImage, (enemy.width, enemy.height)), enemy)

    # Mängija liikumine
    for event in pygame.event.get():
        if event.type == QUIT:
            gameover = True
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                posY -= 5
            elif event.key == K_DOWN:
                posY += 5
            posY = pygame.math.clamp(posY, 0, 555)
        elif event.type == KEYUP:
            if event.key == K_UP or event.key == K_DOWN:
                speedY = 0
        elif event.type == MOUSEBUTTONDOWN:
            if mute_rect.collidepoint(event.pos):
                toggle_mute()

    # LaVar liikumise piiramine
    posY = max(0, min(ekraanY - lavar.height, posY))
    lavar.y = posY
    screen.blit(playerImage, lavar)

    # Mute/unmute ikoon
    if heli_sees:
        screen.blit(unmute_icon, mute_rect)
    else:
        screen.blit(mute_icon, mute_rect)

    pygame.display.flip()
    clock.tick(60)

# Game Over
screen.fill((0, 0, 0))
gameover_text = font.render("GAME OVER", True, white)
time_text = font.render(f"Ellu jaid: {round(elapsed_time, 1)}s", True, white)
score_text = font.render(f"Punkte kogusid: {score}", True, white)
info_text = font.render(f"Rakendus sulgeb automaatselt", True, white)

screen.blit(gameover_text, (ekraanX // 2 - 150, ekraanY // 2 - 50))
screen.blit(time_text, (ekraanX // 2 - 150, ekraanY // 2 + 20))
screen.blit(score_text, (ekraanX // 2 - 150, ekraanY // 2 + 70))
screen.blit(info_text, (ekraanX // 2 - 150, ekraanY // 2 + 120))
pygame.display.flip()

pygame.time.delay(3000)
pygame.quit()
