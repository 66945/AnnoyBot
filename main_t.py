#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from threading import Thread

import httplink

# Create your objects here.
ev3 = EV3Brick()

leftMotor = Motor(Port.A)
rightMotor = Motor(Port.D)
annoyMotor = Motor(Port.C)

irSensor = InfraredSensor(Port.S4)

# Global variables here.
commands = {
    'driveForward': (1, 1),
    'driveBackward': (-1, -1),
    'forwardLeft': (0, 1),
    'forwardRight': (1, 0),
    'backwardLeft': (0, -1),
    'backwardRight': (-1, 0),
    'turnLeft': (-1, 1),
    'turnRight': (1, -1)
}

# Write your program here.
def drive(leftAngle, rightAngle):
    leftMotor.run_angle(speed=500, rotation_angle=leftAngle, wait=False)
    rightMotor.run_angle(speed=500, rotation_angle=rightAngle, wait=True)

def annoy():
    annoyMotor.run_until_stalled(speed=250, duty_limit=10)
    annoyMotor.reset_angle(0)

    while irSensor.distance() < 20:
        annoyMotor.run_target(speed=500, target_angle=-20, wait=True)
        annoyMotor.run_target(speed=500, target_angle=0, wait=True)
    
    annoyMotor.run_until_stalled(speed=-250, duty_limit=50)
    annoyMotor.reset_angle(0)

def annoyToggle():
    while True:
        while irSensor.distance() > 20:
            pass

        annoy()

def processCommand(text):
    cmd = text.split(',')[0]
    params = text.split(',')[-1:]

    motorValues = list(commands[cmd])
    motorValues[0] *= int(params[0])
    motorValues[1] *= int(params[0])

    drive(motorValues[0], motorValues[1])

def main():
    leftMotor.reset_angle(0)
    rightMotor.reset_angle(0)

    annoyMotor.run_until_stalled(speed=-250, duty_limit=50)
    annoyMotor.reset_angle(0)

    print('annoyer reset')

    annoyThread = Thread(target=annoyToggle)
    annoyThread.start()

    testCmds = [
        'driveForward,720',
        'turnLeft,360',
        'driveForward,720',
        'turnLeft,360',
        'driveForward,720',
        'turnLeft,360'
    ]

    for cmd in testCmds:
        processCommand(cmd)
        print(cmd)

    httplink.request()
    input('Done')

if __name__ == "__main__":
    main()
