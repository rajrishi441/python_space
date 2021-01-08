import pygame
import random
import math
from pygame import mixer

pygame.init()

# screen game

screen = pygame.display.set_mode((600, 600))
# TITLE

pygame.display.set_caption("SPACE")

# Player

playerimg = pygame.image.load("spaceship.png")
playerX = 275
playerY = 500
playerX_change = 0
playerY_change = 0


def player(x, y):
    # to drawn the space ship in the screen
    screen.blit(playerimg, (x, y))


# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 60

for i in range(number_of_enemies):
    enemyimg.append(pygame.image.load("monster.png"))
    enemyX.append(random.randint(0, 540))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(10)
    enemyY_change.append(30)


def enemy(x, y, i):
    # to drawn the space ship in the screen
    screen.blit(enemyimg[i], (x, y))


# backround
background = pygame.image.load("background1.png")

# background music
mixer.music.load("music.wav")
mixer.music.play(-1)

# bullet
# bullet_state = ready-> cant see the bullet   || fire-> can see the bullet

bulletimg = pygame.image.load("bullet.png")
bulletX = 100
bulletY = 500
bulletX_change = 0
bulletY_change = 60
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10


# game over

over = pygame.font.Font("freesansbold.ttf", 64)

def gameover():
    over = font.render("Game Over" , True, (255, 255, 255))
    screen.blit(over, (250, 250))

def scoredis(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 32, y + 32))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if distance <= 35:
        return True
    return False


# game loop

running = True

while running:
    # screen filling
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # key moments for <- and -> also when KEY is pressed and down

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                playerX_change += 5

            if event.key == pygame.K_LEFT:
                playerX_change -= 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX - 13
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            playerX_change = 0

    playerX += playerX_change

    # setting X boundries

    if playerX > 540:
        playerX = 540
    elif playerX <= 0:
        playerX = 0

    for i in range(number_of_enemies):

        # gameover

        if enemyY[i] > 480:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            gameover()
            break

        # Enemy movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] > 540:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]

        # collosion

        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("Explosion+1.wav")
            explosion_sound.play()
            bulletY = 500
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 540)
            enemyY[i] = random.randint(0, 150)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    scoredis(textX, textY)
    pygame.display.update()
