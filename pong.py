#!/usr/bin/python3.7

import time
import math
import random

import contextlib
with contextlib.redirect_stdout(None): import pygame

#Helper functions
def resetBall():
    ball['rect'].x = 790
    ball['rect'].y = 440
    ball['vel'][0] = genSpeed()
    ball['vel'][1] = genSpeed()

def genSpeed():
    if random.randint(0, 2) :
        return random.randint(-9, -5)
    return random.randint(4, 8)

#Set up the playing window
pygame.init()

#Initialize display
pygame.display.set_caption("PONG")
screen = pygame.display.set_mode((1600, 900))#, pygame.FULLSCREEN)
surf = pygame.display.get_surface()
w, h = surf.get_size()

#Initialize font
pygame.font.init()
title_text = pygame.font.Font('./Sansation-Bold.ttf', 150)
subtitle_text = pygame.font.Font('./Sansation-Regular.ttf', 50)
score_text = pygame.font.Font('./Sansation-Regular.ttf', 50)
text_color = pygame.Color(255, 255, 255, 255)

#Set the paddle movement speed
move_speed = 9

#Initializing paddles
paddles = [
    pygame.Rect(20, 300, 20, 200),
    pygame.Rect(1560, 300, 20, 200)
]
paddle_color = pygame.Color(255, 255, 255, 255)

#Initializes the ball
ball = {'rect': pygame.Rect(790, 440, 20, 20),
        'vel': [genSpeed(), genSpeed()],
        'color': pygame.Color(255, 255, 255, 255)}

#Initializes the map (0 is the ceiling, 1 is the floor, 2 is the center line
map_rects = [pygame.Rect(0, 0, 1600, 15),
             pygame.Rect(0, 885, 1600, 15),
             pygame.Rect(795, 0, 10, 900)]
map_color = pygame.Color(255, 255, 255, 255)

#Other variables
keys_pressed = set()
done = False
last = 0
p1_score = 0
p2_score = 0
won = "Player 0"
bounded = True
space_held = False

state = "title"

#Main game loop
while not done:
    #Sets max refresh rate to 60 frames/sec
    while time.time() - last < 1/60: pass
    last = time.time()

    #Getting user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            keys_pressed.add(event.key)
        if event.type == pygame.KEYUP:
            keys_pressed.remove(event.key)

    #State-specific game logic
    if state == "title":
        #If the player wants to play a game
        if pygame.K_RETURN in keys_pressed:
            state = "game"
        if pygame.K_i in keys_pressed:
            state = "instr"

        #Drawing the title screen
        surf.fill((64, 64, 96))
        textsurf = pygame.font.Font.render(title_text, "PONG", True, text_color)
        screen.blit(textsurf, (600, 200))
        textsurf = pygame.font.Font.render(subtitle_text, "By: Ryan Houck", True, text_color)
        screen.blit(textsurf, (630, 350))
        textsurf = pygame.font.Font.render(subtitle_text, "Please press Enter to start", True, text_color)
        screen.blit(textsurf, (525, 600))
        textsurf = pygame.font.Font.render(subtitle_text, "(Or i for instructions)", True, text_color)
        screen.blit(textsurf, (580, 675))

    if state == "instr":
        #If the player wants to go back to the title screen
        if pygame.K_BACKSPACE in keys_pressed:
            state = "title"

        #Drawing the title screen
        surf.fill((64, 64, 96))
        textsurf = pygame.font.Font.render(subtitle_text, "Player 1: Up='W', Down='S'", True, text_color)
        screen.blit(textsurf, (525, 200))
        textsurf = pygame.font.Font.render(subtitle_text, "Player 2: Up=UP, Down=DOWN", True, text_color)
        screen.blit(textsurf, (450, 300))
        textsurf = pygame.font.Font.render(subtitle_text, "SPACE: Turn off bounding (in-game)", True, text_color)
        screen.blit(textsurf, (390, 400))
        textsurf = pygame.font.Font.render(subtitle_text, "ESC: Exit the game", True, text_color)
        screen.blit(textsurf, (575, 500))
        textsurf = pygame.font.Font.render(subtitle_text, "You may press BACKSPACE to go back to the title screen", True, text_color)
        screen.blit(textsurf, (150, 700))



    if state == "game":
        #Updating game logic
        #Update paddle 0 location
        if pygame.K_w in keys_pressed:
            paddles[0].y -= move_speed
        if pygame.K_s in keys_pressed:
            paddles[0].y += move_speed

        #Update paddle 1 location
        if pygame.K_UP in keys_pressed:
            paddles[1].y -= move_speed
        if pygame.K_DOWN in keys_pressed:
            paddles[1].y += move_speed

        for paddle in paddles:
            if paddle.y < (0, 15)[bounded]:
                paddle.y = (0, 15)[bounded]
            if paddle.y > (700, 685)[bounded]:
                paddle.y = (700, 685)[bounded]

        if pygame.K_SPACE in keys_pressed and space_held == False:
            if(bounded):
                bounded = False
                map_color = pygame.Color(122, 122, 122, 255)
            else:
                bounded = True
                map_color = pygame.Color(255, 255, 255, 255)
        
        #Update ball location
        ball['rect'].x += ball['vel'][0]
        ball['rect'].y += ball['vel'][1]

        collided=False
        #Checking paddle collision
        if paddles[0].colliderect(ball['rect']):
            ball['rect'].x = 40
            collided = True
        elif paddles[1].colliderect(ball['rect']):
            ball['rect'].x = 1540
            collided = True

        #If the ball collided, change directions and speed up (so long as it's within a safe range)
        if collided == True:
            if ball['vel'][0] * 1.1 < 25 and ball['vel'][0] * 1.1 > -25:
                ball['vel'][0] *= -1.1
            else:
                ball['vel'][0] *= -1

            if ball['vel'][1] * 1.1 < 15 and ball['vel'][1] * 1.1 > -15:
                ball['vel'][1] *= 1.1

        #Checking map collision
        if bounded == True and map_rects[0].colliderect(ball['rect']):
            ball['rect'].y = 15
            ball['vel'][1] *= -1
        if bounded == True and map_rects[1].colliderect(ball['rect']):
            ball['rect'].y = 865
            ball['vel'][1] *= -1

        #Checking ball wrap-around
        if ball['rect'].y < -20:
            ball['rect'].y = 900
        if ball['rect'].y > 900:
            ball['rect'].y = -20

        #Checking for scoring
        if ball['rect'].x <= -20:
            resetBall()
            p2_score += 1
        if ball['rect'].x >= 1600:
            resetBall()
            p1_score += 1

        if p1_score >= 11:
            won = "Player 1"
            state="endscreen"
        elif p2_score >= 11:
            won = "Player 2"
            state="endscreen"

        #Drawing
        surf.fill((64, 64, 96))
        for rect in map_rects:
            pygame.draw.rect(surf, map_color, rect)
        for paddle in paddles:
            pygame.draw.rect(surf, paddle_color, paddle)
        pygame.draw.rect(surf, ball['color'], ball['rect'])
        textsurf = pygame.font.Font.render(score_text, str(p1_score), True, text_color)
        screen.blit(textsurf, (375, 100))
        textsurf = pygame.font.Font.render(score_text, str(p2_score), True, text_color)
        screen.blit(textsurf, (1175, 100))

    if state == "endscreen":
        #If the player wants to start a new game
        if pygame.K_RETURN in keys_pressed:
            p1_score = 0
            p2_score = 0
            paddles[0].x = 20
            paddles[0].y = 300
            paddles[1].x = 1560
            paddles[1].y = 300
            won = "Player 0"
            state = "game"
            
        #Drawing endscreen
        surf.fill((64, 64, 96))
        textsurf = pygame.font.Font.render(subtitle_text, str(won + " has won!"), True, text_color)
        screen.blit(textsurf, (630, 350))
        textsurf = pygame.font.Font.render(subtitle_text, "Press Enter to start another game", True, text_color)
        screen.blit(textsurf, (450, 600))

    pygame.display.update()

    #Exit if escape is pressed
    if pygame.K_ESCAPE in keys_pressed:
        done = True

    if pygame.K_SPACE in keys_pressed:
        space_held = True
    else:
        space_held = False

pygame.quit()
