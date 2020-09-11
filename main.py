#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time

from threading import Thread

import httplink

import os
os.system('setfont Lat15-TerminusBold32x16')

# Create your objects here.
leftMotor = ev3.LargeMotor(ev3.OUTPUT_A)#Motor(Port.A)
rightMotor = ev3.LargeMotor(ev3.OUTPUT_D)#Motor(Port.D)
annoyMotor = ev3.LargeMotor(ev3.OUTPUT_C)#Motor(Port.C)

assert leftMotor.connected
assert rightMotor.connected
assert annoyMotor.connected

irSensor = ev3.InfraredSensor()

assert irSensor

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
    leftMotor.run_to_rel_pos(speed_sp=500, position_sp=leftAngle)
    rightMotor.run_to_rel_pos(speed_sp=500, position_sp=rightAngle)

    leftMotor.wait_while(ev3.Motor.STATE_RUNNING)
    rightMotor.wait_while(ev3.Motor.STATE_RUNNING)

def annoy():
    # annoyMotor.run_forever(speed_sp=50)
    # while not annoyMotor.is_stalled:
    #     pass
    # annoyMotor.stop()

    while irSensor.proximity < 20:
        annoyMotor.run_to_rel_pos(speed_sp=500, position_sp=25)
        annoyMotor.wait_while(ev3.Motor.STATE_RUNNING)

        annoyMotor.run_to_rel_pos(speed_sp=500, position_sp=-25)
        annoyMotor.wait_while(ev3.Motor.STATE_RUNNING)
    
    annoyMotor.run_forever(speed_sp=-50)
    while not annoyMotor.is_stalled:
        pass
    annoyMotor.stop()

def annoyToggle():
    while True:
        while irSensor.proximity > 20:
            pass

        annoy()

def getCommands():
    while True:
        cmd = httplink.getCommand()
        cmd = cmd[0]

        processCommand(cmd)

def processCommand(text):
    cmd = text.split(',')[0]
    params = text.split(',')[-1:]

    if cmd in commands:
        motorValues = list(commands[cmd])
        motorValues[0] *= int(params[0])
        motorValues[1] *= int(params[0])

        drive(motorValues[0], motorValues[1])

def main():
    annoyMotor.run_forever(speed_sp=-50)
    while not annoyMotor.is_stalled:
        pass
    annoyMotor.stop()

    print('annoyer reset')

    annoyThread = Thread(target=annoyToggle)
    annoyThread.start()

    httplink.start('Dad')
    print(httplink.session)
    print(httplink.userPassword)
    
    getCommands()

    input('Done')

if __name__ == "__main__":
    main()