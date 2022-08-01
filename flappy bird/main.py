from asyncio.windows_utils import PipeHandle
import pygame
import sys
import random
from pygame.locals import *

# Global variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY =SCREENHEIGHT * 0.8
GAME_SPIRITES = {}
GAME_SOUNDS = {}
PLAYER = 'bird.png'
BACKGROUND = 'background.png'
PIPE = 'pipe.png'


def welcomeScreen():

    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT - GAME_SPIRITES['player'].get_height())/2
    
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on close button
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if user clicks space bar or up key, then start the game 
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPIRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPIRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPIRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                
def mainGame():
    score = 0
    playerx = int(SCREENHEIGHT/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # create 2 pipes for blitting
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    upperpipes = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[0]['y']}
    ]

    # list of lower pipes
    lowerpipes = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[1]['y']}
    ]
    
    pipeVelx = -4

    playerVely = -9
    playerMaxVely = 10
    playerMinVely = -8
    playerAccy = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False   # it is true only when the bird is flapping 

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVely = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        crashTest = isCollide(playerx, playery, upperpipes, lowerpipes)
        if crashTest:
            return

        playerMidPos = playerx + GAME_SPIRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidPos = pipe['x'] + GAME_SPIRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos +4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVely < playerMaxVely and not playerFlapped:
            playerVely += playerAccy
        
        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPIRITES['player'].get_height()
        playery = playery + min(playerVely, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            upperpipe['x'] += pipeVelx
            lowerpipe['x'] += pipeVelx
        
        # add a new pipe when first is about leave the screen
        if 0 < upperpipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperpipes.append(newPipe[0])
            lowerpipes.append(newPipe[1])


        # if pipe is out of the screen, remove it
        if upperpipes[0]['x'] < -GAME_SPIRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        # lets blit our sprites now
        SCREEN.blit(GAME_SPIRITES['background'], (0, 0))
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_SPIRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPIRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))

        SCREEN.blit(GAME_SPIRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPIRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPIRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPIRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPIRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)




def isCollide(playerx, playery, upperpipes, lowerpipes):
    if playery > GROUNDY -25 or playery < 0 :
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperpipes:
        pipeHeight = GAME_SPIRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and (abs(playerx - pipe['x']) < GAME_SPIRITES['pipe'][0].get_width())):
            GAME_SOUNDS['hit'].play()
            return True
    
    for pipe in lowerpipes:
        pipeHeight = GAME_SPIRITES['pipe'][0].get_height()
        playerHeight = GAME_SPIRITES['player'].get_height()
        if (playery + playerHeight > pipe['y'] and (abs(playerx - pipe['x']) < GAME_SPIRITES['pipe'][0].get_width())):
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    # Generate positions of two pipes
    pipeHeight = GAME_SPIRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPIRITES['base'].get_height() - 1.2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe =[
        {'x': pipex, 'y': -y1},  # upper pipe
        {'x': pipex, 'y': y2}   # lower pipe
    ]
    return pipe




if __name__ == "__main__":
    #this  willbe the main point from where game will start
    pygame.init()   # intialize pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by SAHIL')
    GAME_SPIRITES['numbers'] = (
        pygame.image.load('0.png').convert_alpha(),
        pygame.image.load('1.png').convert_alpha(),
        pygame.image.load('2.png').convert_alpha(),
        pygame.image.load('3.png').convert_alpha(),
        pygame.image.load('4.png').convert_alpha(),
        pygame.image.load('5.png').convert_alpha(),
        pygame.image.load('6.png').convert_alpha(),
        pygame.image.load('7.png').convert_alpha(),
        pygame.image.load('8.png').convert_alpha(),
        pygame.image.load('9.png').convert_alpha(),
    )

    GAME_SPIRITES['base'] = pygame.image.load('base.png').convert_alpha()
    GAME_SPIRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()  
    )

    # Game Sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('point.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('wing.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('swoosh.wav')

    GAME_SPIRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPIRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()
        

