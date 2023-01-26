'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3D of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ 1295 ]
# Author List:		[ Aurvin Thara, Thinley Jigme, Kinley Rabgay, Thukten Singye ]
# Filename:			socket_client_rgb.py
# Functions:		
# 					[ set_color ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import socket
import time
import os, sys
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################

# Function to set RGB LED color
def set_color(redPWM, greenPWM, bluePWM, gndPWM, r, g, b, gn):
	redPWM.ChangeDutyCycle(r)
	greenPWM.ChangeDutyCycle(g)
	bluePWM.ChangeDutyCycle(b)
	gndPWM.ChangeDutyCycle(gn)

##############################################################

def setup_client(host, port):

	"""
	Purpose:
	---
	This function creates a new socket client and then tries
	to connect to a socket server.

	Input Arguments:
	---
	`host` :	[ string ]
			host name or ip address for the server

	`port` : [ string ]
			integer value specifying port name
	Returns:

	`client` : [ socket object ]
			   a new client socket object
	---

	
	Example call:
	---
	client = setup_client(host, port)
	""" 

	client = None

	##################	ADD YOUR CODE HERE	##################

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((host, port))

	##########################################################

	return client

def receive_message_via_socket(client):
	"""
	Purpose:
	---
	This function listens for a message from the specified
	socket connection and returns the message when received.

	Input Arguments:
	---
	`client` :	[ socket object ]
			client socket object created by setup_client() function
	Returns:
	---
	`message` : [ string ]
			message received through socket communication
	
	Example call:
	---
	message = receive_message_via_socket(connection)
	"""

	message = None

	##################	ADD YOUR CODE HERE	##################

	message = client.recv(1024).decode("utf-8")

	##########################################################

	return message

def send_message_via_socket(client, message):
	"""
	Purpose:
	---
	This function sends a message over the specified socket connection

	Input Arguments:
	---
	`client` :	[ socket object ]
			client socket object created by setup_client() function

	`message` : [ string ]
			message sent through socket communication

	Returns:
	---
	None
	
	Example call:
	---
	send_message_via_socket(connection, message)
	"""

	##################	ADD YOUR CODE HERE	##################

	client.sendall(message.encode())

	##########################################################

def rgb_led_setup(redPin, greenPin, bluePin, gndPin, freq):
	"""
	Purpose:
	---
	This function configures pins connected to rgb led as output and
	enables PWM on the pins 

	Input Arguments:
	---
	You are free to define input arguments for this function.

	Returns:
	---
	You are free to define output parameters for this function.
	
	Example call:
	---
	rgb_led_setup()
	"""

	##################	ADD YOUR CODE HERE	##################

	# GPIO 
	GPIO.setup(redPin, GPIO.OUT)
	GPIO.setup(greenPin, GPIO.OUT)
	GPIO.setup(bluePin, GPIO.OUT)
	GPIO.setup(gndPin, GPIO.OUT)

	# PWM 
	redPWM = GPIO.PWM(redPin, freq)
	greenPWM = GPIO.PWM(greenPin, freq)
	bluePWM = GPIO.PWM(bluePin, freq)
	gndPWM = GPIO.PWM(gndPin, freq)

	##########################################################

	return redPWM, greenPWM, bluePWM, gndPWM
	
def rgb_led_set_color(color, redPWM, greenPWM, bluePWM, gndPWM):
	"""
	Purpose:
	---
	This function takes the color as input and changes the color of rgb led
	connected to Raspberry Pi 

	Input Arguments:
	---

	`color` : [ string ]
			color detected in QR code communicated by server
	
	You are free to define any additional input arguments for this function.

	Returns:
	---
	You are free to define output parameters for this function.
	
	Example call:
	---
	rgb_led_set_color(color)
	"""    
	
	##################	ADD YOUR CODE HERE	##################

	# Initialization
	red_PWM.start(0)
	green_PWM.start(0)
	blue_PWM.start(0)
	gnd_PWM.start(0)

	# Condition
	if color == "Red":
		set_color(redPWM, greenPWM, bluePWM, gndPWM, 100, 0, 0, 0)
		print('100, 0, 0')

	elif color == "Blue":
		set_color(redPWM, greenPWM, bluePWM, gndPWM, 0, 0, 100, 0)
		print('0, 0, 100')

	elif color == "Green":
		set_color(redPWM, greenPWM, bluePWM, gndPWM, 0, 100, 0, 0)
		print('0, 100, 0')

	elif color == "Orange":
		set_color(redPWM, greenPWM, bluePWM, gndPWM, 100, 13, 0, 0)
		print('100, 13, 0')

	elif color == "Pink":
		set_color(redPWM, greenPWM, bluePWM, gndPWM, 100, 0, 47, 0)
		print('100, 0, 47')

	elif color == "Sky Blue":
		set_color(redPWM, greenPWM, bluePWM, gndPWM, 0, 39, 39, 0)
		print('0, 39, 39')

	##########################################################

if __name__ == "__main__":

		host = "192.168.1.11"
		port = 5050

		## 
		redPin = 24
		gndPin = 23
		greenPin = 5
		bluePin = 18
		freq = 100

		## PWM values to be set for rgb led to display different colors
		pwm_values = {"Red": (255, 0, 0), "Blue": (0, 0, 255), "Green": (0, 255, 0), "Orange": (255, 35, 0), "Pink": (255, 0, 122), "Sky Blue": (0, 100, 100)}


		## Configure rgb led pins
		red_PWM, green_PWM, blue_PWM, gnd_PWM = rgb_led_setup(redPin, greenPin, bluePin, gndPin, freq)

		## Set up new socket client and connect to a socket server
		try:
			client = setup_client(host, port)

		except socket.error as error:
			print("Error in setting up server")
			print(error)
			sys.exit()

		## Wait for START command from socket_server_rgb.py
		message = receive_message_via_socket(client)
		if message == "START":
			print("\nTask 3D Part 3 execution started !!")

		while True:
			## Receive message from socket_server_rgb.py
			message = receive_message_via_socket(client)

			## If received message is STOP, break out of loop
			if message == "STOP":
				print("\nTask 3D Part 3 execution stopped !!")
				break
			else:
				print("Color received: " + message)
				rgb_led_set_color(message, red_PWM, green_PWM, blue_PWM,gnd_PWM)

		red_PWM.stop()
		blue_PWM.stop()
		green_PWM.stop()
		GPIO.cleanup()