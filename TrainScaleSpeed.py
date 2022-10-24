#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

t1 = 0
t2 = 0
run = 0

running_stop = 0
running_left = 1
running_right = 2

minimum_time_between_runs = 4

running_state = running_stop

time_of_last_measurement = 0

distance_inches = 32
oo_scale = 76.2

print('Speed calculated assuming ' + str(distance_inches) + 'inches between track sensors')

def my_callback_one(channel):
	global t1, t2, running_state, time_of_last_measurement, run
	# print(str(channel) + ' : ' + str(GPIO.input(channel)))

	if GPIO.input(channel) == 0:
		
		if running_state == running_left:
			t2 = time.time()
			time_elapsed = (t2 - t1)
		
			running_state = running_stop
			print('Stop  Timer A at ' + str(t2))
			time_of_last_measurement = time.time()
			calculate_speed(time_elapsed)
	
		elif running_state == running_stop:
			t1 = time.time()
			
			if t1 - time_of_last_measurement > minimum_time_between_runs:
				# avoid false restarts
				running_state = running_right
				run = run + 1
				print("Running A to B ", run)
				print('Start Timer A at ' + str(t1))
			else:
				print('Ignoring false restart A')
	
	
def my_callback_two(channel):
	global t1, t2, running_state, time_of_last_measurement, run
	# print(str(channel) + ' : ' + str(GPIO.input(channel)))

	if GPIO.input(channel) == 0:
		
		if running_state == running_right:
			t2 = time.time()
			time_elapsed = (t2 - t1)

			running_state = running_stop
			print('Stop  Timer B at ' + str(t2))
			time_of_last_measurement = time.time()
			calculate_speed(time_elapsed)

		elif running_state == running_stop:
			t1 = time.time()
			
			if t1 - time_of_last_measurement > minimum_time_between_runs:
				# avoid false restarts
				running_state = running_left
				run = run + 1
				print("Running B to A ", run)
				print('Start Timer B at ' + str(t1))
			else:
				print('Ignoring false restart B')
	
		
def calculate_speed(time_elapsed):
	
	print('>>> ' + str(round(time_elapsed,2)) + ' seconds elapsed')
	
	
	inch_per_hour = (distance_inches / time_elapsed) * 3600
	scale_inch_per_hour = inch_per_hour * oo_scale
	scale_mph = round((scale_inch_per_hour / 63360),1)
	
	print('>>> ' + str(scale_mph) + ' mph at OO scale speed')
	print('---')

GPIO.add_event_detect(17, GPIO.BOTH, bouncetime=40)
GPIO.add_event_detect(18, GPIO.BOTH, bouncetime=40)

GPIO.add_event_callback(17, my_callback_one)
GPIO.add_event_callback(18, my_callback_two)

message = input("Press enter to quit\n\n")

GPIO.remove_event_detect(17)
GPIO.remove_event_detect(18)
GPIO.cleanup()
