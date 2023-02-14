# Libraries
from pygame import *
import sys
import os

# Initializing pygame
init()

## ----------------------# definitions #-------------------------- ##
# Resolution for pygame window
(width, height) = (1200, 700)

# Lists for positions and speed -------- ballSpeedDiff for ball speed calculations
ballPos = [600, 10]
RstickPos = [1100, 300]
LstickPos = [100, 300]
ballSpeed = [-5, -5]
ballSpeedDiff = 0
stickSpeed = 7

# Scores integer declaration
ScoreR = 0
ScoreL = 0

# Used for detecting the start menu or singlePlayer or multiPlayer
Players = 0

# All boolen needed for movement detection, and ShowText to make text active or inactive
GoUpR = False
GoDownR = False
GoUpL = False
GoDownL = False
ReleaseBall = False
ShowText = True

# Fonts used for text 
font1 = font.Font("..\Assets\SnackerComic_PerosnalUseOnly.ttf", 30)
font2 = font.Font("..\Assets\ALBAS___.TTF", 90)
fontScore = font.Font("..\Assets\ALBAS___.TTF", 150)

# Declaring audio files for sound effects
ScoreBeeb = mixer.Sound(os.path.join("..\Assets\GoalBeeb.wav"))
StickCollide = mixer.Sound(os.path.join("..\Assets\StickCollide.wav"))
WallCollide = mixer.Sound(os.path.join("..\Assets\WallCollide.wav"))
## ------------- optional for background music ------------------##
#mixer.music.load(os.path.join("..\Assets\PongBackgroundMusic.wav"))
#mixer.music.play(-1)
#mixer.music.set_volume(0.02) 

# Intializing the FPS for the game (Frame Per Second)
FPS = time.Clock()

# Colors Definitions
White = (255, 255, 255)
Black = (0, 0, 0)
Blue = (0, 0, 255)
Red = (255, 50, 50)
Green = (50, 255, 50)

# Pygame Screen setUp ---- icon, screen and title
Icon = image.load("..\Assets\PongIcon.png")
screen = display.set_mode((width, height))
display.set_caption(" Pong ")
display.set_icon(Icon)
display.flip()


## ----------------------------- ##
## ------ first function ------- ##
## ----------------------------- ##
# Update function to handle everything needs to be updated every frame (60 time per second)
def update(ballSpeed):
## ----- globals ----- ##
    global GoUpR
    global GoDownR
    global GoUpL
    global GoDownL    
    global ReleaseBall
    global ShowText
    global ScoreR
    global ScoreL
    global Players
    global ballSpeedDiff
## ----- globals ----- ##
    
# Setting ballPosition and add speed to the ball
    if ReleaseBall:
        ballPos[0] += ballSpeed[0]
        ballPos[1] += ballSpeed[1]
    else:
        ballPos[0] = width/2
        ballPos[1] = height/2

# Handle detecting goals, adding scores and play goals sound
    if ballPos[0] < 10:
        mixer.Sound.play(ScoreBeeb)
        ScoreR += 1
        ReleaseBall = False
        ballSpeed = [-5, -5]
        ballSpeedDiff = 0
    elif ballPos[0] > (width - 10):
        mixer.Sound.play(ScoreBeeb)
        ScoreL += 1
        ReleaseBall = False
        ballSpeed = [5, -5]
        ballSpeedDiff = 0

# Handle ball collisions with the wall
    if ballPos[1] < 20 or ballPos[1] > (height - 20):
        mixer.Sound.play(WallCollide)
        ballSpeed[1] *= -1

# Detecting if it's single player or multiplayer and handle input for sticks movement
## -------- handle two players input -------- ##
    if Players == 2:
        if GoUpR:
            RstickPos[1] -= stickSpeed
        elif GoDownR:
            RstickPos[1] += stickSpeed
        if GoUpL:
            LstickPos[1] -= stickSpeed
        elif GoDownL:
            LstickPos[1] += stickSpeed
## -------- handle one player input and CPU player -------- ##
    elif Players == 1:
        if GoUpR:
            RstickPos[1] -= stickSpeed
        elif GoDownR:
            RstickPos[1] += stickSpeed
        if LstickPos[1] + 30 > ballPos[1]:
            LstickPos[1] -= stickSpeed + 1
        elif LstickPos[1] + 70 < ballPos[1]:
            LstickPos[1] += stickSpeed + 1     
        
# Handle sticks' position limit to stay in the pygame window
    if RstickPos[1] > (height - 110):
        RstickPos[1] = (height - 110)
    elif RstickPos[1] < 10:
        RstickPos[1] = 10
    if LstickPos[1] > (height - 110):
        LstickPos[1] = (height - 110)
    elif LstickPos[1] < 10:
        LstickPos[1] = 10     


# Input data handler
    for Event in event.get():
        if Event.type == QUIT:
            quit()        
        if Event.type == KEYDOWN:
            if Event.key == K_ESCAPE:
                quit()
            if Event.key == K_UP:
                GoUpR = True
            if Event.key == K_DOWN:
                GoDownR = True
            if Event.key == K_w:
                GoUpL = True
            if Event.key == K_s:
                GoDownL = True                
            if Event.key == K_SPACE:
                ReleaseBall = True 
                ShowText = False
                
        if Event.type == KEYUP:
            if Event.key == K_UP:
                GoUpR = False
            if Event.key == K_DOWN:
                GoDownR = False
            if Event.key == K_w:
                GoUpL = False
            if Event.key == K_s:
                GoDownL = False    
    
    return ScoreR, ScoreL


## ----------------------------- ##
## ------ second function ------- ##
## ----------------------------- ##
# Function to draw graphics in the game screen and handle some related things 
def graphics(ShowText):
## ----- globals ----- ##
    global Players
    global ballSpeedDiff
## ----- globals ----- ##
    
# Declaring variable stores the return values from the first function to use them in the second function
    scores = update(ballSpeed)

# Filling screen with white color every frame to update the graphics 
    screen.fill(White)
    
# Detecting if the user still in the main menu and handle the graphics 
    if Players == 0:
        ## single player button ##
        Single = draw.rect(screen, Black, Rect(width/2.2 - 45, 350, 180, 80), 4, 4)
        ## multi player button ##
        Multi = draw.rect(screen, Black, Rect(width/2.2 - 45, 500, 180, 80), 4, 4)
        
        ## stores mouse pos. in variables ## 
        MouseX, MouseY = mouse.get_pos()
        ## drawing a small rec. to handle mouse collision detection ##
        MouseRect = draw.rect(screen, Black, Rect(MouseX, MouseY, 1, 1), 3, 4)
        
        
        ## Change button color on Mouse collision ##                    ##
        if Single.colliderect(MouseRect):                               ##
            SingleText = font1.render(" Single Player ", True, Blue)    ##
        else:                                                           ##
            SingleText = font1.render(" Single Player ", True, Black)   ##
        if Multi.colliderect(MouseRect):                                ##
            MultiText = font1.render(" Multiplayer ", True, Blue)       ##
        else:                                                           ##
            MultiText = font1.render(" Multiplayer ", True, Black)      ##
        ## Change button color on Mouse collision ##                    ##
        
        ## check which button clicked with the mouse ## 
        if mouse.get_pressed()[0]:
            if Single.colliderect(MouseRect):
                Players = 1
            elif Multi.colliderect(MouseRect):
                Players = 2        
        
        ## put the main menu text to the screen ##               ##
        SingleTextRect = SingleText.get_rect()                   ##
        SingleTextRect.center = (width/2.2 + 45, 390)            ##
        MultiTextRect = MultiText.get_rect()                     ##
        MultiTextRect.center = (width/2.2 + 45, 540)             ##
                                                                 ##
        Title = font2.render(" Pong Game ", True, Black)         ##
        TitleTextRect = Title.get_rect()                         ##
        TitleTextRect.center = (width/2.2 + 45, 180)             ##
                                                                 ##
        screen.blit(SingleText, SingleTextRect)                  ##
        screen.blit(MultiText, MultiTextRect)                    ##
        screen.blit(Title, TitleTextRect)                        ##
        ## put the main menu text to the screen ##               ##

    else:
# Detecting if it's single or multi player and handle their text
        ## this means the game didn't start ## 
        if ShowText:
            if Players == 1:
                RText = font1.render(" Use UP and DOWN to move ", True, Black)
                RTextRect = RText.get_rect()
                RTextRect.center = (width/1.4, height/2) 
            elif Players == 2:
                RText = font1.render(" Use UP and DOWN to move ", True, Black)
                RTextRect = RText.get_rect()
                RTextRect.center = (width/1.4, height/2)                
                LText = font1.render(" Use W and S to move", True, Black)
                LTextRect = LText.get_rect()
                LTextRect.center = (width/3.5, height/2)   
                
                screen.blit(LText, LTextRect)
            screen.blit(RText, RTextRect)
        ## this handle the scores text ##
        else:
            R_score = fontScore.render(str(scores[0]), True, Blue)
            R_score.set_alpha(75)
            R_scoreTextRect = R_score.get_rect()
            R_scoreTextRect.center = (width/1.45, height/2) 
            L_score = fontScore.render(str(scores[1]), True, Red)
            L_score.set_alpha(75)
            L_scoreTextRect = L_score.get_rect()
            L_scoreTextRect.center = (width/3.9, height/2)         
            
            screen.blit(R_score, R_scoreTextRect)
            screen.blit(L_score, L_scoreTextRect)    
       
# Wall and Edges area drawing design
        upWall = draw.rect(screen, Black, Rect(-10, -10, width + 15, 20))
        downWall = draw.rect(screen, Black, Rect(-10, height - 10, width + 10, 20))
        
        for dots in range(20):
            dotedLine = draw.rect(screen, Black, Rect(width - 5, -20 + dots*40, 7, 15))
        for dots in range(20):
            dotedLine = draw.rect(screen, Black, Rect(-2, -20 + dots*40, 7, 15))        
        
# ball and sticks design drawing 
        TheBall = draw.circle(screen, Black, ballPos, 8, 0)
        RStick = draw.rect(screen, Black, Rect(RstickPos[0], RstickPos[1], 10, 100), 0, 4)
        LStick = draw.rect(screen, Black, Rect(LstickPos[0], LstickPos[1], 10, 100), 0, 4)
        
# ------------------------------------------------------------------------------------ #
# Handle ball collission with sticks and increase ball speed and handle it's direction #
# ------------------------------------------------------------------------------------ #
        if TheBall.colliderect(RStick):
            mixer.Sound.play(StickCollide)
            if ballPos[1] > RstickPos[1] and ballPos[1] <= RstickPos[1] + 20:
                if ballSpeedDiff > 0:
                    ballSpeedDiff *= -1
                ballSpeedDiff -= 0.15
                ballSpeed[0] = -5 + ballSpeedDiff
                ballSpeed[1] = -5 + ballSpeedDiff
            elif ballPos[1] > RstickPos[1] + 20 and ballPos[1] <= RstickPos[1] + 40:
                if ballSpeedDiff > 0:
                    ballSpeedDiff *= -1
                ballSpeedDiff -= 0.15
                ballSpeed[0] = -7 + ballSpeedDiff
                ballSpeed[1] = -3 + ballSpeedDiff
            elif ballPos[1] > RstickPos[1] + 40 and ballPos[1] <= RstickPos[1] + 60:
                if ballSpeedDiff > 0:
                    ballSpeedDiff *= -1                
                ballSpeedDiff -= 0.15
                ballSpeed[0] = -10 + ballSpeedDiff
                ballSpeed[1] = 0
            elif ballPos[1] > RstickPos[1] + 60 and ballPos[1] <= RstickPos[1] + 80:
                if ballSpeedDiff > 0:
                    ballSpeedDiff *= -1                
                ballSpeedDiff -= 0.15
                ballSpeed[0] = -7 + ballSpeedDiff
                ballSpeed[1] = 3 - ballSpeedDiff
            elif ballPos[1] > RstickPos[1] + 80 and ballPos[1] <= RstickPos[1] + 100:
                if ballSpeedDiff > 0:
                    ballSpeedDiff *= -1                               
                ballSpeedDiff -= 0.15
                ballSpeed[0] = -5 + ballSpeedDiff
                ballSpeed[1] = 5 - ballSpeedDiff
        
        if TheBall.colliderect(LStick): 
            mixer.Sound.play(StickCollide)
            if ballPos[1] > LstickPos[1] and ballPos[1] <= LstickPos[1] + 20:
                if ballSpeedDiff < 0:
                    ballSpeedDiff *= -1
                ballSpeedDiff += 0.15
                ballSpeed[0] = 5 + ballSpeedDiff
                ballSpeed[1] = -5 - ballSpeedDiff
            elif ballPos[1] > LstickPos[1] + 20 and ballPos[1] <= LstickPos[1] + 40:
                if ballSpeedDiff < 0:
                    ballSpeedDiff *= -1
                ballSpeedDiff += 0.15
                ballSpeed[0] = 7 + ballSpeedDiff
                ballSpeed[1] = -3 - ballSpeedDiff
            elif ballPos[1] > LstickPos[1] + 40 and ballPos[1] <= LstickPos[1] + 60:
                if ballSpeedDiff < 0:
                    ballSpeedDiff *= -1
                ballSpeedDiff += 0.15          
                ballSpeed[0] = 10 + ballSpeedDiff
                ballSpeed[1] = 0
            elif ballPos[1] > LstickPos[1] + 60 and ballPos[1] <= LstickPos[1] + 80:
                if ballSpeedDiff < 0:
                    ballSpeedDiff *= -1
                ballSpeedDiff += 0.15
                ballSpeed[0] = 7 + ballSpeedDiff
                ballSpeed[1] = 3 + ballSpeedDiff
            elif ballPos[1] > LstickPos[1] + 80 and ballPos[1] <= LstickPos[1] + 100:
                if ballSpeedDiff < 0:
                    ballSpeedDiff *= -1
                ballSpeedDiff += 0.15
                ballSpeed[0] = 5 + ballSpeedDiff
                ballSpeed[1] = 5 + ballSpeedDiff 
# ------------------------------------------------------------------------------------ #
# Handle ball collission with sticks and increase ball speed and handle it's direction #
# ------------------------------------------------------------------------------------ #
    
    # update the display
    display.update()   
    # setting the FPS to 60
    FPS.tick(60)  
    

# Infinity loop to call functions (ness
while True:
    graphics(ShowText)