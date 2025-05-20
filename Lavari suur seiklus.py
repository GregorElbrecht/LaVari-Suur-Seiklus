import pygame
from pygame import *
from random import randint

pygame.init()

# Värvid
white = (255, 255, 255)
black = (0, 0, 0)

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

# LaVar pilt
playerImage = pygame.image.load("Download-removebg-preview.png")

# Korvpalli pilt
pallImage = pygame.image.load("Basketball.png")

# Helid
speedup = pygame.mixer.Sound("Sonic Spin Dash - Sound Effect.mp3")
boing = pygame.mixer.Sound("Basketball Bounce - Sound Effect.mp3")
boo = pygame.mixer.Sound("Crowd Booing with a Boo You Suck! at the End  Funny.mp3")

# Stardiekraan
def start_screen():
    screen.fill(black)
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

# Mute/unmute
def toggle_mute():
    global heli_sees
    heli_sees = not heli_sees
    volume = 0.6 if heli_sees else 0
    muusika.set_volume(volume)
    boing.set_volume(0.4 if heli_sees else 0)
    speedup.set_volume(0.1 if heli_sees else 0)
    boo.set_volume(0.3 if heli_sees else 0)

# Mängu funktsioon
def run_game():
    global heli_sees

    # Algväärtused
    posX, posY = 120, 320
    lavar = pygame.Rect(posX, posY, 50, 100)
    player_scaled = pygame.transform.scale(playerImage, [lavar.width, lavar.height])
    enemies = []
    score = 0
    pallide_arv = 31
    palli_kiirus = 7
    viimane_kiirendus = 0
    speedup_text_timer = 0
    speedup_text_y = 300

    start_time = pygame.time.get_ticks()
    gameover = False

    while not gameover:
        screen.blit(bg_image, (0, 0))

        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        time_text = font.render(f"Timer: {round(elapsed_time, 1)}s", True, white)
        score_text = font.render(f"Punktid: {score}", True, white)
        screen.blit(time_text, (500, 10))
        screen.blit(score_text, (200, 10))

        # Speedup tekst ja efekt
        if score >= viimane_kiirendus + 10:
            palli_kiirus += 2
            pallide_arv -= 1
            viimane_kiirendus = score
            speedup.play()
            speedup_text_timer = pygame.time.get_ticks()
            speedup_text_y = 300

        if pygame.time.get_ticks() - speedup_text_timer < 1000:
            kiirus_text = font.render("Speed up!", True, white)
            screen.blit(kiirus_text, (0, speedup_text_y))
            speedup_text_y -= 2  # Tekst liigub üles

        # Uus korvpall
        if randint(1, pallide_arv) == 1:
            enemy_rect = pygame.Rect(ekraanX, randint(50, ekraanY - 70), 60, 73)
            enemies.append(enemy_rect)
            boing.play()

        # Korvpallide liikumine
        for enemy in enemies[:]:
            enemy.x -= palli_kiirus
            if lavar.colliderect(enemy):
                boo.play()
                pygame.time.delay(1000)
                gameover = True
            elif enemy.x + enemy.width < 0:
                enemies.remove(enemy)
                score += 1
            else:
                screen.blit(pygame.transform.scale(pallImage, (enemy.width, enemy.height)), enemy)

        # Mängija juhtimine
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    posY -= 5
                elif event.key == K_DOWN:
                    posY += 5
                posY = pygame.math.clamp(posY, 0, ekraanY - lavar.height)
            elif event.type == MOUSEBUTTONDOWN:
                if mute_rect.collidepoint(event.pos):
                    toggle_mute()

        lavar.y = max(0, min(ekraanY - lavar.height, posY))
        screen.blit(player_scaled, lavar)

        # Mute ikoon
        screen.blit(unmute_icon if heli_sees else mute_icon, mute_rect)

        pygame.display.flip()
        clock.tick(60)

    # Game Over ekraan + Uuesti
    while True:
        screen.fill((0, 0, 0))
        gameover_text = font.render("GAME OVER", True, white)
        time_text = font.render(f"Pidasid vastu: {round(elapsed_time, 1)}s", True, white)
        score_text = font.render(f"Punkte kogusid: {score}", True, white)
        restart_text = font.render("UUESTI", True, black)

        restart_button = pygame.Rect(ekraanX // 2 - 100, ekraanY // 2 + 130, 200, 60)
        pygame.draw.rect(screen, white, restart_button)
        screen.blit(restart_text, (restart_button.x + 35, restart_button.y + 10))

        screen.blit(gameover_text, (ekraanX // 2 - 150, ekraanY // 2 - 50))
        screen.blit(time_text, (ekraanX // 2 - 150, ekraanY // 2 + 20))
        screen.blit(score_text, (ekraanX // 2 - 150, ekraanY // 2 + 70))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return

start_screen()
while True:
    run_game()
