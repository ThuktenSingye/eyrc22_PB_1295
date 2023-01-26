'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*
*  This script is intended for implementation of Task 4A
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_4a.py
*  Created:
*  Last Modified:		02/01/2023
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
# Author List:		[ Kinley Rabgay, Thinley Jigme, Aurbin Thara, Thukten Singye ]
# Filename:			task_4a.py
# Functions:		[ Comma separated list of functions in this file ]
# 					
####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import numpy as np
import cv2
from zmqRemoteApi import RemoteAPIClient
import zmq
import os
import time
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################


##############################################################

def place_packages(medicine_package_details, sim, all_models):
    """
	Purpose:
	---
	This function takes details (colour, shape and shop) of the packages present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The packages should be inserted only into the 
    designated areas in each shop as mentioned in the Task document.

    Functions from Regular API References should be used to set the position of the 
    packages.

	Input Arguments:
	---
	`medicine_package_details` :	[ list ]
                                nested list containing details of the medicine packages present.
                                Each element of this list will contain 
                                - Shop number as Shop_n
                                - Color of the package as a string
                                - Shape of the package as a string
                                - Centroid co-ordinates of the package			

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	
	Example call:
	---
	all_models = place_packages(medicine_package_details, sim, all_models)
	"""
    models_directory = os.getcwd()
    packages_models_directory = os.path.join(models_directory, "package_models")
    arena = sim.getObject('/Arena')    
####################### ADD YOUR CODE HERE #########################
    
    shop1_start_coord = 111.03125
    shop2_start_coord = 211.03125
    shop3_start_coord = 311.03125
    shop4_start_coord = 411.03125
    shop5_start_coord = 511.03125
    c_x = 0
    c_y = (150.625-344) * 0.89 / 250
    model=""
    shape = ""

    for i in medicine_package_details:

        if str(i[2]).lower()=='circle':
            shape = 'cylinder'
            model = os.path.join(packages_models_directory,f'{i[1]}_cylinder.ttm')
        if str(i[2]).lower()=='triangle':
            shape = 'cone'
            model = os.path.join(packages_models_directory,f'{i[1]}_cone.ttm')
        if str(i[2]).lower()=='square':
            shape = 'cube'
            model = os.path.join(packages_models_directory,f'{i[1]}_cube.ttm')
        model_handle = sim.loadModel(model)
        sim.setObjectParent(model_handle, arena, True)
        sim.setObjectAlias(model_handle, f'{i[1]}_{shape}')
        
        if i[0]=='Shop_1':
            c_x= (344-shop1_start_coord) * 0.89 / 250
            #sim.setObjectPosition(model_handle, -1, [c_x, c_y, 0.0150])
            shop1_start_coord+=22.5
        if i[0]=='Shop_2':
            c_x= (344-shop2_start_coord) * 0.89 / 250
            #sim.setObjectPosition(model_handle, -1, [c_x, c_y, 0.0150])
            shop2_start_coord+= 22.5
        
        if i[0]=='Shop_3':
            c_x= (344-shop3_start_coord) * 0.89 / 250
            #sim.setObjectPosition(model_handle, -1, [c_x, c_y, 0.0150])
            shop3_start_coord+=22.5
        if i[0]=='Shop_4':
            c_x= (344-shop4_start_coord) * 0.89 / 250
            #sim.setObjectPosition(model_handle, -1, [c_x, c_y, 0.0150])
            shop4_start_coord+=22.5
        if i[0]=='Shop_5':
            c_x= (344-shop5_start_coord) * 0.89 / 250
            shop5_start_coord+=22.5
        sim.setObjectPosition(model_handle, -1, [c_x, c_y, 0.0150])
        all_models.append(model_handle)

###################################################################
    return all_models


def place_traffic_signals(traffic_signals, sim, all_models):
    """
	Purpose:
	---
	This function takes position of the traffic signals present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    them on the virtual arena. The signal should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    signals.

	Input Arguments:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	None
	
	Example call:
	---
	all_models = place_traffic_signals(traffic_signals, sim, all_models)
	"""
    models_directory = os.getcwd()
    traffic_sig_model = os.path.join(models_directory, "signals", "traffic_signal.ttm" )
    arena = sim.getObject('/Arena')   
####################### ADD YOUR CODE HERE #########################
    task_1 = __import__('task_1a')
    output = []
    _,_,x_dict,y_dict = task_1.get_unit(task_1.getImage())
    x_coord=[]
    y_coord=[]
    result = []
    for i in range(len(traffic_signals)):
        x_coord.append(list(traffic_signals[i][0]))
        y_coord.append(list(traffic_signals[i][1]))
    for i in range(len(x_coord)):
        result.append([x_coord[i],y_coord[i]])

    for i in range(len(result)):
        x= x_dict["".join(result[i][0])]
        y= y_dict["".join(result[i][1])]
        c_x = (344-x) * 0.89 / 250
        c_y = (y-344) * 0.89 / 250
        output.append([c_x,c_y])

    for i in range(len(output)):
        traffic_node_handle = sim.loadModel(traffic_sig_model)
        sim.setObjectAlias(traffic_node_handle,f'Signal_{traffic_signals[i]}')
        sim.setObjectParent(traffic_node_handle, arena, True)
        sim.setObjectPosition(traffic_node_handle, -1, [output[i][0],output[i][1],0.15588])
        all_models.append(traffic_node_handle)

####################################################################
    return all_models

def place_start_end_nodes(start_node, end_node, sim, all_models):
    """
	Purpose:
	---
	This function takes position of start and end nodes present in 
    the arena and places them on the virtual arena. 
    The models should be inserted at a particular node.

    Functions from Regular API References should be used to set the position of the 
    start and end nodes.

	Input Arguments:
	---
	`start_node` : [ string ]
    `end_node` : [ string ]
					

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
	"""
    models_directory = os.getcwd()
    start_node_model = os.path.join(models_directory, "signals", "start_node.ttm" )
    end_node_model = os.path.join(models_directory, "signals", "end_node.ttm" )
    arena = sim.getObject('/Arena')   
####################### ADD YOUR CODE HERE #########################
    task_1 = __import__('task_1a')
    start_node_handle = sim.loadModel(start_node_model)

    _,_,x_dict,y_dict = task_1.get_unit(task_1.getImage())
    start_node_x = x_dict["".join(start_node[0])]
    start_node_y= y_dict["".join(start_node[1])]
    #print("Start node x and y", start_node_x, start_node_y)
    s_x = (344-start_node_x) * 0.89 / 250
    s_y = (start_node_y-344) * 0.89 / 250
    
    #End node
    end_node_handle = sim.loadModel(end_node_model)
   
    end_node_x = x_dict["".join(end_node[0])]
    end_node_y= y_dict["".join(end_node[1])]
    #print("Start node x and y", start_node_x, start_node_y)
    e_x = (344-end_node_x) * 0.89 / 250
    e_y = (end_node_y-344) * 0.89 / 250
    sim.setObjectParent(start_node_handle, arena, True)
    sim.setObjectParent(end_node_handle, arena, True)
    sim.setObjectAlias(start_node_handle,'Start_Node')
    sim.setObjectAlias(end_node_handle,'End_Node')
    sim.setObjectPosition(start_node_handle, -1, [s_x,s_y,0.15588])
    sim.setObjectPosition(end_node_handle, -1, [e_x,e_y,0.15588])
    all_models.append(end_node_handle)
    all_models.append(start_node_handle)

####################################################################
    return all_models

def place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing horizontal roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    horizontal barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    horizontal barricades.

	Input Arguments:
	---s_x = (344-start_node_x) * 0.89 / 250
    s_y = (start_node_y-344) * 0.89 / 250
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    horiz_barricade_model = os.path.join(models_directory, "barricades", "horizontal_barricade.ttm" )
    arena = sim.getObject('/Arena')  
####################### ADD YOUR CODE HERE #########################
    task_1 = __import__('task_1a')
    _,_,x_dict,y_dict = task_1.get_unit(task_1.getImage())

    for i in range(len(horizontal_roads_under_construction)):
        start = str(horizontal_roads_under_construction[i]).split('-')[0]
        end =str(horizontal_roads_under_construction[i]).split('-')[1]

        start_x= x_dict["".join(start[0])]
        end_x = x_dict["".join(end[0])]
        y = y_dict[''.join(start[1])]
        s_x = (344-start_x) * 0.89 / 250
        e_x = (344-end_x) * 0.89 / 250
        s_x= (s_x+e_x) /2
        s_y = (y-344) * 0.89 / 250
        horiz_barricade_handle = sim.loadModel(horiz_barricade_model)
        sim.setObjectAlias(horiz_barricade_handle,f'Horizontal_missing_road_{start}_{end}')
        sim.setObjectParent(horiz_barricade_handle, arena, True)
        #sim.setObjectPosition(horiz_barricade_handle, -1, [0,y, 0.003])
        sim.setObjectPosition(horiz_barricade_handle, -1, [s_x,s_y,0.003])
        all_models.append(horiz_barricade_handle)

    
####################################################################
    return all_models


def place_vertical_barricade(vertical_roads_under_construction, sim, all_models):
    """
	Purpose:
	---
	This function takes the list of missing vertical roads present in 
    the arena (using "detect_arena_parameters" function from task_1a.py) and places
    vertical barricades on virtual arena. The barricade should be inserted 
    between two nodes as shown in Task document.

    Functions from Regular API References should be used to set the position of the 
    vertical barricades.

	Input Arguments:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links		

    `sim` : [ object ]
            ZeroMQ RemoteAPI object

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	Returns:

    `all_models` : [ list ]
            list containing handles of all the models imported into the scene
	---
	None
	
	Example call:
	---
	all_models = place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
	"""
    models_directory = os.getcwd()
    vert_barricade_model = os.path.join(models_directory, "barricades", "vertical_barricade.ttm" )
    arena = sim.getObject('/Arena') 
    #print("The type of model", type(all_models))
####################### ADD YOUR CODE HERE #########################
    task_1 = __import__('task_1a')
    _,_,x_dict,y_dict = task_1.get_unit(task_1.getImage())
    for i in range(len(vertical_roads_under_construction)):
        start = str(vertical_roads_under_construction[i]).split('-')[0]
        end =str(vertical_roads_under_construction[i]).split('-')[1]
        start_y= y_dict["".join(start[1])]
        end_y = y_dict["".join(end[1])]
        x = x_dict[''.join(start[0])]
        s_y = (start_y-344) * 0.89 / 250
        e_y = (end_y-344) * 0.89 / 250
        s_y= (s_y+e_y) / 2
        s_x = (344-x) * 0.89 / 250
        vert_barricade_handle = sim.loadModel(vert_barricade_model)
        sim.setObjectAlias(vert_barricade_handle,f'Vertical_missing_road_{start}_{end}')
        sim.setObjectParent(vert_barricade_handle, arena, True)
        sim.setObjectPosition(vert_barricade_handle, -1, [s_x,s_y,0.003])
        all_models.append(vert_barricade_handle)
####################################################################
    return all_models

if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')

    # path directory of images in test_images folder
    img_dir = os.getcwd() + "/test_imgs/"

    i = 0

    config_img = cv2.imread(img_dir + 'maze_' + str(i) + '.png')

    print('\n============================================')
    print('\nFor maze_0.png')

    # object handles of each model that gets imported to the scene can be stored in this list
    # at the end of each test image, all the models will be removed    
    all_models = []

    # import task_1a.py. Make sure that task_1a.py is in same folder as task_4a.py
    task_1 = __import__('task_1a')
    detected_arena_parameters = task_1.detect_arena_parameters(config_img)

    # obtain required arena parameters
    medicine_package_details = detected_arena_parameters["medicine_packages"]
    traffic_signals = detected_arena_parameters['traffic_signals']
    start_node = detected_arena_parameters['start_node']
    end_node = detected_arena_parameters['end_node']
    horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
    vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction'] 

    print("[1] Setting up the scene in CoppeliaSim")
    all_models = place_packages(medicine_package_details, sim, all_models)
    all_models = place_traffic_signals(traffic_signals, sim, all_models)
    all_models = place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
    all_models = place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
    all_models = place_start_end_nodes(start_node, end_node, sim, all_models)
    print("[2] Completed setting up the scene in CoppeliaSim")

    # wait for 10 seconds and then remove models
    time.sleep(10)
    print("[3] Removing models for maze_0.png")

    for i in all_models:
        sim.removeModel(i)


    choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')
    
    if choice == 'y':
        for i in range(1,5):

            print('\n============================================')
            print('\nFor maze_' + str(i) +'.png')
            config_img = cv2.imread(img_dir + 'maze_' + str(i) + '.png')

            # object handles of each model that gets imported to the scene can be stored in this list
            # at the end of each test image, all the models will be removed    
            all_models = []

            # import task_1a.py. Make sure that task_1a.py is in same folder as task_4a.py
            task_1 = __import__('task_1a')
            detected_arena_parameters = task_1.detect_arena_parameters(config_img)

            # obtain required arena parameters
            medicine_package_details = detected_arena_parameters["medicine_packages"]
            traffic_signals = detected_arena_parameters['traffic_signals']
            start_node = detected_arena_parameters['start_node']
            end_node = detected_arena_parameters['end_node']
            horizontal_roads_under_construction = detected_arena_parameters['horizontal_roads_under_construction']
            vertical_roads_under_construction = detected_arena_parameters['vertical_roads_under_construction'] 

            print("[1] Setting up the scene in CoppeliaSim")
            place_packages(medicine_package_details, sim, all_models)
            place_traffic_signals(traffic_signals, sim, all_models)
            place_horizontal_barricade(horizontal_roads_under_construction, sim, all_models)
            place_vertical_barricade(vertical_roads_under_construction, sim, all_models)
            place_start_end_nodes(start_node, end_node, sim, all_models)
            print("[2] Completed setting up the scene in CoppeliaSim")

            # wait for 10 seconds and then remove models
            time.sleep(10)
            print("[3] Removing models for maze_" + str(i) + '.png')
            for i in all_models:
                sim.removeModel(i)
            