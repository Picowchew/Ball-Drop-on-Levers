# Ball Drop on Levers


# Setting up pygame
import pygame
pygame.init()


# Importing the math module
import math


# Setting up the screen
screenWidth = 1230
screenHeight = 750
screenDimensions = (screenWidth, screenHeight)
screen = pygame.display.set_mode(screenDimensions)
pygame.display.set_caption ("Ball Drop on Levers")


# Will be used to manage frame rate
clock = pygame.time.Clock()


# Loading the lever images
leverOne = pygame.image.load("Rectangle300x18.png")
leverTwo = pygame.image.load("Rectangle240x18.png")
leverThree = pygame.image.load("Rectangle180x18.png")


# Setting the initial number of levers placed down, the initial angles for the levers, and making a list of the levers touched by the ball
countLevers = 0

angle = 0
angleAddOne = 0
angleAddTwo = 0
angleAddThree = 0

leversTouched = []


# Defining some colours; the 'BLUE' and 'GREEN' are not the pure primary colours
BLUE   = (  50, 100, 255)
GRAY   = ( 130, 130, 130)
GREEN  = (   0, 255, 100)
RED    = ( 255,   0,   0)
WHITE  = ( 255, 255, 255)
YELLOW = ( 255, 255,   0)


# Setting the radius, colour, initial position, and initial vertical speed of the ball
radiusBall = 20
ballColour = RED
xBallInit = 600
yBallInit = 40
vSpeedInit = 3
xBall = xBallInit
yBall = yBallInit
vSpeed = vSpeedInit


# Setting the height of the score boxes
scoreBoxHeight = 45


# Setting the maximum y-coordinate of the ball
yBallMax = screenHeight - scoreBoxHeight - radiusBall


# Setting the inital round, score from the round, total score from the rounds, and total additional score
roundGame = 1
roundScore = 0
roundScoreTotal = 0
addScoreTotal = 0


# Setting up some audio files
finishedRound = pygame.mixer.Sound('FinishedRound.wav') # Source: https://www.youtube.com/watch?v=uetxqmMJtLw
finishedGame = pygame.mixer.Sound('FinishedGame.wav') # Source: https://www.youtube.com/watch?v=kgMToRGOAT4


# Instructions on how to play the game
print("\n\nWelcome to the game called 'Ball Drop on Levers'. The goal of this game is to receive as many points as possible. There are a total of 3 rounds.\
\n\nIn each round, you can click the mouse to place down a lever, for a total of three levers, starting with the longest lever and ending with the shortest lever. \
Left-clicking the mouse will later make the lever rotate CCW and right-clicking will later make the lever rotate CW. In addition, the ball can be moved left and right \
using the 'a' and 'd' keys, respectively. Afterwards, the 'space' key can be pressed to drop the ball and start the rotation of the levers.\
\n\nThe grid lines are meant to serve as an aid to help the user be able to produce consistent results from round to round, if desired.\
\n\nThe additional score is shown in the left-top corner. This is a culmulation from round to round. For each round, having the ball touch the shortest lever is worth \
70 points, medium-size lever is worth 50 points, and longest lever is worth 30 points.\
\n\nNote that in the case that the levers intersect or the ball intersects more than one lever, then the SMALLER LEVER WILL TAKE PRIORITY. Also note that if the ball \
falls upon a vertical lever, then the ball can fall down VERY FAST.")





# ----- Defining some functions and procedures -----

# This function returns the radius of the lever (the distance from the center to a vertex) and initial angles of the radii of the lever where the reference arm is (xCenterLever, yCenterLever) to (0, yCenterLever)
def determineRadiusLeverAndInitAngles(widthLever, heightLever, relatedAcuteAngle):

    radiusLever =  math.sqrt((widthLever/2)**2 + (heightLever/2)**2) # Pythagorean theorem

    # BL: Bottom-left vertex, BR: Bottom-right vertex, TR: Top-right vertex, TL: Top-left vertex
    initBLAngle = relatedAcuteAngle
    initBRAngle = 180 - relatedAcuteAngle
    initTRAngle = 180 + relatedAcuteAngle
    initTLAngle = 360 - relatedAcuteAngle
    
    return(radiusLever, initBLAngle, initBRAngle, initTRAngle, initTLAngle)



# This function returns the possible scores for each round
def scoresPerRound(scoreList):

    global scoreFont # Referencing 'scoreFont' in the global scope

    # Arguments are the text, smoothing out the characters of the text, and the colour of the text
    scoreHigh = scoreFont.render(str(scoreList[0]), True, RED)
    scoreMed = scoreFont.render(str(scoreList[1]), True, RED)
    scoreLow = scoreFont.render(str(scoreList[2]), True, RED)

    return(scoreHigh, scoreMed, scoreLow)



# This procedure displays a lever on the screen
def placeDownLever(leverImage, xCenterLever, yCenterLever):
    
    leverRect = leverImage.get_rect() # Getting the rectangle that covers the entire lever
    leverRect.center = (xCenterLever, yCenterLever) # Setting the center of the rectangle to the specified coordinates
    screen.blit(leverImage, leverRect) # Displaying the final lever in the correct position



# This function returns the additional angle that the lever turns
def angleAddLever(rotateDir):
    
    global angle # Referencing 'angle' in the global scope

    if rotateDir == "CCW":
        angleAdd = angle # CCW has a positive angle by convention
        
    elif rotateDir == "CW":
        angleAdd = -angle # CW has a negative angle by convention

    return(angleAdd)



# This procedure displays a rotated lever on the screen
def rotateLever(leverNum, angleAdd, xCenterLever, yCenterLever):

    rotLever = pygame.transform.rotate(leverNum, angleAdd) # Rotating the lever
    leverRect = rotLever.get_rect() # Getting the rectangle that covers the entire lever
    leverRect.center = (xCenterLever, yCenterLever) # Setting the center of the rectangle to the center of the lever (as previously determined by the mouse cursor)
    screen.blit(rotLever, leverRect) # Drawing the final rotated lever in the correct position



# This function returns the coordinates of the vertices and the min. and max. x and y values of the vertices of the lever
def determineLeverVerticesCoordinates(xCenterLever, yCenterLever, initBLAngle, initBRAngle, initTRAngle, initTLAngle, radiusLever, angleAdd):

    # The total angle of rotation of a radius of the lever is equal to its initial angle plus the additional angle of rotation
    totalBLAngle = initBLAngle + angleAdd
    totalBRAngle = initBRAngle + angleAdd
    totalTRAngle = initTRAngle + angleAdd
    totalTLAngle = initTLAngle + angleAdd
    
    
    # Horizontal components of the radii of the lever
    hCompBL = radiusLever*(math.cos(math.radians(totalBLAngle)))
    hCompBR = radiusLever*(math.cos(math.radians(totalBRAngle)))
    hCompTR = radiusLever*(math.cos(math.radians(totalTRAngle)))
    hCompTL = radiusLever*(math.cos(math.radians(totalTLAngle)))
    

    # Vertical components of the radii of the lever
    vCompBL = radiusLever*(math.sin(math.radians(totalBLAngle)))
    vCompBR = radiusLever*(math.sin(math.radians(totalBRAngle)))
    vCompTR = radiusLever*(math.sin(math.radians(totalTRAngle)))
    vCompTL = radiusLever*(math.sin(math.radians(totalTLAngle)))
    
    
    # Coordinates of the vertices of the lever
    xBL = xCenterLever - hCompBL
    yBL = yCenterLever + vCompBL
    
    xBR = xCenterLever - hCompBR
    yBR = yCenterLever + vCompBR
    
    xTR = xCenterLever - hCompTR
    yTR = yCenterLever + vCompTR

    xTL = xCenterLever - hCompTL
    yTL = yCenterLever + vCompTL
    
    
    # Min. and max. x values of the vertices of the lever
    xList = [xBL, xBR, xTR, xTL]
    xMin = min(xList)
    xMax = max(xList)

    
    # Min. and max. y values of the vertices of the lever
    yList = [yBL, yBR, yTR, yTL]
    yMin = min(yList)
    yMax = max(yList)
    
    
    return(xBL, yBL, xBR, yBR, xTR, yTR, xTL, yTL, xMin, xMax, yMin, yMax)



# This function returns the discriminant and the potential intersected side of the lever by the ball; determines if the ball potentially intersects the lever by returning the value of the discriminant
def determineIntersection(xVertexOne, yVertexOne, xVertexTwo, yVertexTwo, xVertexThree, yVertexThree, yMin, yMax):

    global radiusBall, xBall, yBall # Referencing 'radiusBall', 'xBall', and 'yBall' in the global scope
    
    if xBall <= xVertexTwo: # If the ball potentially intersects the left side of the lever

        if xVertexTwo - xVertexOne != 0: # Dividing by 0 is undefined
            slope = (yVertexTwo - yVertexOne)/(xVertexTwo - xVertexOne) # The slope of the side of the lever
            """
            Calculations:
            Equation of ball:             (x - xBall)**2 + (y - yBall)**2 == radiusBall**2              (1)
            Equation of side of lever:    y - yVertexTwo == slope*(x - xVertexTwo)                      (2)
            
           (2)    y == slope*x + (-slope*xVertexTwo + yVertexTwo)                                       (3)
           (1)    x**2 - 2*x*xBall + xBall**2 + y**2 - 2*y*yBall + yBall**2 == radiusBall**2
                  x**2 + (-2*xBall)*x + xBall**2 + y**2 - 2*y*yBall + yBall**2 - radiusBall**2 == 0     (4)
sub (3) in (4)    x**2 + (-2*xBall)*x + xBall**2 + (slope*x + (-slope*xVertexTwo + yVertexTwo))**2 - 2*(slope*x + (-slope*xVertexTwo + yVertexTwo))*yBall + yBall**2 - radiusBall**2 == 0
                  x**2 + (-2*xBall)*x + xBall**2 + (slope**2)*(x**2) + (2*slope*(-slope*xVertexTwo + yVertexTwo))*x + (-slope*xVertexTwo + yVertexTwo)**2 - (2*yBall*slope)*x - 2*yBall*(-slope*xVertexTwo + yVertexTwo) + yBall**2 - radiusBall**2 == 0
                 (1 + slope**2)*(x**2) + (-2*xBall + 2*slope*(-slope*xVertexTwo + yVertexTwo) - 2*yBall*slope)*x + (xBall**2 + (-slope*xVertexTwo + yVertexTwo)**2 - 2*yBall*(-slope*xVertexTwo + yVertexTwo) + yBall**2 - radiusBall**2) == 0
            """
            discr = (-2*xBall + 2*slope*(-slope*xVertexTwo + yVertexTwo) - 2*yBall*slope)**2 - 4*(1 + slope**2)*(xBall**2 + (-slope*xVertexTwo + yVertexTwo)**2 - 2*yBall*(-slope*xVertexTwo + yVertexTwo) + yBall**2 - radiusBall**2)

            return(discr, "left")
        else:
            return(-1, "left") # The discriminant is negative to let the ball fall straight down when the function is called
        

    elif xVertexTwo < xBall: # If the ball potentially intersects the right side of the lever
        if xVertexThree - xVertexTwo != 0:
            slope = (yVertexThree - yVertexTwo)/(xVertexThree - xVertexTwo)
            discr = (-2*xBall + 2*slope*(-slope*xVertexTwo + yVertexTwo) - 2*yBall*slope)**2 - 4*(1 + slope**2)*(xBall**2 + (-slope*xVertexTwo + yVertexTwo)**2 - 2*yBall*(-slope*xVertexTwo + yVertexTwo) + yBall**2 - radiusBall**2)
            return(discr, "right")
        else:
            return(-1, "right")



# This function returns the new x-coordinate and potential y-coordinates of the ball, if the ball intersects the lever
def determineBallStateIntersect(xVertexOne, yVertexOne, xVertexTwo, yVertexTwo, xVertexThree, yVertexThree, intersectedSideOfLever):

    global xBall, yBall # Referencing 'xBall' and 'yBall' in the global scope
    
    if intersectedSideOfLever == "left": # Different sides of the lever have different equations 
        
        xBallCalc = xBall - 3 # The ball's new x-coordinate is 3 units to the left; this is true for the top side of the lever and simplifies the process for the bottom side
        
        slope = (yVertexTwo - yVertexOne)/(xVertexTwo - xVertexOne) # The slope of the side of the lever
        
        """
        Calculations: # Determining the new yBall such that the ball and side of lever intersect at one point
        discr == 0
        (-2*xBallCalc + 2*slope*(-slope*xVertexTwo + yVertexTwo) - 2*yBallCalc*slope)**2 - 4*(1 + slope**2)*(xBallCalc**2 + (-slope*xVertexTwo + yVertexTwo)**2 - 2*yBallCalc*(-slope*xVertexTwo + yVertexTwo) + yBallCalc**2 - radiusBall**2) == 0
        (-2*xBallCalc + 2*slope*(-slope*xVertexTwo + yVertexTwo))**2 - 2*(-2*xBallCalc + 2*slope*(-slope*xVertexTwo + yVertexTwo))*(2*slope)*yBallCalc + (2*slope*yBallCalc)**2 - 4*(1 + slope**2)*(xBallCalc**2 + (-slope*xVertexTwo + yVertexTwo)**2 - radiusBall**2) - 4*(1 + slope**2)*(-2*yBallCalc*(-slope*xVertexTwo + yVertexTwo)) - 4*(1 + slope**2)*(yBallCalc**2) == 0
        (-2*(-2*xBallCalc + 2*slope*(-slope*xVertexTwo + yVertexTwo))*(2*slope))*yBallCalc + ((2*slope)**2)*(yBallCalc**2) - (4*(1 + slope**2)*(-2*(-slope*xVertexTwo + yVertexTwo)))*yBallCalc - (4*(1 + slope**2))*(yBallCalc**2) + (-2*xBallCalc + 2*slope*(-slope*xVertexTwo + yVertexTwo))**2 - 4*(1 + slope**2)*(xBallCalc**2 + (-slope*xVertexTwo + yVertexTwo)**2 - radiusBall**2) == 0
        ((2*slope)**2 - 4*(1 + slope**2))*(yBallCalc**2) + (-2*(-2*xBallCalc + 2*slope*(-slope*xVertexTwo + yVertexTwo))*(2*slope) - 4*(1 + slope**2)*(-2*(-slope*xVertexTwo + yVertexTwo)))*yBallCalc + ((-2*xBallCalc + 2*slope*(-slope*xVertexTwo + yVertexTwo))**2 - 4*(1 + slope**2)*(xBallCalc**2 + (-slope*xVertexTwo + yVertexTwo)**2 - radiusBall**2)) == 0
        """
    
        discrTwo = (-2*(-2*xBallCalc + 2*slope*(-slope*xVertexTwo + yVertexTwo))*(2*slope) - 4*(1 + slope**2)*(-2*(-slope*xVertexTwo + yVertexTwo)))**2 - 4*((2*slope)**2 - 4*(1 + slope**2))*((-2*xBallCalc + 2*slope*(-slope*xVertexTwo + yVertexTwo))**2 - 4*(1 + slope**2)*(xBallCalc**2 + (-slope*xVertexTwo + yVertexTwo)**2 - radiusBall**2))

        if 2*((2*slope)**2 - 4*(1 + slope**2)) != 0: # Denominator cannot equal 0
            yBallOne = (-(-2*(-2*xBallCalc + 2*slope*(-slope*xVertexTwo + yVertexTwo))*(2*slope) - 4*(1 + slope**2)*(-2*(-slope*xVertexTwo + yVertexTwo))) + math.sqrt(discrTwo))/(2*((2*slope)**2 - 4*(1 + slope**2)))
            yBallTwo = (-(-2*(-2*xBallCalc + 2*slope*(-slope*xVertexTwo + yVertexTwo))*(2*slope) - 4*(1 + slope**2)*(-2*(-slope*xVertexTwo + yVertexTwo))) - math.sqrt(discrTwo))/(2*((2*slope)**2 - 4*(1 + slope**2)))

        else:
            yBallOne = yBall
            yBallTwo = yBall

    elif intersectedSideOfLever == "right":

        xBallCalc = xBall + 3 # The ball's new x-coordinate is 3 units to the right; this is true for the top side of the lever and simplifies the process for the bottom side

        slope = (yVertexThree - yVertexTwo)/(xVertexThree - xVertexTwo)

        discrTwo = (-2*(-2*xBallCalc + 2*slope*(-slope*xVertexTwo + yVertexTwo))*(2*slope) - 4*(1 + slope**2)*(-2*(-slope*xVertexTwo + yVertexTwo)))**2 - 4*((2*slope)**2 - 4*(1 + slope**2))*((-2*xBallCalc + 2*slope*(-slope*xVertexTwo + yVertexTwo))**2 - 4*(1 + slope**2)*(xBallCalc**2 + (-slope*xVertexTwo + yVertexTwo)**2 - radiusBall**2))

        if 2*((2*slope)**2 - 4*(1 + slope**2)) != 0:
            yBallOne = (-(-2*(-2*xBallCalc + 2*slope*(-slope*xVertexTwo + yVertexTwo))*(2*slope) - 4*(1 + slope**2)*(-2*(-slope*xVertexTwo + yVertexTwo))) + math.sqrt(discrTwo))/(2*((2*slope)**2 - 4*(1 + slope**2)))
            yBallTwo = (-(-2*(-2*xBallCalc + 2*slope*(-slope*xVertexTwo + yVertexTwo))*(2*slope) - 4*(1 + slope**2)*(-2*(-slope*xVertexTwo + yVertexTwo))) - math.sqrt(discrTwo))/(2*((2*slope)**2 - 4*(1 + slope**2)))

        else:
            yBallOne = yBall
            yBallTwo = yBall
    
    if yBallOne > yBallTwo: # Ensuring that yBallOne <= yBallTwo
        temp = yBallOne
        yBallOne = yBallTwo
        yBallTwo = temp
    
    return(xBallCalc, yBallOne, yBallTwo)



# This function returns the new y-coordinate and vertical speed of the ball, if the ball does not intersect the lever
def determineBallStateNoIntersect():
    global vSpeed, yBall # Referencing 'vSpeed' and 'yBall' in the global scope

    vSpeedCalc = vSpeed # This may be overrided later in the function
    
    if vSpeed < 3: # The ball's vertical speed must be a positive value, so the ball moves down once it falls off the lever; if vSpeed is less than 3, then it is increased to 3 to make the ball fall faster
        vSpeedCalc = 3
        
    elif vSpeed > 10: # If vSpeed is greater than 10, then it is decreased to 10 to make the ball fall slower
        vSpeedCalc = 10
        
    yBallCalc = yBall + vSpeedCalc # The ball's vertical speed is initially 3; if the ball falls off a lever, then its vertical speed is equal to its final vertical speed when touching the lever (as long as the final vertical speed is not less than 3 or greater than 10)
    
    return(yBallCalc, vSpeedCalc)



# This function returns the new coordinates and vertical speed of the ball, if the ball is within range of the lever
def discrCases(xVertexOne, yVertexOne, xVertexTwo, yVertexTwo, xVertexThree, yVertexThree, xVertexFour, yVertexFour, intersectedSideOfLeverTop, intersectedSideOfLeverBot, discrTop, discrBot):

    global radiusBall, xBall, yBall, vSpeed  # Referencing 'radiusBall', 'xBall', 'yBall', and 'vSpeed' in the global scope

    xBallCalc = xBall # This may be overrided later in the function


    if discrTop >= 0 and discrBot >= 0: # This can happen if the ball is at a vertex of the lever

        xBallCalc, yBallOne, yBallTwo = determineBallStateIntersect(xVertexOne, yVertexOne, xVertexTwo, yVertexTwo, xVertexThree, yVertexThree, intersectedSideOfLeverTop) # The values are determined as if the ball only intersects the top side of the lever

        yBallCalc = round(yBallOne) # yBallCalc needs to be an integer in order for the ball to later be drawn
        vSpeedCalc = yBallCalc - yBall # vSpeedCalc is the change in the y-coordinate of the ball

        if yBall >= yBallCalc + radiusBall: # This overrides the previous calculated values if the ball moves up too much

            yBallCalc, vSpeedCalc = determineBallStateNoIntersect() # The same will happen as if the ball and side of lever do not intersect            

            xBallCalc = xBall # The new x-coordinate will be the same as its current value


    elif discrBot >= 0: # If the ball intersects the bottom side of the lever

        if (intersectedSideOfLeverBot == "left" and xBall + radiusBall >= xVertexOne and yBall - radiusBall >= yVertexOne) or (intersectedSideOfLeverBot == "right" and xBall - radiusBall <= xVertexThree and yBall - radiusBall >= yVertexThree): # If the ball is within range of the lever for either intersected side
       
            xBallCalc, yBallOne, yBallTwo = determineBallStateIntersect(xVertexOne, yVertexOne, xVertexFour, yVertexFour, xVertexThree, yVertexThree, intersectedSideOfLeverBot)
            yBallNoInt, vSpeedNoInt = determineBallStateNoIntersect()
            
            yBallCalc = round(max(yBallTwo, yBallNoInt)) # yBallCalc will be the greater one of yBallTwo and yBallNoInt
            vSpeedCalc = yBallCalc - yBall
            
            if yBallCalc == round(yBallNoInt):
                xBallCalc = xBall

        else: # The same will happen as if the ball and side of lever do not intersect

            yBallCalc, vSpeedCalc = determineBallStateNoIntersect()


    elif discrTop >= 0: # If the ball intersects the top side of the lever

        xBallCalc, yBallOne, yBallTwo = determineBallStateIntersect(xVertexOne, yVertexOne, xVertexTwo, yVertexTwo, xVertexThree, yVertexThree, intersectedSideOfLeverTop)

        yBallCalc = round(yBallOne)
        vSpeedCalc = yBallCalc - yBall

        if (yBall >= yBallCalc + radiusBall) or (intersectedSideOfLeverTop == "left" and yBallCalc + radiusBall - 5 >= yVertexOne) or (intersectedSideOfLeverTop == "right" and yBallCalc + radiusBall - 5 >= yVertexThree): # If the ball becomes out of range of the top of the lever; 5 was arbitrarily added to ensure the smoothness of the ball

            yBallCalc, vSpeedCalc = determineBallStateNoIntersect()

            xBallCalc = xBall


    else: # The ball and side of lever do not intersect

        yBallCalc, vSpeedCalc = determineBallStateNoIntersect()


    return(xBallCalc, yBallCalc, vSpeedCalc)



# This function returns the new coordinates and vertical speed of the ball
def determineBallState(xVertexOne, yVertexOne, xVertexTwo, yVertexTwo, xVertexThree, yVertexThree, xVertexFour, yVertexFour, xMin, xMax, yMin, yMax):

    global radiusBall, xBall  # Referencing 'radiusBall' and 'xBall' in the global scope

    xBallCalc = xBall # This may be overrided later in the function


    if (xMin - radiusBall - 5 <= xBall <= xMax + radiusBall + 5) and (yMin - radiusBall <= yBall <= yMax + radiusBall): # If the ball is within range of the lever; 5 was arbitrarily added to ensure the smoothness of the ball when falling off the lever (the roughness is due to the lever rotating while the ball is falling off)

        if yMin == yVertexOne: # If vertex one is at the top of the lever

            discrTop, intersectedSideOfLeverTop = determineIntersection(xVertexTwo, yVertexTwo, xVertexOne, yVertexOne, xVertexFour, yVertexFour, yMin, yMax)
            discrBot, intersectedSideOfLeverBot = determineIntersection(xVertexTwo, yVertexTwo, xVertexThree, yVertexThree, xVertexFour, yVertexFour, yMin, yMax)

            xBallCalc, yBallCalc, vSpeedCalc = discrCases(xVertexTwo, yVertexTwo, xVertexOne, yVertexOne, xVertexFour, yVertexFour, xVertexThree, yVertexThree, intersectedSideOfLeverTop, intersectedSideOfLeverBot, discrTop, discrBot)


        elif yMin == yVertexTwo: # If vertex two is at the top of the lever           

            discrTop, intersectedSideOfLeverTop = determineIntersection(xVertexThree, yVertexThree, xVertexTwo, yVertexTwo, xVertexOne, yVertexOne, yMin, yMax)
            discrBot, intersectedSideOfLeverBot = determineIntersection(xVertexThree, yVertexThree, xVertexFour, yVertexFour, xVertexOne, yVertexOne, yMin, yMax)

            xBallCalc, yBallCalc, vSpeedCalc = discrCases(xVertexThree, yVertexThree, xVertexTwo, yVertexTwo, xVertexOne, yVertexOne, xVertexFour, yVertexFour, intersectedSideOfLeverTop, intersectedSideOfLeverBot, discrTop, discrBot)


        elif yMin == yVertexThree: # If vertex three is at the top of the lever

            discrTop, intersectedSideOfLeverTop = determineIntersection(xVertexFour, yVertexFour, xVertexThree, yVertexThree, xVertexTwo, yVertexTwo, yMin, yMax)
            discrBot, intersectedSideOfLeverBot = determineIntersection(xVertexFour, yVertexFour, xVertexOne, yVertexOne, xVertexTwo, yVertexTwo, yMin, yMax)

            xBallCalc, yBallCalc, vSpeedCalc = discrCases(xVertexFour, yVertexFour, xVertexThree, yVertexThree, xVertexTwo, yVertexTwo, xVertexOne, yVertexOne, intersectedSideOfLeverTop, intersectedSideOfLeverBot, discrTop, discrBot)


        elif yMin == yVertexFour: # If vertex four is at the top of the lever

            discrTop, intersectedSideOfLeverTop = determineIntersection(xVertexOne, yVertexOne, xVertexFour, yVertexFour, xVertexThree, yVertexThree, yMin, yMax)
            discrBot, intersectedSideOfLeverBot = determineIntersection(xVertexOne, yVertexOne, xVertexTwo, yVertexTwo, xVertexThree, yVertexThree, yMin, yMax)

            xBallCalc, yBallCalc, vSpeedCalc = discrCases(xVertexOne, yVertexOne, xVertexFour, yVertexFour, xVertexThree, yVertexThree, xVertexTwo, yVertexTwo, intersectedSideOfLeverTop, intersectedSideOfLeverBot, discrTop, discrBot)

            
    else: # The ball and side of lever do not intersect

        yBallCalc, vSpeedCalc = determineBallStateNoIntersect()


    return(xBallCalc, yBallCalc, vSpeedCalc)





# ----- Setting up some values for each lever -----

# Setting up the width of the levers, height of the levers, and the related acute angle of the radii of the levers
widthLeverOne = 300
heightLeverOne = 18
relatedAcuteAngleOne = math.degrees(math.atan(math.fabs(heightLeverOne/2)/math.fabs(widthLeverOne/2)))

widthLeverTwo = 240
heightLeverTwo = 18
relatedAcuteAngleTwo = math.degrees(math.atan(math.fabs(heightLeverTwo/2)/math.fabs(widthLeverTwo/2)))

widthLeverThree = 180
heightLeverThree = 18
relatedAcuteAngleThree = math.degrees(math.atan(math.fabs(heightLeverThree/2)/math.fabs(widthLeverThree/2)))


# Determining the radii length of the levers and the initial angle of the radii
radiusLeverOne, initBLAngleOne, initBRAngleOne, initTRAngleOne, initTLAngleOne = determineRadiusLeverAndInitAngles(widthLeverOne, heightLeverOne, relatedAcuteAngleOne)
radiusLeverTwo, initBLAngleTwo, initBRAngleTwo, initTRAngleTwo, initTLAngleTwo = determineRadiusLeverAndInitAngles(widthLeverTwo, heightLeverTwo, relatedAcuteAngleTwo)
radiusLeverThree, initBLAngleThree, initBRAngleThree, initTRAngleThree, initTLAngleThree = determineRadiusLeverAndInitAngles(widthLeverThree, heightLeverThree, relatedAcuteAngleThree)





# ----- Main program loop -----

doneProgram = False # Variable that determines whether the user is done using the program
doneGame = False # Variable that determines whether the user is done playing the game
pressedSpaceKey = False # Variable that determines whether the user has pressed the space key for the round (to drop the ball)


# The main program loop runs indefinitely until the user is done using the program
while not doneProgram:
    
    # ----- Main Event Loop -----

    # User does an action
    for event in pygame.event.get():

        # If user closes the program
        if event.type == pygame.QUIT:

            # The main program loop gets exited
            doneProgram = True


        elif event.type == pygame.MOUSEMOTION:
            xMouse, yMouse = pygame.mouse.get_pos() # Getting the coordinates of the mouse cursor
        

        elif (event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3)) and (yBall == yBallInit): # If the mouse was left-clicked or right-clicked and the ball is at the top of the screen (before it is dropped)

            if countLevers == 0: # If 0 levers were previously placed down

                # The coordinates of the center of lever is the current coordinates of the mouse cursor
                xCenterLeverOne = xMouse
                yCenterLeverOne = yMouse

                countLevers += 1 # The number of levers placed down is now 1
                
                if event.button == 1:
                    rotateDirOne = "CCW" # The lever will rotate CCW if the mouse was left-clicked
                
                elif event.button == 3:
                    rotateDirOne = "CW" # The lever will rotate CW if the mouse was right-clicked
                    
            elif countLevers == 1: # If 1 lever was previously placed down

                xCenterLeverTwo = xMouse
                yCenterLeverTwo = yMouse

                countLevers += 1 # The number of levers placed down is now 2
                
                if event.button == 1:
                    rotateDirTwo = "CCW"
                
                elif event.button == 3:
                    rotateDirTwo = "CW"
                    
            elif countLevers == 2: # If 2 levers were previously placed down

                xCenterLeverThree = xMouse
                yCenterLeverThree = yMouse

                countLevers += 1 # The number of levers placed down is now 3

                if event.button == 1:
                    rotateDirThree = "CCW"
                
                elif event.button == 3:
                    rotateDirThree = "CW"

        
        elif event.type == pygame.MOUSEBUTTONDOWN and yBall >= yBallMax: # If the mouse was clicked and the ball is at the score boxes at the bottom of the screen

            if 1 <= roundGame <= 3:
                roundScoreTotal += roundScore # Updating the total score from the rounds

                finishedRound.play() # Play the finishedRound sound effect

                # Setting some variables back to their initial values
                xBall = xBallInit
                yBall = yBallInit
                vSpeed = vSpeedInit
                countLevers = 0
                angle = 0
                angleAddOne = 0
                angleAddTwo = 0
                angleAddThree = 0
                pressedSpaceKey = False

                leversTouched = [] # Clearing the list of the levers touched by the ball
                
                roundGame += 1 # Increasing the round of the game by 1
            
            if roundGame == 4:
                if doneGame == False:
                    finishedGame.play() # Play the finishedGame sound effect
                    doneGame = True # One of the functions of doneGame is to ensure that finishedGame will only play once




    
    # ----- Game Logic Code -----
    
    # Determining which keys are pressed down
    keys = pygame.key.get_pressed()


    if yBall == yBallInit: # If the ball is at the top of the screen (before it is dropped)
        
        if pressedSpaceKey == False: # If the user has not pressed the space key to drop the ball
            
            if keys[pygame.K_a] == True: # If the 'a' key is pressed/held down
                xBall -= 3 # The ball moves left 3 units

            if keys[pygame.K_d] == True: # If the 'd' key is pressed/held down
                xBall += 3 # The ball moves right 3 units

            if keys[pygame.K_SPACE] == True and countLevers == 3: # If the 'space' key is pressed down and 3 levers are already placed down on the screen

                yBall += vSpeed # The ball moves down by vSpeed units

                pressedSpaceKey = True # The user has now pressed the space key

        else:
            yBall, vSpeed = determineBallStateNoIntersect() # The ball will fall down


    elif yBall < yBallMax: # After the ball is dropped, before the ball reaches the score boxes at the bottom of the screen
        
        angle += 1 # Incrementing the angle of the lever
        if angle == 360: # Setting the angle back to 0 once a full revolution is reached
            angle = 0


        # Determining the additional angles that the levers turn
        angleAddOne = angleAddLever(rotateDirOne)
        angleAddTwo = angleAddLever(rotateDirTwo)
        angleAddThree = angleAddLever(rotateDirThree)


        # Determining the vertices of lever three, and then determining if and how the ball interacts with lever three
        xBLThree, yBLThree, xBRThree, yBRThree, xTRThree, yTRThree, xTLThree, yTLThree, xMinThree, xMaxThree, yMinThree, yMaxThree = determineLeverVerticesCoordinates(xCenterLeverThree, yCenterLeverThree, initBLAngleThree, initBRAngleThree, initTRAngleThree, initTLAngleThree, radiusLeverThree, angleAddThree)
        xBallCalcThree, yBallCalcThree, vSpeedCalcThree = determineBallState(xBLThree, yBLThree, xBRThree, yBRThree, xTRThree, yTRThree, xTLThree, yTLThree, xMinThree, xMaxThree, yMinThree, yMaxThree)

        if xBallCalcThree == xBall: # If the ball does not interact with lever three
            
            # Determining the vertices of lever two, and then determining if and how the ball interacts with lever two
            xBLTwo, yBLTwo, xBRTwo, yBRTwo, xTRTwo, yTRTwo, xTLTwo, yTLTwo, xMinTwo, xMaxTwo, yMinTwo, yMaxTwo = determineLeverVerticesCoordinates(xCenterLeverTwo, yCenterLeverTwo, initBLAngleTwo, initBRAngleTwo, initTRAngleTwo, initTLAngleTwo, radiusLeverTwo, angleAddTwo)
            xBallCalcTwo, yBallCalcTwo, vSpeedCalcTwo = determineBallState(xBLTwo, yBLTwo, xBRTwo, yBRTwo, xTRTwo, yTRTwo, xTLTwo, yTLTwo, xMinTwo, xMaxTwo, yMinTwo, yMaxTwo)

            if xBallCalcTwo == xBall: # If the ball does not interact with lever two

                # Determining the vertices of lever one, and then determining if and how the ball interacts with lever one
                xBLOne, yBLOne, xBROne, yBROne, xTROne, yTROne, xTLOne, yTLOne, xMinOne, xMaxOne, yMinOne, yMaxOne = determineLeverVerticesCoordinates(xCenterLeverOne, yCenterLeverOne, initBLAngleOne, initBRAngleOne, initTRAngleOne, initTLAngleOne, radiusLeverOne, angleAddOne)
                xBallCalcOne, yBallCalcOne, vSpeedCalcOne = determineBallState(xBLOne, yBLOne, xBROne, yBROne, xTROne, yTROne, xTLOne, yTLOne, xMinOne, xMaxOne, yMinOne, yMaxOne)

                if (xBallCalcOne != xBall) and ("leverOne" not in leversTouched): # If the ball interacts with lever one and to prevent points being given for the same lever multiple times in the same round
                    leversTouched.append("leverOne")
                    addScoreTotal += 30 # The ball touching lever one gives 30 points

                # xBall, yBall, and vSpeed are assigned values based on their interaction with lever one or no interaction with any lever
                xBall = xBallCalcOne
                yBall = yBallCalcOne
                vSpeed = vSpeedCalcOne

            # If the ball interacts with lever two
            else:
                if "leverTwo" not in leversTouched: # To prevent points being given for the same lever multiple times in the same round
                    leversTouched.append("leverTwo")
                    addScoreTotal += 50 # The ball touching lever two gives 50 points

                # xBall, yBall, and vSpeed are assigned values based on their interaction with lever two
                xBall = xBallCalcTwo
                yBall = yBallCalcTwo
                vSpeed = vSpeedCalcTwo
                
        # If the ball interacts with lever three
        else:
            if "leverThree" not in leversTouched: # To prevent points being given for the same lever multiple times in the same round
                leversTouched.append("leverThree")
                addScoreTotal += 70 # The ball touching lever three gives 70 points

            # xBall, yBall, and vSpeed are assigned values based on their interaction with lever three                      
            xBall = xBallCalcThree
            yBall = yBallCalcThree
            vSpeed = vSpeedCalcThree
            
        ### Thus, lever three (shortest lever) takes priority over lever two (medium-size lever), which in turn takes priority over lever one (longest lever)


    else: # This is equivalent to 'elif yBall >= yBallMax:'; when the ball reaches the score boxes at the bottom of the screen
        
        # Calculating the score for the round based on the round number and which score box the ball hit
        
        if roundGame == 1:
            if xBall < 175:
                roundScore = scoreListOne[0]
            elif 175 <= xBall < 351:
                roundScore = scoreListOne[1]
            elif 351 <= xBall < 527:
                roundScore = scoreListOne[0]
            elif 527 <= xBall < 703:
                roundScore = scoreListOne[2]
            elif 703 <= xBall < 879:
                roundScore = scoreListOne[0]
            elif 879 <= xBall < 1055:
                roundScore = scoreListOne[1]
            else: # This is equivalent to 'elif 1055 <= xBall:'
                roundScore = scoreListOne[0]
        
        elif roundGame == 2:
            if xBall < 175:
                roundScore = scoreListTwo[1]
            elif 175 <= xBall < 351:
                roundScore = scoreListTwo[0]
            elif 351 <= xBall < 527:
                roundScore = scoreListTwo[2]
            elif 527 <= xBall < 703:
                roundScore = scoreListTwo[1]
            elif 703 <= xBall < 879:
                roundScore = scoreListTwo[2]
            elif 879 <= xBall < 1055:
                roundScore = scoreListTwo[0]
            else:
                roundScore = scoreListTwo[1]

        elif roundGame == 3:
            if xBall < 175:
                roundScore = scoreListThree[2]
            elif 175 <= xBall < 351:
                roundScore = scoreListThree[1]
            elif 351 <= xBall < 527:
                roundScore = scoreListThree[2]
            elif 527 <= xBall < 703:
                roundScore = scoreListThree[0]
            elif 703 <= xBall < 879:
                roundScore = scoreListThree[2]
            elif 879 <= xBall < 1055:
                roundScore = scoreListThree[1]
            else:
                roundScore = scoreListThree[2]



    # Readjusting the position of the ball if the ball is off-screen
    if yBall < radiusBall: # This is to prevent the ball from going off the top of the screen
        yBall = radiusBall
        
    elif yBall > yBallMax: # This is to prevent the ball from going through the score boxes
        yBall = yBallMax
        
    if xBall < radiusBall: # This is to prevent the ball from going off the left of the screen
        xBall = radiusBall
        
    elif xBall > screenWidth - radiusBall: # This is to prevent the ball from going off the right of the screen
        xBall = screenWidth - radiusBall





    # ----- Drawing Code -----
    
    # Setting background colour to white
    screen.fill(WHITE)


    
    # Drawing vertical grid lines
    for i in range(30, screenWidth, 30):
        pygame.draw.line(screen, GRAY, (i, 0), (i, screenHeight))

    # Drawing horizontal grid lines
    for i in range(30, screenHeight, 30):
        pygame.draw.line(screen, GRAY, (0, i), (screenWidth, i))



    # Setting the font of the scores on the score boxes
    scoreFont = pygame.font.SysFont(None, 40) # Arguments are the default system font, and font size

    # Setting the scores for each round
    scoreListOne   = [40, 20, 10]
    scoreListTwo   = [45, 25, 15]
    scoreListThree = [50, 30, 20]

    scoreHighOne, scoreMedOne, scoreLowOne = scoresPerRound(scoreListOne)
    scoreHighTwo, scoreMedTwo, scoreLowTwo = scoresPerRound(scoreListTwo)
    scoreHighThree, scoreMedThree, scoreLowThree = scoresPerRound(scoreListThree)

    # Drawing the score boxes and their scores, based on the round
    if roundGame == 1:
        # Drawing the score boxes at the bottom of the screen; 1230 is the screen width, and 1230/7 == 175 R5, so the two score boxes at the end will have a width of 175, and all the others 176
        pygame.draw.rect(screen, BLUE, [0, screenHeight - scoreBoxHeight, 175, scoreBoxHeight]) # [x of top-left corner, y of top-left corner, width, height]
        pygame.draw.rect(screen, GREEN, [175, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])
        pygame.draw.rect(screen, BLUE, [351, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])
        pygame.draw.rect(screen, YELLOW, [527, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])
        pygame.draw.rect(screen, BLUE, [703, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])
        pygame.draw.rect(screen, GREEN, [879, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])
        pygame.draw.rect(screen, BLUE, [1055, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])

        # Displaying the scores on the score boxes
        screen.blit(scoreHighOne, (72, 715)) # Score box 1
        screen.blit(scoreMedOne, (248, 715)) # Score box 2
        screen.blit(scoreHighOne, (424, 715)) # Score box 3
        screen.blit(scoreLowOne, (600, 715)) # Score box 4
        screen.blit(scoreHighOne, (776, 715)) # Score box 5
        screen.blit(scoreMedOne, (952, 715)) # Score box 6
        screen.blit(scoreHighOne, (1128, 715)) # Score box 7
        
    elif roundGame == 2:
        # Drawing the score boxes at the bottom of the screen
        pygame.draw.rect(screen, GREEN, [0, screenHeight - scoreBoxHeight, 175, scoreBoxHeight]) # [x of top-left corner, y of top-left corner, width, height]
        pygame.draw.rect(screen, BLUE, [175, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])
        pygame.draw.rect(screen, YELLOW, [351, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])
        pygame.draw.rect(screen, GREEN, [527, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])
        pygame.draw.rect(screen, YELLOW, [703, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])
        pygame.draw.rect(screen, BLUE, [879, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])
        pygame.draw.rect(screen, GREEN, [1055, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])

        # Displaying the scores on the score boxes
        screen.blit(scoreMedTwo, (72, 715)) # Score box 1
        screen.blit(scoreHighTwo, (248, 715)) # Score box 2
        screen.blit(scoreLowTwo, (424, 715)) # Score box 3
        screen.blit(scoreMedTwo, (600, 715)) # Score box 4
        screen.blit(scoreLowTwo, (776, 715)) # Score box 5
        screen.blit(scoreHighTwo, (952, 715)) # Score box 6
        screen.blit(scoreMedTwo, (1128, 715)) # Score box 7

    elif roundGame == 3:
        # Drawing the score boxes at the bottom of the screen
        pygame.draw.rect(screen, YELLOW, [0, screenHeight - scoreBoxHeight, 175, scoreBoxHeight]) # [x of top-left corner, y of top-left corner, width, height]
        pygame.draw.rect(screen, GREEN, [175, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])
        pygame.draw.rect(screen, YELLOW, [351, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])
        pygame.draw.rect(screen, BLUE, [527, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])
        pygame.draw.rect(screen, YELLOW, [703, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])
        pygame.draw.rect(screen, GREEN, [879, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])
        pygame.draw.rect(screen, YELLOW, [1055, screenHeight - scoreBoxHeight, 176, scoreBoxHeight])

        # Displaying the scores on the score boxes
        screen.blit(scoreLowThree, (72, 715)) # Score box 1
        screen.blit(scoreMedThree, (248, 715)) # Score box 2
        screen.blit(scoreLowThree, (424, 715)) # Score box 3
        screen.blit(scoreHighThree, (600, 715)) # Score box 4
        screen.blit(scoreLowThree, (776, 715)) # Score box 5
        screen.blit(scoreMedThree, (952, 715)) # Score box 6
        screen.blit(scoreLowThree, (1128, 715)) # Score box 7



    if yBall == yBallInit: # If the ball is at the top of the screen (before it is dropped)

        if countLevers >= 1:
            placeDownLever(leverOne, xCenterLeverOne, yCenterLeverOne) # Lever one is displayed on the screen

        if countLevers >= 2:
            placeDownLever(leverTwo, xCenterLeverTwo, yCenterLeverTwo) # Lever two is displayed on the screen

        if countLevers == 3:
            placeDownLever(leverThree, xCenterLeverThree, yCenterLeverThree) # Lever three is displayed on the screen

        
        # This is for the additional score shown in the top-left corner of the screen
        pygame.draw.rect(screen, WHITE, [25, 65, 115, 80]) # This is the filling of the rectangle
        pygame.draw.rect(screen, RED, [25, 65, 115, 80], 2) # This is the border of the rectangle

        addFont = pygame.font.SysFont(None, 70)
        addScore = addFont.render(str(addScoreTotal), True, RED)
        screen.blit(addScore, (42, 85))


    elif yBall < yBallMax: # After the ball is dropped, before the ball reaches the score boxes at the bottom of the screen
        
        # Displaying rotated levers on the screen
        rotateLever(leverOne, angleAddOne, xCenterLeverOne, yCenterLeverOne)
        rotateLever(leverTwo, angleAddTwo, xCenterLeverTwo, yCenterLeverTwo)
        rotateLever(leverThree, angleAddThree, xCenterLeverThree, yCenterLeverThree)


        # This is for the additional score shown in the top-left corner of the screen
        pygame.draw.rect(screen, WHITE, [25, 65, 115, 80]) # This is the filling of the rectangle
        pygame.draw.rect(screen, RED, [25, 65, 115, 80], 2) # This is the border of the rectangle

        addFont = pygame.font.SysFont(None, 70)
        addScore = addFont.render(str(addScoreTotal), True, RED)
        screen.blit(addScore, (42, 85))
    

    else: # This is equivalent to 'elif yBall >= yBallMax:'; when the ball reaches the score boxes at the bottom of the screen
        
        # Setting up the fonts of the text shown at the end of the rounds
        roundFont = pygame.font.SysFont(None, 100)
        clickFont = pygame.font.SysFont(None, 50)

        # Different rounds have different texts
        if roundGame == 1:
            roundNum = roundFont.render("Round 1", True, RED)
        elif roundGame == 2:
            roundNum = roundFont.render("Round 2", True, RED)
        elif roundGame == 3:
            roundNum = roundFont.render("Round 3", True, RED)

        # Setting up the other text that will be displayed on the screen
        roundScoreText = roundFont.render("Score:", True, RED)
        roundScoreNum = roundFont.render(str(roundScore), True, RED)
        clickText = clickFont.render("[click to continue]", True, RED)

        # This is for a background behind the text
        pygame.draw.rect(screen, WHITE, [425, 148, 375, 410]) # This is the filling of the rectangle
        pygame.draw.rect(screen, RED, [425, 148, 375, 410], 2) # This is the border of the rectangle

        # Displaying the text
        screen.blit(roundNum, (480, 200))
        screen.blit(roundScoreText, (510, 310))
        screen.blit(roundScoreNum, (575, 385))
        screen.blit(clickText, (467, 490))


        # This is for the additional score shown in the top-left corner of the screen
        pygame.draw.rect(screen, WHITE, [25, 65, 115, 80]) # This is the filling of the rectangle
        pygame.draw.rect(screen, RED, [25, 65, 115, 80], 2) # This is the border of the rectangle

        addFont = pygame.font.SysFont(None, 70)
        addScore = addFont.render(str(addScoreTotal), True, RED)
        screen.blit(addScore, (42, 85))


    
    # Drawing the ball
    pygame.draw.circle(screen, ballColour, [xBall, yBall], radiusBall)



    # If the user is done playing the game (finished all three rounds), then the drawing code below will override all of the drawing code above
    if doneGame == True:
        
        # Setting background colour to white
        screen.fill(WHITE)


        # This is for the individual scores
        addendFont = pygame.font.SysFont(None, 60)
        
        totalRoundScore = addendFont.render("Score from Rounds: " + str(roundScoreTotal), True, RED)
        totalAddScore = addendFont.render("Additional Score: " + str(addScoreTotal), True, RED)

        screen.blit(totalRoundScore, (415, 150))
        screen.blit(totalAddScore, (425, 210))

        
        # This is for the total score
        totalFont = pygame.font.SysFont(None, 120)
        
        totalScore = totalFont.render("Total Score:", True, RED)
        totalScoreNum = totalFont.render(str(roundScoreTotal + addScoreTotal), True, RED)
        
        screen.blit(totalScore, (410, 320))
        screen.blit(totalScoreNum, (565, 435))


    
    # ----- Updating the screen -----
    pygame.display.flip()


    # ----- Setting max. frames per second to 60 -----
    clock.tick(60)


# Terminating pygame
pygame.quit()
