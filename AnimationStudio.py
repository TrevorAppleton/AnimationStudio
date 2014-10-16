from Tkinter import *
from ttk import *
import os
import glob

import Image, ImageTk

## Functions to select frames
def firstFrame():
    if countFrames()>0:
        frameNumber.set(1) #If there are any frames
    else:
        frameNumber.set(0) #Set to 0 if there are none
    updateGUI()
    return None

def lastFrame():
    frameNumber.set(countFrames())
    updateGUI()
    return None

def nextFrame():
    if frameNumber.get() < (countFrames()):
        frameNumber.set(frameNumber.get()+1)
    updateGUI()
    return None

def prevFrame():
    if frameNumber.get() > 1:
        frameNumber.set(frameNumber.get()-1)
    updateGUI()
    return None

def takeFrame():
    frameNumber.set(countFrames()+1)   
    os.system("raspistill -o image%s.jpg"%(setZero()))
    updateGUI()
    return None

##Deletes the last stored frame
def deleteFrame():    
    frameNumber.set(countFrames())
    if countFrames() > 0:
        os.remove('image%s.jpg'%setZero())
        frameNumber.set(countFrames())
        updateGUI()
    return None

##Returns the number of jpg files in the directory.
def countFrames():
    openFiles = glob.glob('image*.jpg')
    return len(openFiles)

## sets the right number of zeros for the frameNumber
def setZero():
    return str(frameNumber.get()).zfill(7)

##Updates the image in the GUI and refreshes
def updateGUI():
        
    if countFrames()>0: # Checks to see if there are any existing frames
        fileName = "image%s.jpg"%setZero()
        inFile = Image.open(fileName)        
        ## Resize image to suit GUI
        ## Was 2592 x 1944 - Divide both of these by 6
        newSizeFile = inFile.resize((400,300))
        
        displayFile =  ImageTk.PhotoImage(newSizeFile)#Convert to Tkinter compatible
        Label(mainframe, image=displayFile).grid(column=1, row = 1, sticky = 'WE',columnspan = 5)
        root.update()#Refreshes
                
    else:
        
        frameImage = PhotoImage(file = "blankScreen.gif")
        Label(mainframe, image=frameImage).grid(column=1, row = 1, sticky = 'WE',columnspan = 5)
        root.update()

## Creates the video file.
def createFilm():
    setfpsIn = fpsIn.get()
    setfpsOut = fpsOut.get()
    os.system("avconv -r %s -i image%s.jpg -r %s -vcodec libx264 -crf 20 -g 15 -vf crop=2592:1458,scale=1280:720 timelapse.mp4"%(setfpsIn,'%7d',setfpsOut))
    return None


##Setup of main GUI
root = Tk()
root.title ('Animation Studio')
root.geometry("410x450")

mainframe = Frame(root, padding = '3 3 12 12')
mainframe.grid(column=0, row = 0, sticky=(N,W,E,S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0,weight=1)

##Variables
frameNumber = IntVar()
fpsIn = IntVar()
fpsOut = IntVar()

##Set Variables
frameNumber.set(countFrames())
fpsIn.set(10)
fpsOut.set(24)

##Frame Select
Button(mainframe, text="<<", command = firstFrame).grid(column = 1, row = 2, sticky = 'WE')
Button(mainframe, text="<", command = prevFrame).grid(column = 2, row = 2, sticky = 'WE')
Button(mainframe, text=">", command = nextFrame).grid(column = 4, row = 2, sticky = 'WE')
Button(mainframe, text=">>", command = lastFrame).grid(column = 5, row = 2, sticky = 'WE')
Entry(mainframe, textvariable = frameNumber, width = 7).grid(column = 3, row = 2, sticky = 'WE')


##Take Frame
Button(mainframe, text="Take Frame", command = takeFrame).grid(column = 1, row = 3, sticky = "WE", columnspan = 5)

##Delete Frame
Button(mainframe, text="Delete Last Frame", command = deleteFrame).grid(column = 1, row = 4, sticky = "WE", columnspan = 5)

##Set FPS in
Label(mainframe, text='Set FPS In').grid(column=1, row = 5, sticky = W)
Entry(mainframe, textvariable = fpsIn, width = 7).grid(column = 2, row = 5, sticky = 'WE')

##Set FPS out
Label(mainframe, text='Set FPS Out').grid(column=4, row = 5, sticky = W)
Entry(mainframe, textvariable = fpsOut, width = 7).grid(column = 5, row = 5, sticky = 'WE')

##Create Film
Button(mainframe, text="Create Film", command = createFilm).grid(column = 1, row = 7, sticky = "WE", columnspan = 5)

updateGUI()

root.mainloop()
