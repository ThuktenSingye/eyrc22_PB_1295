'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2A   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2a.py
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

# Team ID:			[ 1295 ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_2a.py
# Functions:		control_logic, detect_distance_sensor_1, detect_distance_sensor_2
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
##############################################################

def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to actuate the rotary joints of the robot in this function, such that
	it traverses the points in given order

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

	# define
	left_joint = sim.getObject("./left_joint")
	right_joint = sim.getObject("./right_joint")

	# constants
	turn_count = 0
	max_speed = 6
	spike_speed = 0.4
	front_max = 0.4

	# making rotations
	def rotate(lj, rj, side):
		# rotate speed
		rotate_speed = 2

		# rotate right
		if side != -1:
			sim.setJointTargetVelocity(lj,-rotate_speed)
			sim.setJointTargetVelocity(rj, rotate_speed)				
			time.sleep(0.5)
			# extra turn if need
			side_1 = round(detect_distance_sensor_2(sim), 3)
			side_2 = round(detect_distance_sensor_3(sim), 3)
			threshold = 0.5
			alpha = 0.1
			if (side_1-side_2)>threshold:
				sim.setJointTargetVelocity(lj,-alpha)
				sim.setJointTargetVelocity(rj, alpha)
			elif (side_1-side_2)<-threshold:
				sim.setJointTargetVelocity(lj, alpha)
				sim.setJointTargetVelocity(rj,-alpha)

		# rotate left
		else:
			sim.setJointTargetVelocity(lj, rotate_speed)
			sim.setJointTargetVelocity(rj,-rotate_speed)
			time.sleep(0.6)

	
	stop = False
	while not stop:
		# get the readings
		distance_1 = round(detect_distance_sensor_1(sim), 3)
		distance_2 = round(detect_distance_sensor_2(sim), 3)
		distance_3 = round(detect_distance_sensor_3(sim), 3)

		# code for rotation
		if distance_1 != -1:
			sim.setJointTargetVelocity(left_joint, max_speed)
			sim.setJointTargetVelocity(right_joint, max_speed)

			# if front distance within threshold
			if distance_1<front_max:
				if distance_2 != -1:
					# stop the robot and the simulation
					if turn_count == 9:
						sim.setJointTargetVelocity(left_joint, 0)
						sim.setJointTargetVelocity(right_joint, 0)
						stop = True

					# rotate left
					else:
						rotate(left_joint, right_joint, distance_2)	
						turn_count += 1
				else:
					# rotate right
					rotate(left_joint, right_joint, distance_2)
					turn_count +=  1
						
		# code for path traversal
		else:
			# maintain path
			if (distance_2 != distance_3):
				# drive left 
				if (distance_2>distance_3):
					sim.setJointTargetVelocity(left_joint, max_speed+spike_speed)
					sim.setJointTargetVelocity(right_joint, max_speed)

				# drive right
				else:
					sim.setJointTargetVelocity(left_joint, max_speed)
					sim.setJointTargetVelocity(right_joint, max_speed+spike_speed)
			
			# drive straight
			else:
				sim.setJointTargetVelocity(left_joint, max_speed)
				sim.setJointTargetVelocity(right_joint, max_speed)
	#################################################

def detect_distance_sensor_1(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_1'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_1 = detect_distance_sensor_1(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############

	p_sensor_1 = sim.getObject("./distance_sensor_1")
	distance_1 = sim.readProximitySensor(p_sensor_1)
	distance_1 = distance_1[1]

	if distance_1 != 0:
		distance = distance_1
	else:
		distance = -1

	##################################################
	return distance

def detect_distance_sensor_2(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_2'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_2 = detect_distance_sensor_2(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############

	p_sensor_2 = sim.getObject("./distance_sensor_2")
	distance_2 = sim.readProximitySensor(p_sensor_2)
	distance_2 = distance_2[1]

	if distance_2 != 0:
		distance = distance_2
	else:
		distance = -1

	##################################################
	return distance

def detect_distance_sensor_3(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_1'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_1 = detect_distance_sensor_1(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############

	p_sensor_3 = sim.getObject("./distance_sensor_3")
	distance_3 = sim.readProximitySensor(p_sensor_3)
	distance_3 = distance_3[1]

	if distance_3 != 0:
		distance = distance_3
	else:
		distance = -1

	##################################################
	return distance

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
			control_logic(sim)
			time.sleep(5)

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
