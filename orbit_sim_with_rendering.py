from tkinter import *
import time
import random
import math

#Made by Crisian Bicheru 2018
#Uses Newtonian physics
#Orbiting objects seem to gain energy over time,
#likely due to the gap in time between calculations

WIDTH = 1300             #resolution, 
HEIGHT = 1000

dT = 0.0005              #delay between frames, <0.0005 is optimal since this is a render.
                         #changing this in-sim results in interesting behaviour when dT is high
blackHoleMass = 10000000 #default mass of black hole
gravConstant = 1         #default gravitational constant
ox = 0                   #default spawn offset x
oy = 0                   #default spawn offset y
spawnSpeedX = 0          #default spawn speed (x direction)
spawnSpeedY = 0          #default spawn speed (y direction)
playbackRate = 1         #default playback rate (must be an int currently {otherwise you have to approximate})
triggerDistance = 1      #you can set this lower if you also set dT lower (you have to raise it if you raise dT), if you set this too low the code may not detect an elapsed orbit

unrenderedSpheres = 0
lines = []
toggle = 0
timeToggle = 0
frozen = []

tk = Tk()
back = Canvas(tk, width=WIDTH+255, height=HEIGHT+20)
back.pack()
simFrame = Frame(tk)
canvas = Canvas(simFrame, width=WIDTH, height=HEIGHT, bg="grey")
tk.title("orbital motion")
simFrame.place(x=245, y=10)
canvas.pack()

class Ball:
    def __init__(self):
        global unrenderedSpheres
        self.size = random.randrange(20, 30)
        self.shape = canvas.create_oval(ox, oy, self.size+ox, self.size+oy, fill="red")
        self.speedx = spawnSpeedX
        self.speedy = spawnSpeedY
        self.t = 0
        self.delayt = 0
        self.dT = dT
        self.startX = ox+self.size/2
        self.startY = oy+self.size/2
        self.frame = -1
        self.frames = 0
        self.boundUnlock = 0
        self.renderComplete = 0
        self.renderedFrames = {}
        unrenderedSpheres += 1
        menu().update()

    def update(self):
        if self.dT == 0:
            pass
        else:
            global dT, planets, unrenderedSpheres, triggerDistance
            if self.renderComplete == 0:
                self.t += self.dT
                pos = canvas.coords(self.shape)
                centerX = (pos[0]+pos[2])/2
                centerY = (pos[1]+pos[3])/2
                if centerY - HEIGHT/2 > 0:
                    gravMagnitude = (gravConstant*blackHoleMass/((centerX-WIDTH/2)**2+(centerY-HEIGHT/2)**2))
                    aByc = (centerX-WIDTH/2) / math.sqrt((centerX-WIDTH/2)**2+(centerY-HEIGHT/2)**2)
                    gravXacceleration = -(gravMagnitude*(aByc))
                    gravYacceleration = -(gravMagnitude*math.cos(math.asin(aByc)))
                        
                else:
                    gravMagnitude = (gravConstant*blackHoleMass/((centerX-WIDTH/2)**2+(centerY-HEIGHT/2)**2))
                    aByc = (centerX-WIDTH/2) / math.sqrt((centerX-WIDTH/2)**2+(centerY-HEIGHT/2)**2)
                    gravXacceleration = -(gravMagnitude*(aByc))
                    gravYacceleration = (gravMagnitude*math.cos(math.asin(aByc)))

                #black hole collision
                if abs(centerX-WIDTH/2) < (15+self.size/2) and abs(centerY-HEIGHT/2) < (15+self.size/2):
                    canvas.delete(self.shape)
                    planets.remove(self)
                    unrenderedSpheres += -1
                
                dy = self.speedy*(self.dT)+0.5*gravYacceleration*(self.dT)**2
                dx = self.speedx*(self.dT)+0.5*gravXacceleration*(self.dT)**2
                self.speedy += (gravYacceleration*self.dT)
                self.speedx += (gravXacceleration*self.dT)
                canvas.move(self.shape, dx, dy)

                
                
                self.renderedFrames[round(self.t/self.dT)-1] = [centerY, centerX]

                if self.boundUnlock == 0:
                    if abs(centerX-self.startX) > 10:
                        self.boundUnlock = 1
                
                if abs(centerX-self.startX) < triggerDistance and abs(centerY-self.startY) < triggerDistance and self.boundUnlock == 1:
                    self.renderComplete = 1
                    unrenderedSpheres += -1
                    self.frames = len(self.renderedFrames)
                    canvas.itemconfig(self.shape, fill="green")
                    menu().update()
            else:
                global playbackRate
                self.frame += playbackRate
                self.frame = self.frame % self.frames
                pos = canvas.coords(self.shape)
                centerX = (pos[0]+pos[2])/2
                centerY = (pos[1]+pos[3])/2
                y = self.renderedFrames[self.frame][0]
                x = self.renderedFrames[self.frame][1]
                dy = y-centerY
                dx = x-centerX
                canvas.move(self.shape, dx, dy)
        

class blackHole:
    def __init__(self):
        self.size = 30
        self.shape = canvas.create_oval((WIDTH-self.size)/2, (HEIGHT-self.size)/2, (WIDTH+self.size)/2, (HEIGHT+self.size)/2, fill="black")
    def update(self):
        pass


class menu:
    def __init__(self):
        global gravConstant, blackHoleMass, dT, playbackRate
        self.button = Button(tk, text="Spawn New", command=self.createNewBall, state="normal")
        self.button.place(x=70, y=10)
        self.label = Label(tk, text = "x-coordinate:")
        self.label.place(x=10, y=40)
        self.label = Label(tk, text = "y-coordinate:")
        self.label.place(x=10, y=65)
        self.label = Label(tk, text = "x-velocity:")
        self.label.place(x=10, y=90)
        self.label = Label(tk, text = "y-velocity:")
        self.label.place(x=10, y=115)
        self.label = Label(tk, text = "grav. constant:")
        self.label.place(x=10, y=170)
        self.label = Label(tk, text = "black hole mass:")
        self.label.place(x=10, y=195)
        self.label = Label(tk, text = "delta-time:")
        self.label.place(x=10, y=220)
        self.label = Label(tk, text = "playback rate:")
        self.label.place(x=10, y=395)
        self.label2 = Label(tk, text = str(playbackRate)+"x")
        self.label2.place(x=110, y=395)
        self.entry = Entry(tk)
        self.entry.insert(0, "0")
        self.entry.place(x=110, y=40)
        self.entry2 = Entry(tk)
        self.entry2.insert(0, "0")
        self.entry2.place(x=110, y=65)
        self.entry3 = Entry(tk)
        self.entry3.insert(0, "0")
        self.entry3.place(x=110, y=90)
        self.entry4 = Entry(tk)
        self.entry4.insert(0, "0")
        self.entry4.place(x=110, y=115)
        self.button2 = Button(tk, text="Update:", command=self.updateVals, state="disabled")
        self.button2.place(x=80, y=140)
        self.entry5 = Entry(tk)
        self.entry5.insert(0, gravConstant)
        self.entry5.place(x=110, y=170)
        self.entry6 = Entry(tk)
        self.entry6.insert(0, blackHoleMass)
        self.entry6.place(x=110, y=195)
        self.entry7 = Entry(tk)
        self.entry7.insert(0, dT)
        self.entry7.place(x=110, y=220)
        self.button3 = Button(tk, text="Show/Hide Grid", command=self.toggleGrid)
        self.button3.place(x=60, y=245)
        self.button4 = Button(tk, text="Clear Planets and Allow Spawning", command=self.planetDestroy)
        self.button4.place(x=5, y=275)
        self.button5 = Button(tk, text="Freeze Time", command=self.freezeTime, state="normal")
        self.button5.place(x=65, y=305)
        self.button6 = Button(tk, text="Increase Playback Speed", command=self.increasep, state="normal")
        self.button6.place(x=35, y=335)
        self.button7 = Button(tk, text="Decrease Playback Speed", command=self.decreasep, state="normal")
        self.button7.place(x=35, y=365)

    def increasep(self):
        global playbackRate, unrenderedSpheres
        self.button.config(state="disabled")
        self.button5.config(state="disabled")
        playbackRate += 1
        self.label2.config(text = str(playbackRate)+"x")

    def decreasep(self):
        global playbackRate
        self.button.config(state="disabled")
        self.button5.config(state="disabled")
        playbackRate += -1          
        self.label2.config(text = str(playbackRate)+"x")
    
    def freezeTime(self):
        global timeToggle, frozen, planets
        if timeToggle == 0:
            frozen = planets
            planets = []
            self.button.config(state="disabled")
            self.button5.config(text="Unfreeze Time")
            timeToggle = 1
        else:
            planets = frozen
            frozen = []
            self.button.config(state="normal")
            self.button5.config(text="Freeze Time")
            timeToggle = 0

    def planetDestroy(self):
        global planets, frozen, timeToggle, unrenderedSpheres
        if timeToggle == 0:
            for planet in planets:
                canvas.delete(planet.shape)
                planets = []
        else:
            for planet in frozen:
                canvas.delete(planet.shape)
                frozen = []
        unrenderedSpheres = 0
        self.button.config(state="normal")
        self.button5.config(state="normal")
        
        
    
    def createNewBall(self):
        global ox, oy, spawnSpeedX, spawnSpeedY
        ox = float(self.entry.get())*50
        oy = float(self.entry2.get())*50
        spawnSpeedX = float(self.entry3.get())*50
        spawnSpeedY = float(self.entry4.get())*50
        planets.append(Ball())

    def updateVals(self):
        pass

    def toggleGrid(self):
        global lines, toggle
        if toggle == 0:
            numRows = int(round(HEIGHT/50))
            numColumns = int(round(WIDTH/50))
            for x in range(1, numColumns):
                vertLine = canvas.create_line(50*x, 0, 50*x, HEIGHT)
                lines.append(vertLine)
            for y in range(1, numRows):
                horiLine = canvas.create_line(0, 50*y, WIDTH, 50*y)
                lines.append(horiLine)
            toggle = 1
        else:
            for line in lines:
                canvas.delete(line)
            toggle = 0
    
    def update(self):
        global playbackRate, unrenderedSpheres
        if unrenderedSpheres != 0:
            self.button6.config(state="disabled")
            self.button7.config(state="disabled")
        else:
            self.button6.config(state="normal")
            self.button7.config(state="normal")
            self.button.config(state="normal")


planets = []
others = []
others.append(blackHole())
others.append(menu())
blackHole().update()
while True:
    for objecT in planets:
        objecT.update()
    tk.update()
    time.sleep(dT)
