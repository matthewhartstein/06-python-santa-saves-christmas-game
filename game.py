import random
import math
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.jpg")

# Background music
mixer.music.load("music.wav")
mixer.music.set_volume(0.1)  # Set background music to 10% volume
mixer.music.play(-1)

# Set program title and icon
pygame.display.set_caption("The Best Game Ever!")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("player.png")
playerX = 375
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyType = []
num_enemies = 8

# Items
itemImg = []
itemX = []
itemY = []
itemX_change = []
itemY_change = []
num_items = 1

# Number of enemies
for i in range(num_enemies):
    # Bias towards Grinch (60% Grinch, 40% Elf)
    enemy_type = random.choices(["grinch.png", "elf.png"], weights=[0.6, 0.4], k=1)[0]
    enemyImg.append(pygame.image.load(enemy_type))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(0, 600))
    enemyX_change.append(2.5)
    enemyY_change.append(2.5)
    enemyType.append(enemy_type)

# Number of health items
for i in range(num_items):
    itemImg.append(pygame.image.load("cookie.png"))
    itemX.append(random.randint(0, 800))
    itemY.append(random.randint(0, 600))
    itemX_change.append(5)
    itemY_change.append(5)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)
textX = 690
textY = 575

# Health
health_value = 100
fontX = 10
fontY = 575

# Game over text
game_over = pygame.font.Font('freesansbold.ttf', 64)

def displayScore(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))

def displayHealth(x, y):
    health = font.render("Health: " + str(health_value), True, (0, 0, 0))
    screen.blit(health, (x, y))

def gameOver():
    text = game_over.render("GAME OVER!", True, (11, 102, 35))
    # Calculate text size and center it on 800x600 screen
    text_rect = text.get_rect(center=(800 // 2, 600 // 2))
    screen.blit(text, text_rect)
    mixer.music.stop()

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def cookie(x, y, i):
    screen.blit(itemImg[i], (x, y))

def isEnemyCollision(enemyX, enemyY, playerX, playerY, enemy_type):
    global health_value, score_value
    distance = math.sqrt((math.pow(enemyX - playerX, 2)) + (math.pow(enemyY - playerY, 2)))
    if distance < 20:
        # Only decrease health for Grinch collisions
        if enemy_type == "grinch.png":
            health_value -= 10
        # Only add score for Elf collisions
        if enemy_type == "elf.png":
            score_value += 10
        return True
    return False

def isItemCollision(itemX, itemY, playerX, playerY):
    global health_value
    distance = math.sqrt((math.pow(itemX - playerX, 2)) + (math.pow(itemY - playerY, 2)))
    if distance < 20:
        health_value = 100  # Restore health to 100
        return True
    return False

# Game loop
running = True
clock = pygame.time.Clock()  # For controlling frame rate

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_UP:
                playerY_change = -10
            if event.key == pygame.K_DOWN:
                playerY_change = 10

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                playerX_change = 0
                playerY_change = 0

    # Player movement with boundaries
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 750:
        playerX = 750
    if playerY <= 0:
        playerY = 0
    elif playerY >= 550:
        playerY = 550

    # Enemy and Item Movement
    for i in range(num_enemies):
        # Game over
        if health_value <= 0:
            for j in range(num_enemies):
                enemyY[j] = 2000
            for j in range(num_items):
                itemY[j] = 2000
            gameOver()
            break

        # Enemy movement
        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 2.5
        elif enemyX[i] >= 750:
            enemyX_change[i] = -2.5
        if enemyY[i] <= 0:
            enemyY_change[i] = 2.5
        elif enemyY[i] >= 550:
            enemyY_change[i] = -2.5

        # Enemy collision
        collision = isEnemyCollision(enemyX[i], enemyY[i], playerX, playerY, enemyType[i])
        if collision:
            attack_sound = mixer.Sound('attack.wav')
            attack_sound.set_volume(0.1)  # Set attack sound to 10% volume
            attack_sound.play()
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(0, 600)
        enemy(enemyX[i], enemyY[i], i)

        # Item movement
        if i < num_items:  # Ensure we don't access out-of-bounds indices
            itemX[i] += itemX_change[i]
            itemY[i] += itemY_change[i]

            if itemX[i] <= 0:
                itemX_change[i] = 5
            elif itemX[i] >= 750:
                itemX_change[i] = -5
            if itemY[i] <= 0:
                itemY_change[i] = 5
            elif itemY[i] >= 550:
                itemY_change[i] = -5

            # Item collision
            item_collision = isItemCollision(itemX[i], itemY[i], playerX, playerY)
            if item_collision:
                slurp = mixer.Sound('slurp.wav')
                slurp.set_volume(0.1)  # Set slurp sound to 10% volume
                slurp.play()
                itemX[i] = random.randint(0, 800)
                itemY[i] = random.randint(0, 600)
            cookie(itemX[i], itemY[i], i)

    player(playerX, playerY)
    displayScore(textX, textY)
    displayHealth(fontX, fontY)

    pygame.display.update()
    clock.tick(60)  # Limit to 60 FPS