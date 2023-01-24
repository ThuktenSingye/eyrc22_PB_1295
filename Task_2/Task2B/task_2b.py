'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2B   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2b.py
*  Created:				
*  Last Modified:		8/10/2022
*  Author:				e-Yantra Team
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_2b.py
# Functions:		control_logic, read_qr_code
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import  sys
import traceback
import time
import os
import math
from zmqRemoteApi import RemoteAPIClient
import zmq
import numpy as np
import cv2
import random
from pyzbar.pyzbar import decode
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
def decode_and_deliver(sim, nodeCount):

	arena_dummy_handle = sim.getObject("/Arena_dummy") 
	childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")

	if nodeCount == 5:
		sim.callScriptFunction("activate_qr_code", childscript_handle, "checkpoint E")
		package = read_qr_code(sim)
		print("Decoded QR message: ",package)
		if package == "Orange Cone":
			package = "package_1"
		elif package == "Blue Cylinder":
			package = "package_2"
		elif package == "Pink Cuboid":
			package = "package_3"
		sim.callScriptFunction("deliver_package", childscript_handle, f'{package}', "checkpoint E")
		sim.callScriptFunction("deactivate_qr_code", childscript_handle, "checkpoint E")
	elif nodeCount == 9:
		sim.callScriptFunction("activate_qr_code", childscript_handle, "checkpoint I")
		package = read_qr_code(sim)
		print("Decoded QR message: ",package)
		if package == "Orange Cone":
			package = "package_1"
		elif package == "Blue Cylinder":
			package = "package_2"
		elif package == "Pink Cuboid":
			package = "package_3"
		sim.callScriptFunction("deliver_package", childscript_handle, f'{package}', "checkpoint I")
		sim.callScriptFunction("deactivate_qr_code", childscript_handle, "checkpoint I")
		
	elif nodeCount == 13:
		sim.callScriptFunction("activate_qr_code", childscript_handle, "checkpoint M")
		package = read_qr_code(sim)
		print("Decoded QR message: ",package)
		if package == "Orange Cone":
			package = "package_1"
		elif package == "Blue Cylinder":
			package = "package_2"
		elif package == "Pink Cuboid":
			package = "package_3"
		sim.callScriptFunction("deliver_package", childscript_handle, f'{package}', "checkpoint M")
		sim.callScriptFunction("deactivate_qr_code", childscript_handle, "checkpoint M")


def align(sim, contours):
    trackArea= cv2.minAreaRect(contours)
    _,(w_min, h_min) , ang = trackArea
    if w_min < h_min:
        ang = 90 - ang
    else:
        ang = -ang
    ang = int(ang)
    if ang > 0 and ang <88:
        sim.setJointTargetVelocity(leftJoint, 0)
        sim.setJointTargetVelocity(rightJoint, 1.5)
    elif ang < 0 and ang > -88:
        sim.setJointTargetVelocity(leftJoint, 1.5)
        sim.setJointTargetVelocity(rightJoint, 0)          
    else:
        travelStraight(sim, contours)

def rotateRight(sim):
    sim.setJointTargetVelocity(leftJoint , omega)
    sim.setJointTargetVelocity(rightJoint, -omega)
def rotateLeft(sim):
    sim.setJointTargetVelocity(leftJoint , -omega)
    sim.setJointTargetVelocity(rightJoint, omega)

def travelStraight(sim, contours_white):
    M = cv2.moments(contours_white)
    if M['m00']!=0:
        cx= int(M['m10']/M['m00'])
        if cx < 250:
            sim.setJointTargetVelocity(leftJoint, minSpeed)
            sim.setJointTargetVelocity(rightJoint, maxSpeed)
        elif cx > 260:
            sim.setJointTargetVelocity(leftJoint, maxSpeed)
            sim.setJointTargetVelocity(rightJoint, minSpeed)
        elif cx < 260 and cx > 250:
            forward(sim=sim)
def region_of_interest(image):
    height = image.shape[0]
    width = image.shape[1]
    rect = np.array([[(0, height), (0, 0), (width, 0), (width, height)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, rect, 255)
    maskedImage = cv2.bitwise_and(image, mask)
    return maskedImage
def stop(sim):
    sim.setJointTargetVelocity(leftJoint , 0)
    sim.setJointTargetVelocity(rightJoint, 0)
def forward(sim):
	sim.setJointTargetVelocity(leftJoint, maxSpeed)
	sim.setJointTargetVelocity(rightJoint, maxSpeed)
def forward_min(sim):
	sim.setJointTargetVelocity(leftJoint, 2)
	sim.setJointTargetVelocity(rightJoint, 2)

def check_area(cnt):
    area = cv2.contourArea(cnt)
    if area < 2000 and area > 1000:
        return True
    return False


##############################################################

def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to make the robot follow the line to cover all the checkpoints
	and deliver packages at the correct locations.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	None

	Example call:
	---
	control_logic(sim)
	"""
	##############  ADD YOUR CODE HERE  ##############
	global leftJoint, rightJoint, omega, minSpeed, maxSpeed, vision_sensor, minOmega
	leftJoint = sim.getObject("/left_joint")
	rightJoint = sim.getObject("/right_joint")
	vision_sensor = sim.getObject('/vision_sensor')
	nodeDetected = False
	nodeIncremented = False
	minOmega = 1.875
	omega = 2
	nodeCount = 0
	turn = False
	maxSpeed = 4.5
	minSpeed = 3.785
	path = {1:"A",2:"B", 3:"C",4:"D", 5:"E", 6:"F", 7:"G", 8:"H", 9:"I", 10:"J", 11:"K", 12:"L", 13:"M", 14:"N", 15:"O", 16:"P", 17:"A" }
	forward(sim)

	while True:
		frame, res = sim.getVisionSensorImg(vision_sensor) #
		resX, resY = res
		frame = np.frombuffer(frame, dtype=np.uint8).reshape(resY, resX, 3) 
		yellowFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		yellowNode = cv2.inRange(yellowFrame, (80, 70, 50), (100, 255, 255))
		contours_yellow, hierarchy_yel = cv2.findContours(yellowNode.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(grayFrame,(5,5),0)
		_, thresh = cv2.threshold(blur, 240, 255, cv2.THRESH_BINARY) 
		canny = cv2.Canny(thresh, 50, 150)
		crop_image = region_of_interest(canny)
		contours_rotate,_ = cv2.findContours(crop_image[0:500,:], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		contours_white,_ = cv2.findContours(crop_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
		if len(contours_yellow) > 0: 
			if not nodeIncremented:
				nodeCount+=1
				nodeIncremented = True
			if not nodeDetected:
				node= cv2.minAreaRect(contours_yellow[0])
				y_min= node[0][1]
				if  y_min <215:
					stop(sim)
					print(f'Current Checkpoint: {path[nodeCount]}')
					#decode_and_deliver(sim, nodeCount)
					nodeDetected = True
					time.sleep(0.2)
				
		if nodeDetected and len(contours_yellow) == 0: 
			if nodeCount == 5 or nodeCount == 9 or nodeCount == 13:
				print(f'Current Checkpoint: {path[nodeCount]}')
				nodeCount+=1
				nodeDetected = False
				forward(sim)
			elif nodeCount == 17:
				stop(sim)
				break
			else:
				contour_len = []
				for cnt in contours_rotate:
					if check_area(cnt):
						contour_len.append(cnt)
				if not turn:
					if  len(contour_len)==1 : 
						if  nodeCount%2 == 0 and nodeCount <=17 : 
							rotateRight(sim)
						elif nodeCount%2 ==1 and nodeCount <=17 : 
							rotateLeft(sim)
					if len(contour_len)==0:
						turn = True
				if turn:
					contour_len = []
					for cnt in contours_rotate:
						if check_area(cnt):
							contour_len.append(cnt)
					if len(contour_len) >=1:
						for cnt in contours_white:
							if check_area(cnt):
								M = cv2.moments(cnt)
								if M['m00']!=0:
									cx= int(M['m10']/M['m00'])
									if cx < 300 and cx > 220:
										stop(sim)
										nodeDetected = False
										turn = False
										nodeIncremented = False
				
					if  nodeCount%2 == 0 and nodeCount <=17 : 
						rotateRight(sim)
					elif nodeCount%2 ==1 and nodeCount <=17 : 
						rotateLeft(sim)
		elif nodeDetected and len(contours_white)!=0:
			forward_min(sim)
		else:
			if nodeCount ==5 or nodeCount== 9 or nodeCount == 13:
				sim.setJointTargetVelocity(leftJoint, 1.5)
				sim.setJointTargetVelocity(rightJoint, 1.5)
			else:
				midOne =[]
				for cnt in contours_white:
					if check_area(cnt):
						midOne.append(cnt)
				if len(midOne) > 0:
					align(sim, midOne[0])
				else:
					forward(sim)
				
	##################################################

def read_qr_code(sim):
	"""
	Purpose:
	---
	This function detects the QR code present in the camera's field of view and
	returns the message encoded into it.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	`qr_message`   :    [ string ]
		QR message retrieved from reading QR code

	Example call:
	---
	control_logic(sim)
	"""
	qr_message = None
	##############  ADD YOUR CODE HERE  ##############
	frame, res = sim.getVisionSensorImg(vision_sensor)
	resX, resY = res
	frame = np.frombuffer(frame, dtype=np.uint8).reshape(resY, resX, 3)
	frame= cv2.flip(frame, 0)

	qrcode = decode(frame)
	qr_message =  (qrcode[0].data).decode()
	
	##################################################
	return qr_message
######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN CODE BELOW #########

if __name__ == "__main__":
	client = RemoteAPIClient()
	sim = client.getObject('sim')	

	try:

		## Start the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.startSimulation()
			if sim.getSimulationState() != sim.simulation_stopped:
				print('\nSimulation started correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be started correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be started !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

		## Runs the robot navigation logic written by participants
		try:
			#time.sleep(5)
			control_logic(sim)

		except Exception:
			print('\n[ERROR] Your control_logic function throwed an Exception, kindly debug your code!')
			print('Stop the CoppeliaSim simulation manually if required.\n')
			traceback.print_exc(file=sys.stdout)
			print()
			sys.exit()

		## Stop the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.stopSimulation()
			time.sleep(0.5)
			if sim.getSimulationState() == sim.simulation_stopped:
				print('\nSimulation stopped correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be stopped correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be stopped !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

	except KeyboardInterrupt:
		## Stop the simulation using ZeroMQ RemoteAPI
		return_code = sim.stopSimulation()
		time.sleep(0.5)
		if sim.getSimulationState() == sim.simulation_stopped:
			print('\nSimulation interrupted by user in CoppeliaSim.')
		else:
			print('\nSimulation could not be interrupted. Stop the simulation manually .')
			sys.exit()
