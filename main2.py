import random
import pygame
import os

# Initialize pygame
pygame.init()

# Character velocity
vel = 5
BULLET_VEL = 7

# Add sound
pygame.mixer.init()
bg_sound = pygame.mixer.Sound("bg.mp3")
bullet_sound = pygame.mixer.Sound("g2.mp3")
bg_sound.play(-1)  # Play the background sound on a loop

# Enemy speed factor
enemy_speed_factor = 1.5

# FPS
clock = pygame.time.Clock()
RED_BULLET = []
# Create a screen
WIDTH = 500
HEIGHT = 600

# Character size
s1 = 80
s2 = 80

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader")

icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Add background image
bg = pygame.image.load("bg.png")

# Add character
SPACESHIP_BLUE = pygame.image.load(os.path.join("blue.png"))
BLUE = pygame.transform.rotate(pygame.transform.scale(SPACESHIP_BLUE, (s1, s2)), 0)

# Enemy setup
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

def respawn_enemy(i):
    if i < num_of_enemies:
        enemyX[i] = random.randint(0, WIDTH - 64)
        enemyY[i] = random.randint(50, 150)
        enemyX_change[i] = 4 * enemy_speed_factor
        enemyY_change[i] = 40 * enemy_speed_factor

for i in range(num_of_enemies):
    YELLOW = pygame.image.load("enemy.png")
    enemyImg.append(YELLOW)
    enemyX.append(0)
    enemyY.append(0)
    enemyX_change.append(0)
    enemyY_change.append(0)
    respawn_enemy(i)

# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

def show_score(x, y):
    score_display = font.render("Score: " + str(score), True, (255, 255, 255))
    WIN.blit(score_display, (x, y))

def is_collision(player_rect, enemy_rect):
    return player_rect.colliderect(enemy_rect)

def game_over():
    over_font = pygame.font.Font('freesansbold.ttf', 64)
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    WIN.blit(over_text, (WIDTH // 6, HEIGHT // 3))

    # Restart button
    button_font = pygame.font.Font('freesansbold.ttf', 32)
    restart_text = button_font.render("Restart", True, (255, 255, 255))
    restart_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2, 150, 50)
    pygame.draw.rect(WIN, (0, 0, 255), restart_rect)
    WIN.blit(restart_text, (restart_rect.x + 20, restart_rect.y + 10))

    pygame.display.update()
    return restart_rect

def enemy_movement():
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4 * enemy_speed_factor
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= WIDTH - 64:
            enemyX_change[i] = -4 * enemy_speed_factor
            enemyY[i] += enemyY_change[i]

def bullet_movement(RED_BULLET):
    global score
    bullet_to_remove = []

    for bullet in RED_BULLET:
        bullet.y -= BULLET_VEL
        if bullet.y < 0:
            bullet_to_remove.append(bullet)
        else:
            for i in range(num_of_enemies):
                enemy_rect = pygame.Rect(enemyX[i], enemyY[i], 64, 64)
                if enemy_rect.colliderect(bullet):
                    bullet_to_remove.append(bullet)
                    score += 1
                    respawn_enemy(i)
                    break

    RED_BULLET[:] = [bullet for bullet in RED_BULLET if bullet not in bullet_to_remove]

def character_movement(keys, blue):
    if keys[pygame.K_LEFT] and blue.x > vel:
        blue.x -= vel
    if keys[pygame.K_RIGHT] and blue.x < WIDTH - s1 - vel:
        blue.x += vel
    if keys[pygame.K_UP] and blue.y > vel:
        blue.y -= vel
    if keys[pygame.K_DOWN] and blue.y < HEIGHT - s2 - vel:
        blue.y += vel

def game_window(RED_BULLET, blue):
    WIN.blit(bg, (0, 0))
    WIN.blit(BLUE, (blue.x, blue.y))
    for i in range(num_of_enemies):
        WIN.blit(enemyImg[i], (enemyX[i], enemyY[i]))

    for bullet in RED_BULLET:
        pygame.draw.rect(WIN, (255, 255, 0), bullet)
    show_score(10, 10)
    pygame.display.update()

def main():
    global score, enemyX, enemyY, enemyX_change, enemyY_change, num_of_enemies
    blue = pygame.Rect(210, 480, s1, s2)
    run = True
    game_over_displayed = False
    restart_rect = None

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over_displayed:
                    bullet = pygame.Rect(blue.x + blue.width // 2 - 5, blue.y, 10, 15)
                    RED_BULLET.append(bullet)
                    bullet_sound.play()
            if event.type == pygame.MOUSEBUTTONDOWN and game_over_displayed:
                if restart_rect and restart_rect.collidepoint(event.pos):
                    # Reset game variables
                    score = 0
                    RED_BULLET.clear()
                    for i in range(num_of_enemies):
                        respawn_enemy(i)
                    blue = pygame.Rect(210, 480, s1, s2)
                    game_over_displayed = False

        keys = pygame.key.get_pressed()
        if not game_over_displayed:
            character_movement(keys, blue)
            enemy_movement()
            bullet_movement(RED_BULLET)

            player_rect = pygame.Rect(blue.x, blue.y, s1, s2)
            for i in range(num_of_enemies):
                enemy_rect = pygame.Rect(enemyX[i], enemyY[i], 64, 64)
                if is_collision(player_rect, enemy_rect):
                    game_over_displayed = True
                    restart_rect = game_over()
                    break

            if not game_over_displayed:
                game_window(RED_BULLET, blue)

    pygame.quit()

if __name__ == "__main__":
    main()
