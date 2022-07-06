import os
import logging
import RPi.GPIO as GPIO
import time
import threading
from datetime import datetime

#Set up logger to file and console
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)-6s %(levelname)-8s %(message)s',
                    filename="/home/pi/GarageWeb/backend/garagewebapi/static/log.txt")
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)-6s %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)


logging.info("Program Starting -- Hello!")

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class GarageDoor:
    def __init__(self, DoorName, pin1, pin2):
        self.DoorName = DoorName
        self.pin1 = pin1
        self.pin2 = pin2
        self.TimeDoorOpened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')  #Default Time
        self.DoorOpenTimer = -1  #Default start status turns timer off
        self.DoorOpenTimerMessageSent = 1  #Turn off messages until timer is started
        GPIO.setup(self.pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        logging.debug(self.DoorName + "'s Garage Door initialized on pins + " + str(self.pin1) + " and " + str(self.pin2))


    def run(self, _running):
        while _running():
            time.sleep(1)
            if self.DoorOpenTimer == 1:  #Door Open Timer has Started
                currentTimeDate = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
                if (currentTimeDate - self.TimeDoorOpened).seconds > 900 and self.DoorOpenTimerMessageSent == 0:
                    logging.info(self.DoorName + "'s Garage Door has been Open for 15 minutes")
                    self.DoorOpenTimerMessageSent = 1

            if GPIO.input(self.pin1) == GPIO.HIGH and GPIO.input(self.pin2) == GPIO.HIGH:  #Door Status is Unknown
                logging.info(self.DoorName + "'s Door is Opening/Closing")
                while GPIO.input(self.pin1) == GPIO.HIGH and GPIO.input(self.pin2) == GPIO.HIGH:
                    if _running() == False:
                        break
                    time.sleep(.5)
                else:
                    if GPIO.input(self.pin1) == GPIO.LOW:  #Door is Closed
                        logging.info(self.DoorName + "'s Door is Closed")
                        self.DoorOpenTimer = 0

                    if GPIO.input(self.pin2) == GPIO.LOW:  #Door is Open
                        logging.info(self.DoorName + "'s Door is Open")
                        #Start Door Open Timer
                        self.TimeDoorOpened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
                        self.DoorOpenTimer = 1
                        self.DoorOpenTimerMessageSent = 0
            else:
                if GPIO.input(self.pin1) == GPIO.LOW and self.DoorOpenTimer == -1:  #Door is Closed
                    logging.info(self.DoorName + "'s Door is Closed")
                    self.DoorOpenTimer = 0

                if GPIO.input(self.pin2) == GPIO.LOW and self.DoorOpenTimer != 1:  #Door is Open
                    logging.info(self.DoorName + "'s Door is Open")
                    #Start Door Open Timer
                    self.TimeDoorOpened = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
                    self.DoorOpenTimer = 1
                    self.DoorOpenTimerMessageSent = 0

        if _running() == False:
            logging.debug(self.DoorName + " terminating")
            

# Create Garage Door instances
Door1 = GarageDoor("Christy", 16, 18)
Door2 = GarageDoor("Gary", 32, 36)
# Each instance does some GPIO setup so small delay to allow the device to get set.
time.sleep(1)

# Threads are clear to run
_running = True

# Create a thread to monitor each door
Door_1_Thread = threading.Thread(target=Door1.run, args = (lambda : _running, ))
Door_2_Thread = threading.Thread(target=Door2.run, args = (lambda : _running, ))

# Wrapped to catch CTRL-C event
try:
    # Start monitoring the doors
    Door_1_Thread.start()
    Door_2_Thread.start()
    # Wait for threads to finish
    Door_1_Thread.join()
    Door_2_Thread.join()

except KeyboardInterrupt:
    _running = False
    # Give the threads a chance to exit
    logging.info("Shutting down the door monitors")
    while threading.active_count() > 1:
        logging.info(threading.active_count())
        time.sleep(.5)
    logging.info("Program Shutdown -- Goodbye!")
    GPIO.cleanup()

