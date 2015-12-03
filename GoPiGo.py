
from gopigo import *
import time
STOP_DIST = 50

class Pigo:

    #####
    ##### Basic status and methods
    #####

    status = {"ismoving" : False, "servo" : 90, "leftspeed" : 175, "rightspeed" : 175, "dist": 100}
    #ismoving = False
    #servoPos = 90


    def __init__(self):
        print "I am alive. Beep beep."
        self.status["dist"] = us_dist(15)
    def stop(self):
        self.status["ismoving"] = False
        for x in range(3):
            stop()
            print "Halt!"
    def fwd(self):
        self.status ["ismoving"] = True
        for x in range(3):
            fwd()

    def bwd(self):
        self.status ["ismoving"] = True
        for x in range(3):
            bwd()

    def right_rot(self):
        for x in range(3):
            right_rot()

    def left_rot(self):
        for x in range(3):
            left_rot()

    #Check if the conditions are safe for the PiGo to continue.
    def keepGoing(self):
        if self.status["dist"] < STOP_DIST:
            print "Obstacle within stop distance."
            return False
        elif volt() > 14 or volt() < 6:
            print "Voltage level unsafe." + str(volt())
            return False
        else:
            return True

    def checkDist(self):
        self.status['dist'] = us_dist(15)
        print "Obstruction detected " + str(self.status["dist"]) + "mm away"
    #####
    ##### Complex methods
    #####

    def safeDrive(self):
        self.fwd()
        while self.keepGoing():
            self.checkDist()
        self.stop()

    def servoSweep(self):
        for ang in range(20,160,5):
            servo(ang)
            time.sleep(.1)

    def spinRight(self):
        self.right_rot()
        time.sleep(3)
        self.stop()

    def spinLeft(self):
        self.left_rot()
        time.sleep(3)
        self.stop()


    #####
    ##### Main app starts here
    #####
tina = Pigo()