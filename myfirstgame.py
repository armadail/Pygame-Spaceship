import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800,600))
#background
background = pygame.image.load('background.jpg')
#background music
mixer.music.load('background.mp3')
mixer.music.play(-1)
#icon and caption
pygame.display.set_caption("space invaders")
icon = pygame.image.load('spaceship.png')
#game over text
gameover_font = pygame.font.Font('Starjedi.ttf', 64)
def game_over_text():
    score = gameover_font.render("game over", True, (255,255,255))
    screen.blit(score, (200,250))

#score
score_value = 0
font = pygame.font.Font('Starjedi.ttf', 32)

textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x , y))

#player
playerImg = pygame.image.load('me.png')
pygame.display.set_icon(icon)
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0


def player(x,y):
    screen.blit(playerImg, (x, y))
#alien
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
number_of_aliens = 6
for i in range(number_of_aliens):
    alienImg.append(pygame.image.load('alien.png'))
    alienX.append(random.randint(0, 735))
    alienY.append(random.randint(50, 150))
    alienX_change.append(5)
    alienY_change.append(40)

def alien(x,y,i):
    screen.blit(alienImg[i], (x, y))

#bullet
#bullet_state: ready - cant see on screen
#              fire - bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
pygame.display.set_icon(icon)
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"


def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))
#collison
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY-bulletY, 2))
    if distance < 27:
        return True
    else:
        return False    

running  = True
while running:
    #screen.fill((255,0,0))
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -5
        if event.key == pygame.K_RIGHT:
            playerX_change = 5
        if event.key == pygame.K_UP:
            playerY_change = -5
        if event.key == pygame.K_DOWN:
            playerY_change = 5
        if event.key == pygame.K_SPACE:
            bullet_sound = mixer.Sound('laser.wav')
            bullet_sound.play() 
            bulletX = playerX
            bulletY = playerY
            fire_bullet(bulletX, bulletY)

    if event.type == pygame.KEYUP:
        playerX_change = 0
        playerY_change = 0        
        
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >=736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    #alien movement
    for i in range(number_of_aliens):
        #game Over
        if alienY[i] > 536:
            for j in range(number_of_aliens):
                alienY[j] = 2000
                game_over_text()
            break
 

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0 or alienX[i] >=736:
            alienX_change[i] = -(alienX_change[i])
            alienY[i] += alienY_change[i]
        #collision
        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play() 
            bullet_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 735)
            alienY[i] = random.randint(50, 150)

        alien(alienX[i], alienY[i], i)

    #bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
