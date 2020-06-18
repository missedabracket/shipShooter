#Ship Shooter
from guizero import App, Box, Text, TextBox, Waffle, info, MenuBar
import random

def compWin():
    playerWaffle.set_all('red')
    info("You lose","You have been defeated by the enemy!")

def playerWin():
    computerWaffle.cancel(attackPlayer)
    computerWaffle.set_all('red')
    info("Player wins","You have defeated the enemy!")

def pClicked(x,y):
    global playerShip
    location = str(x) + "," + str(y)
    playerText.value = "Players ship is at: "+ location + ". "
    #print(location)
    playerShip = [x,y]
    #print(playerShip)
    computerWaffle.show()
    aiSearch("hard")  # Always set to hard at the moment
    playerWaffle.set_pixel(x,y,'yellow')
    playerWaffle.enabled = False

def cClicked(x,y):
    global missiles
    location = str(x) + "," + str(y)
    compText.value = location
    #print(location)
    setLocation(x,y)
    missiles -=1
    missilesText.value = missiles
    #attackPlayer()

def attackPlayer():
    global aiSearchLocations
    #Randomly pick and remove from list, a location to fire missile at
    loc = aiSearchLocations.pop()
    #print(loc)
    x = loc[0]
    y = loc[1]
    playerWaffle.set_pixel(x,y,'black')
    missileHistory.value = missileHistory.value + str(loc) + "\n"
    #Check if computer has won
    if loc == playerShip:
        playerWaffle.after(500,compWin)

def setLocation(x,y):
    global compShip
    computerWaffle.set_pixel(x,y,'black')
    computerWaffle.after(1000,attackPlayer)
    #If correct location player wins
    if compShip == [x,y]:
        computerWaffle.set_pixel(x,y,'red')
        computerWaffle.after(500,playerWin)

    #computerWaffle.after(5000,attackPlayer())

#Generate a list of places to search
def aiSearch(difficulty):
    global aiSearchLocations, playerShip
    if difficulty == "easy":
        for i in range(80):
            x = random.randrange(10)
            y = random.randrange(10)
            aiSearchLocations.append([x,y])
    elif difficulty == "normal":
        for i in range(40):
            x = random.randrange(10)
            y = random.randrange(10)
            aiSearchLocations.append([x,y])
    else:
        for i in range(10):
            x = random.randrange(10)
            y = random.randrange(10)
            aiSearchLocations.append([x,y])
    size = len(aiSearchLocations)
    #print(playerShip)
    aiSearchLocations.insert(random.randint(0,size), playerShip) #Insert actual ship location in random place

#Needs to take a variable but doesn't yet! Always set to hard
def reInitialise():
    global missiles, compShip, aiSearchLocations, playerShip
    playerWaffle.enabled = True
    missiles = 10
    missilesText.value = missiles
    missileHistory.value = ""
    aiSearchLocations = []
    playerShip = []
    x = random.randint(0,9)
    y = random.randint(0,9)
    compShip = [x,y]
    print(compShip)
    playerWaffle.set_all('blue')
    computerWaffle.set_all('aqua')
    computerWaffle.hide()
    #aiSearch("hard") #Change to normal or easy if wanted

#Set vars
missiles = 10
x = random.randint(0,9)
y = random.randint(0,9)
compShip = [x,y] # location of computer ship
playerShip = []  # Location that player chooses
print(compShip)
aiSearchLocations = []  # Locations ai will search
mHistory = "" #Stores ai missile attempts

#Windows and Boxes
battleBoard = App(title="Ship Shooter",width=700,height=700,layout="grid")
playerBoard = Box(battleBoard,layout="grid",grid=[0,0])
compBoard = Box(battleBoard,layout="grid",grid=[1,0])
textBoxes = Box(battleBoard,layout="grid",grid=[0,1],align='left')
missileBox = Box(battleBoard,layout="grid",grid=[0,2],align='right')
menubar = MenuBar(battleBoard,
                  toplevel=["Game"],
                  options=[
                      [ ["Easy", reInitialise], ["Normal", reInitialise], ["Hard", reInitialise] ]
                  ])

#Game boards for ships
playerWaffle = Waffle(playerBoard,height=10,width=10,dim=29,grid=[0,0],color="blue",command=pClicked)
computerWaffle = Waffle(compBoard,height=10,width=10,dim=29,grid=[0,0],color="aqua",command=cClicked)

#Text information
Text(textBoxes,text="Missiles remaining: ",size=18,color="blue",grid=[0,0],align='left')
playerText = Text(textBoxes,text="Players ship is at: ",size=18,color="blue",grid=[0,1],align='left')
missilesText = Text(textBoxes,text=missiles,size=18,grid=[1,0],color="blue")
compText = Text(textBoxes,text=compShip,size=18,color="green",grid=[0,2])
missileHistory = Text(textBoxes,text=mHistory,size=12,color="red",grid=[0,3])

#starting settings
computerWaffle.hide()

#Show game
battleBoard.display()