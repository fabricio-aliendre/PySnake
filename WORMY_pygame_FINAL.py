#### PYGAME WORMY 2.0
#Fahim Haqyar ID: 20945337
#Charalampos Harris ID: 20959412
#Amar Manoj ID: 20914443
#Fabricio Aliendre  ID: 20896756

import random, pygame, sys
from pygame.locals import *

FPS = 6 #We changed the fps from 15 to 6, because as the levels of the game increase the fps of the game increase  (C.K)
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size." #The width of the cell was changed to 5 (C.K)
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size." #The wheight of the cell was changed to 10 (C.K)
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
ORANGE    = (255,  69,   0)   #New colour added (C.K)
BLUE      = (  0,   0, 255)   #New colour added (C.K)
GRAY      = (107, 107, 107)   #New colour added (C.K)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():    
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()  #This timer pauses a code from running for 1/x seconds (C.K)
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) 
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)  #This is function that will come handy to generate texts in future functions (C.K)
    pygame.display.set_caption('Wormy') #Names the program running 'Wormy' (C.K) 

    showStartScreen() #This shows the starting screen of the game (C.K)
    while True:  #This while loop will first run 'runGame()' function and then proceed to run 'showGameOverScreen()'. This will repeat until terminate() is called within any of the functions. (C.K)
        runGame()
        showGameOverScreen()

def runGame(): 
    # Set a random start point.
    startx = random.randint(6, CELLWIDTH - 8)# I changed the star point from 5 to 6 and the cell width from 7 to 8 (C.K)
    starty = random.randint(6, CELLHEIGHT - 7)# I changed the star point from 5 to 6 and the cell height from 6 to 7 (C.K)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT
    level = 1   #games starts at level 1 (FA) C.K

    # Start the apple in a random place. C.K
    apple = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop (C.K)
            if event.type == QUIT:  # If the event is a QUIT event, then we run terminate() function (C.K)
                terminate()
            elif event.type == KEYDOWN: #checks if the player pressed any key down (C.K)
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:  #If the worm is moving right, then the new direciton of wormy can't be left or else it will eat itself. (C.K) 
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT: #Repeats the same logic for every direction (C.K) 
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:#Repeats the same logic for every direction (C.K)
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:#Repeats the same logic for every direction (C.K)
                    direction = DOWN
                elif event.key == K_ESCAPE:  #ESC key will call terminate() function (C.K) 
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # proceed to call showGameOverScreen() function C.K
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over C.K
            
        if wormCoords[HEAD]['x'] == apple[ 'x'] and wormCoords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation() # set a new apple somewhere else
        else:
            del wormCoords[-1] # remove worm's tail segment (FA)
    

#Moves the worm by adding a segment (new head) in the direction it is moving (FA)
#'direction' determines where the new head of the snake will appear. (FA)
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}   #subtracts 1 only in x direction since it's relocating the snake's head up one unit on the game's coordinate system. (FA) 
            wormCoords.insert(0, newHead)     #This is what makes the worm move. That's why it repeats for all directions (FA)
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
            wormCoords.insert(0, newHead)
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}  
            wormCoords.insert(0, newHead)
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}  #adds 1 only in x direction since it's relocating the snake's head right one unit on the game's coordinate system. (FA)
            wormCoords.insert(0, newHead)  #this makes it move (FA)
         
        score = len(wormCoords) - 3  #Score is the number of items in the list 'wormCoords', which starts as 3 (FA)
        DISPLAYSURF.fill(BLACK)  #Background colour is black (FA)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple) #displays the apple on the game (FA)
        drawScore(score)  #calls for the current score to update live and showcase it in the game (FA)
        
        if level == 11:  # If the player beats level 10, following two functions wlil run (FA)
            showCongratulations() #similar to showGameOverScreen() except it congratulates the player (FA)
            runGame()            #runs the game again if the user presses any key(FA)
        elif (score) % 5 == 0:    #Every time the score is a multiple of 5 (FA)
            for num in range(5, 51, 5):  #It will check if the score is exactly one of the numbers of the generated by the range function (FA)
                if score/num == 1:
                    level = int(num/5) + 1  #if so, the level will be that number divided by 5. 1 is added since the starting level was 1. (FA)
                
        drawLevel(level)  #calls for the current level to update live and showcase it in the game (FA)
        pygame.display.update()  #Updates the game screen for every time the worm 'moves' (FA)
        FPSCLOCK.tick(FPS+3*level) #The while loop pauses for 1/x seconds before reading every item from the start of the loop (FA)
        #FPS + 3*level will make the pauses shorter as the levels increase.(FA)


def drawPressKeyMsg(): #Function projects a text on the game which reads 'Press a key to play' (FA)
    pressKeySurf = BASICFONT.render('Press a key to play', True, WHITE)  #Changed the text colour to white (FA)
    pressKeyRect = pressKeySurf.get_rect() #Generates the text box (FA)
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 60) #Location of the text box on the game's coordinate grid (FA)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect) #Displays the text box on the game screen (FA)
  
  
def drawEscapeMsg(): #Function projects a text on the game which reads 'or ESC to exit' (FA)                                    #ADDED ONE MORE FUNCTION
    pressEscapeSurf = BASICFONT.render('or ESC to exit', True, WHITE) #Same idea as drawPressKeyMsg (FA)
    pressEscapeRect = pressEscapeSurf.get_rect()  
    pressEscapeRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 35) #Located purposely right under drawPressKeyMsg (FA)
    DISPLAYSURF.blit(pressEscapeSurf, pressEscapeRect)
      

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        #This checks if the event type was updated to QUIT. If so, it exits the game (FA)
        terminate()
    #KeyUpEvents starts to recor the keys pressed at the moment the function is called (FA)
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    #If the latest key presed is ESC, then it will exit the game at any time.
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

#Amar (158-192)
def showStartScreen():
  titleFont = pygame.font.Font('freesansbold.ttf', 93) #the font was changed from 100 to 93 (AM)
  titleSurf1 = titleFont.render('Wormy!', True, WHITE, ORANGE) #the colors were changed to GRAY and ORANGE (AM)
  titleSurf2 = titleFont.render('Wormy!', True, BLUE) #the color was changed to BLUE (AM)
  
  degrees1 = 0
  degrees2 = 0
  while True:
    DISPLAYSURF.fill(BLACK)
    rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1) #The pygame.transform.rotate() function returns the new surface object, rotated by the desired degree. Here the image is "titleSurf1" and the degree you want it to be rotated is "degrees1" (AM)
    rotatedRect1 = rotatedSurf1.get_rect() #get_rect() function is used to return a rectangle covering the entire surface area (AM)
    rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)
    
    rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
    rotatedRect2 = rotatedSurf2.get_rect()
    rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)
    
    drawPressKeyMsg()

    if checkForKeyPress():
      pygame.event.get() #pygame.event.get() returns a list of all unprocessed events (AM)
      return
    pygame.display.update() #display.update() makes displau surface actually appear on the users monitor (AM)
    FPSCLOCK.tick(15)
    degrees1 += 5 #rotated by 5 degrees. it was changed to 5 degrees from 3 degrees (AM)
    degrees2 += 9 #rotated by 9 degrees. it was changed to 9 degrees from 7 degrees (AM)
    
def terminate():
    pygame.quit() #function is used to deactivate the pygame library (AM)
    sys.exit() #the exit funtion allows the user to exit from Python (AM)

def getRandomLocation(): #Produces a random integer WITHIN the games coordinate system. (AM)
  return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def showCongratulations():  #Similar structure to showGameOverScreen() (FA)
    CongratsFont = pygame.font.Font('freesansbold.ttf', 50)
    
    CongratsSurf = CongratsFont.render('Congratulations!', True, ORANGE)
    BeatSurf = CongratsFont.render('You Beat The Game', True, ORANGE)
    #Generates the texts (FA)
    CongratsRect = CongratsSurf.get_rect()
    BeatRect = BeatSurf.get_rect()
    #Generates the textboxes (FA)
    CongratsRect.midtop = (WINDOWWIDTH / 2, 100)
    BeatRect.midtop = (WINDOWWIDTH / 2, CongratsRect.height + 110)
    #Allocates the textboxes within the games' coordinate system (FA)
        
    DISPLAYSURF.blit(CongratsSurf, CongratsRect)
    DISPLAYSURF.blit(BeatSurf, BeatRect)
    #Calls for the textboxes to be displayed (FA)
    drawPressKeyMsg()   #this is the functions that shows the 'press any key' (FA)
    drawEscapeMsg()        
    drawThanksMsg()   #this is the functions that shows the 'Thanks for playing' (FA)
    pygame.display.update() 
    pygame.time.wait(500) # Games waits for 500ms before calling checkForKeyPress() (FA)
    checkForKeyPress() 
    
    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def showGameOverScreen(): # The screen shown after each match (FH)
    gameOverFont = pygame.font.Font('freesansbold.ttf', 200)
    # The font size was changed from 150 to 200
    gameSurf = gameOverFont.render('Try', True, ORANGE)
    overSurf = gameOverFont.render('Again', True, ORANGE)
    # Game Over message was changes to "Try Again" and font colour was changed from white to the new added colour
    # orange (FH)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 35)
    # Adjusts the "Boooo Loser" message grid (FH)
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    drawEscapeMsg()   #his is the functions that shows the 'or Press ESC to exit' (FA)
    pygame.display.update() 
    pygame.time.wait(500)
    # Games waits for 500ms before starting a new game to prevent any accidental game start function (FH)
    checkForKeyPress()  # clear out any key presses in the event queue (FH)
    # Displays the Press a Key to Play function (FH)

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue (FH)
            return

def drawScore(score):
    # Function for showing the score(FH)
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, RED)
    # Colour was changed from white to red (FH)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    # Adjusts the position and grid size of the score (FH)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    
def drawLevel(level):
    levelWRITE = BASICFONT.render('Level: %s' % (level), True, RED)
    levelRect = levelWRITE.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 220, 10)          
    DISPLAYSURF.blit(levelWRITE, levelRect)

def drawThanksMsg():  
    ThanksFont = pygame.font.Font('freesansbold.ttf', 35)
    ThanksSurf = ThanksFont.render('Thanks for playing', True, ORANGE)
    ThanksRect = ThanksSurf.get_rect()
    ThanksRect.topleft = (WINDOWWIDTH / 4, WINDOWHEIGHT*(2/3))
    DISPLAYSURF.blit(ThanksSurf, ThanksRect)

def drawWorm(wormCoords):
    # The drawWorm() function will draw a red box for each of the segments of the worm’s body. (FH)
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, RED, wormSegmentRect)
        # The colour for outer square was changed from dark green to red. (FH)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        # Coordinates for the inner square (FH)
        pygame.draw.rect(DISPLAYSURF, BLACK, wormInnerSegmentRect)
        # The colour for inner square was changed from light green to black. (FH)

def drawApple(coord):
    # The function for drawing an apple on the screen.
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, GREEN, appleRect)
    # The colour of the apple was changed from red to green. (FH)


def drawGrid():
    # This function is introduced just to make it easier to visualize the grid of cells, we call pygame.draw.line()
    # to draw out each of the vertical and horizontal lines of the grid. (FH)
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines (FH)
        pygame.draw.line(DISPLAYSURF, GRAY, (x, 0), (x, WINDOWHEIGHT))  #Changed colour from DARKGRAY to GRAY for better visibility
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines (FH)
        pygame.draw.line(DISPLAYSURF, GRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
#When the .py code is run, the main() function will be called(FH)