#original import
from tkinter import*
from functools import total_ordering
import time
from PIL import ImageTk, Image
import io
import os
import RPi.GPIO as GPIO
from PIL import Image, ImageTk

#allseeing pi import
from time import gmtime, strftime
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
from overlay_functions import*

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()

TRIG=4
ECHO=18

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

camera =PiCamera()
camera.resolution=(760,760)

app = Tk() #main window
currentLoc = .5 #location of x of image
filename="gn1.gif" 
output=""
#a="" #for future use

def newwin(): #new window for pic capture with overlay
    top = Toplevel()
    top.title("Capture Image")
    top.geometry("730x1360")
    destroy= Button(top, text= "Close", command=top.destroy, fg="white", bg= "black", height = 1, width =8 )
    destroy.place(relx= .9, rely=.97, anchor="c")
    top.configure(bg='black')
    
    camera.start_preview(alpha=255)
    camera.hflip=True
    preview_overlay(camera, overlay) 
    
    Next = Button(top, text = "Next overlay",command = next_overlay, fg="white", bg= "black", height = 1, width =8 )
    Next.place(relx= .565, rely=.97, anchor="c")

    takepic = Button(top, text = "Take picture",command = take_picture, fg="white", bg= "black", height = 1, width =8 )
    takepic.place(relx= .5, rely=.93, anchor="c")

    Preview = Button(top, text = "Stop Preview",command = stoppreview, fg="white", bg= "black", height = 1, width =8 )
    Preview.place(relx= .435, rely=.97, anchor="c")
#1st image
img = ImageTk.PhotoImage(Image.open("in1.gif"))
panel = Label(app, image = img,bd=0, bg='black')
panel.place(relx= .5, rely=.5, anchor="c")

#welcome text
T = Text(app, height= 1, width=80, bg='black', fg='white')
T.insert(END, "\t\t\t             Welcome to Smart Mirror")
T.place(relx=.5, rely=.033, anchor= "c")
T.config(font=("times",13))

#contributors
T2 = Text(app, height=2, width= 15, bg= 'black',fg= 'white')
T2.insert(END, "     Contribution of \nOmey, Nasir, Nababi.")
T2.place(relx=.9, rely=.06, anchor="c")
T2.config(font=("times",8),highlightbackground='black')

#distance information
S = Text(app, height= 1, width=80, bg='black', fg='white')
S.insert(END, "\t\t             Stand Within 70 to 80 cm")
S.place(relx=.5, rely=.92, anchor= "c")


def take_picture():
    global output
    global img
    output = strftime("/home/pi/Desktop/temp/pic/image-%d-%m %H:%M.png", gmtime())
    camera.capture(output)
    camera.stop_preview()
    remove_overlays(camera)
    output_overlay(output,overlay)
    img = ImageTk.PhotoImage(Image.open(output))
    panel = Label(app, image = img,bd=0, bg='black')
    panel.place(relx= .5, rely=.5, anchor="c")

def stoppreview():
    camera.stop_preview()
    remove_overlays(camera)
    
def next_overlay():
    global overlay
    overlay= next(all_overlays)
    preview_overlay(camera, overlay)

def get_distance():

    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == False:
            start = time.time()
    while GPIO.input(ECHO) == True:
            end = time.time()
    sig_time = end-start

    #cm
    distance = sig_time/0.000058
    #print('Distance: {} cm'.format(distance))
    return distance

#this function change background of welcome text
def change():
    currentBg= T.cget("bg")
    nextBg = "white" if currentBg == "black" else "black"
    nextFg = "white" if currentBg== "white" else "black"
    T.config(bg=nextBg,fg=nextFg)
    app.after(1000,change)
change()    


#set text of distance information
def distanceInform():
     
                 
         distance= get_distance()
         time.sleep(0.05)

         if 80>distance:
          
             S2 = Text(app, height= 1, width=80, bg='black', fg='white')
             S2.insert(END, "\t\t\t\t   Distance ok")
             S2.place(relx=.5, rely=.904, anchor= "c")
             
         elif 90<distance:
            
             S2 = Text(app, height= 1, width=80, bg='black', fg='white')
             S2.insert(END, "\t\t\t\tPlease come in range")
             S2.place(relx=.5, rely=.904, anchor= "c")
         app.after(1500,distanceInform)    
            
   
distanceInform()  

def UP():
    global img
    global currentLoc
    currentLoc= currentLoc-.01
    img = ImageTk.PhotoImage(Image.open(filename))
    panel = Label(app, image = img,bd=0,bg='black')
    panel.place(relx=.5, rely=currentLoc, anchor="c")
    
def Down():
    global img
    global currentLoc
    currentLoc= currentLoc+.01
    img = ImageTk.PhotoImage(Image.open(filename))
    panel = Label(app, image = img,bd=0,bg='black')
    panel.place(relx=.5, rely=currentLoc, anchor="c") 
  

def exitProgram():
    print("Exit Button pressed")
    GPIO.cleanup()
    #app.iconify()
    app.destroy()
  
  
def choose(x):
    global img
    global filename
    if x == "male":
       filename = "tm2.gif"
       img = ImageTk.PhotoImage(Image.open("tm2.gif"))
       panel = Label(app, image = img,bd=0, bg='black')
       panel.place(relx= .5, rely=.5, anchor="c")
       
    elif x == "ornament":
       filename = "gn1.gif"
       img = ImageTk.PhotoImage(Image.open("gn1.gif"))
       panel = Label(app, image = img,bd=0, bg='black')
       panel.place(relx= .5, rely=.5, anchor="c")
       
    elif x == "diamond":
       filename = "gn1.gif"
       img = ImageTk.PhotoImage(Image.open("gn2.gif"))
       panel = Label(app, image = img,bd=0, bg='black')
       panel.place(relx= .5, rely=.5, anchor="c")   
    
    elif x == "shirt":
       filename = "sm2.gif"
       img = ImageTk.PhotoImage(Image.open("sm2.gif"))
       panel = Label(app, image = img,bd=0, bg='black')
       panel.place(relx= .5, rely=.5, anchor="c")

    else:
        global filename
        filename = "tg2.gif"
        img = ImageTk.PhotoImage(Image.open("tg2.gif"))
        panel = Label(app, image = img,bd=0, bg='black')
        panel.place(relx= .5, rely=.5, anchor="c")
        
    
app.title("Smart Mirror")
app.configure(bg='black')
app.geometry("730x1360")
app.attributes('-fullscreen',True)

exitButton  = Button(app, text = "Exit",command = exitProgram,  fg="white", bg= "black", height =1 , width = 8) 
exitButton.place(relx=.09, rely=.95, anchor="c")

#opens new window to capture pic
Auto = Button(app, text = "picture",command = newwin, fg="white", bg= "black", height = 1, width =8 )
Auto.place(relx= .9, rely=.95, anchor="c")

Up= Button(app, text = "Move Up",command = UP, fg="white", bg= "black", height = 1, width =8 )
Up.place(relx= .5, rely=.94, anchor="c")
Down= Button(app, text = "Move Down",command = Down, fg="white", bg= "black", height = 1, width =8 )
Down.place(relx= .5, rely=.965, anchor="c")

#dropdown menu to show image
oc= StringVar()
oc.set("Select")
OMenu = OptionMenu(app, oc, "male","female","ornament","diamond","shirt",command=choose)
OMenu.place(relx=.5,rely=.055,anchor="c")


app.mainloop()



