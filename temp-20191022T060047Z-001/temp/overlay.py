from guizero import App, Text, Picture
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
#camera =PiCamera()
#camera.resolution=(800,480)


def take_picture():
    camera =PiCamera()
    camera.resolution=(760,760)
    camera.start_preview(alpha=255)
    camera.hflip=True
    output = strftime("/home/pi/Desktop/temp/pic/image-%d-%m %H:%M.png", gmtime())
    camera.capture(output)
    camera.stop_preview()
    #remove_overlays(camera)
    output_overlay(output,overlay)
    time.sleep(2)

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
    print('Distance: {} cm'.format(distance))
    return distance

def auto():
    distance= get_distance()
    time.sleep(0.05)

    if 80>distance>70:
        take_picture()
    elif 70>distance>80:
        print('please come in range') 
app= App("Smart Shopping Mirror", 800,480)
message=Text(app, "Shop Smartly")
app.display()


