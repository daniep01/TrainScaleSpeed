#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def my_callback_one(channel):
	print(str(channel) + ' : ' + str(GPIO.input(channel)))

def my_callback_two(channel):
	print(str(channel) + ' : ' + str(GPIO.input(channel)))

GPIO.add_event_detect(17, GPIO.BOTH, bouncetime=40)
GPIO.add_event_detect(18, GPIO.BOTH, bouncetime=40)

GPIO.add_event_callback(17, my_callback_one)
GPIO.add_event_callback(18, my_callback_two)

message = input("Press enter to quit\n\n")

GPIO.remove_event_detect(17)
GPIO.remove_event_detect(18)
GPIO.cleanup()
