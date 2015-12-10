
from gopigo import *
import time
STOP_DIST = 50

class Pigo:

    #####
    ##### Basic status and methods
    #####

    status = {"ismoving" : False, "servo" : 90, "leftspeed" : 175, "rightspeed" : 175, "dist": 100}
    vision = [None] * 180
    STEPPER = 5


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
        servo(90)
        time.sleep(.1)
        self.status['dist'] = us_dist(15)
        print "Obstruction detected " + str(self.status['dist']) + "mm away"
        if self.status['dist'] < STOP_DIST:
            return False
        else:
            return True

    def servoPos(self):
        servo(90)
    #########
    ##### Complex methods
    #####

    def safeDrive(self):
        self.fwd()
        while self.keepGoing():
            self.checkDist()
        self.stop()

    def servoSweep(self):
        for ang in range(20,160,self.STEPPER):
            servo(ang)
            time.sleep(.1)
            self.vision[ang] = us_dist(15)

    def spinRight(self):
        self.right_rot()
        time.sleep(3)
        self.stop()

    def spinLeft(self):
        self.left_rot()
        time.sleep(3)
        self.stop()

    def isAPath(self):
        for ang in range(10, 160, self.STEPPER):
            counter = 0
            if self.vision[ang] > 20:
                counter += 5
            else:
                counter = 0
            if counter >= 20/self.STEPPER:
                return True
        return False

    def turnTo(self, angle):
        BIGTURN = .5
        turn = .2

        if angle > 130 or angle < 50:
            turn = BIGTURN
        if angle > 90:
            print "we're turning left"
            self.left_rot()
            time.sleep(turn)
            self.stop()
        else:
            print "we're turning right"
            self.right_rot()
            time.sleep(turn)
            self.stop()


    def smartChoice(self):
        counter = 0
        option = [0] * 12 #we're going to fill this array with the angles of open paths
        optindex = 0  #this starts at 0 and will increase every time we find an option
        for ang in range(20, 160, self.STEPPER):
            if self.vision[ang] > STOP_DIST:
                counter += 1
            else:
                counter = 0
            if counter >= (20/self.STEPPER):
                print "We've found an option at angle " + str(ang - 10)
                option[optindex] = (ang - 10)
                counter = 0
                optindex += 1
        if self.status['wentleft']:
            print "I went left last time. Seeing if I have a right turn option"
            for choice in option:
                if choice < 90:
                    self.status['wentleft'] = False #switch this for next time
                    return choice
        else:
            print "Went right last time. Seeing if there's a left turn option"
            for choice in option:
                if choice > 90:
                    self.status['wentleft'] = True
                    return choice
        print "I couldn't turn the direction I wanted. Goint to use angle " + str(option[0])
        if option[0] != 0: #let's make sure there's something in there
            return option[0]
        print "If I print this line I couldn't find an angle. How'd I get this far?"
        return 90



    def turnAround(self):
        return "Turn Around"

#####
##### Main app starts here
#####
tina = Pigo()
#tina.RUNPROGRAM
while True:
    if tina.checkDist():
        tina.safeDrive()
    else:
        tina.servoSweep()
        if tina.isAPath():
            tina.turnTo(tina.smartChoice())
        else:
            tina.turnAround()
