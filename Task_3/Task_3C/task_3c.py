'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3C of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			task_3c.py
# Functions:		[ perspective_transform, transform_values, set_values ]
# 					


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the five available  ##
## modules for this task                                    ##
##############################################################
import cv2 
import numpy 
from  numpy import interp
from zmqRemoteApi import RemoteAPIClient
import zmq
##############################################################

#################################  ADD UTILITY FUNCTIONS HERE  #######################


#####################################################################################

def perspective_transform(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the image after 
    applying perspective transform on it. Using this function, you should
    crop out the arena from the full frame you are receiving from the 
    overhead camera feed.

    HINT:
    Use the ArUco markers placed on four corner points of the arena in order
    to crop out the required portion of the image.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library 

    Returns:
    ---
    `warped_image` : [ numpy array ]
            return cropped arena image as a numpy array
    
    Example call:
    ---
    warped_image = perspective_transform(image)
    """   
    warped_image = [] 
#################################  ADD YOUR CODE HERE  ###############################
    topLeft = [0,0]
    topRight = [512,0]
    bottomLeft = [0,512]
    bottomRight = [512,512]
    _, ArUco_corners = task_1b.detect_ArUco_details(image)
    for id, value in ArUco_corners.items():
        if id == 1:
            bottomRight = [value[2][0], value[2][1]]
        elif id == 2:
            bottomLeft = [value [3][0], value[3][1]]
        elif id == 3:
            topLeft = [value[0][0], value[0][1]]
        elif id == 4:
            topRight = [value[1][0], value[1][1]]

    src = numpy.float32([topLeft,bottomLeft, topRight, bottomRight])
    det = numpy.float32([[0,0],[0,512], [512,0],[512,512]])
    M = cv2.getPerspectiveTransform(src, det)
    warped_image = cv2.warpPerspective(image,M,(512,512))
    
######################################################################################

    return warped_image

def transform_values(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the 
    position and orientation of the ArUco marker (with id 5), in the 
    CoppeliaSim scene.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by camera

    Returns:
    ---
    `scene_parameters` : [ list ]
            a list containing the position and orientation of ArUco 5
            scene_parameters = [c_x, c_y, c_angle] where
            c_x is the transformed x co-ordinate [float]
            c_y is the transformed y co-ordinate [float]
            c_angle is the transformed angle [angle]
    
    HINT:
        Initially the image should be cropped using perspective transform 
        and then values of ArUco (5) should be transformed to CoppeliaSim
        scale.
    
    Example call:
    ---
    scene_parameters = transform_values(image)
    """   
    scene_parameters = []
#################################  ADD YOUR CODE HERE  ###############################
    pi = 22/ 7
    cX =0
    cY = 0
    angle = 0
    ArUco_details_dict, _ = task_1b.detect_ArUco_details(image)
    for ids, coord in ArUco_details_dict.items():
        if ids == 5:
            cX = coord[0][0]
            cY = coord[0][1]
            angle = coord[1]
    c_x = (256-cX) * 0.9550 / 256
    c_y = (cY-256) * 0.9550 / 256
    if angle >=0:
        c_angle = (-180 - angle) * pi/180
    else:
        c_angle = (180 + angle) * pi/180
    scene_parameters = [c_x, c_y, c_angle]
######################################################################################

    return scene_parameters


def set_values(scene_parameters):
    """
    Purpose:
    ---
    This function takes the scene_parameters, i.e. the transformed values for
    position and orientation of the ArUco marker, and sets the position and 
    orientation in the CoppeliaSim scene.

    Input Arguments:
    ---
    `scene_parameters` :	[ list ]
            list of co-ordinates and orientation obtained from transform_values()
            function

    Returns:
    ---
    None

    HINT:
        Refer Regular API References of CoppeliaSim to find out functions that can
        set the position and orientation of an object.
    
    Example call:
    ---
    set_values(scene_parameters)
    """   
    aruco_handle = sim.getObject('/aruco_5')
#################################  ADD YOUR CODE HERE  ###############################
    x, y, angle = scene_parameters
    sim.setObjectPosition(aruco_handle,sim.handle_world, [x, y, 0.03])
    sim.setObjectOrientation(aruco_handle, -1, [0,0,angle])
######################################################################################

    return None

if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    task_1b = __import__('task_1b')
#################################  ADD YOUR CODE HERE  ################################
    video = cv2.VideoCapture("1295.mp4")
    #video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    #video.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
    if not video.isOpened():
        print("Cannot open the video file")
        exit()
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            print("Cant't receive frames (Stream end?). Exiting ...")
            break
        ArUco_details_dict, ArUco_corners = task_1b.detect_ArUco_details(frame)
        wrapped_image = perspective_transform(frame)
        scene_parameters = transform_values(wrapped_image)
        ##############################################
        print(f"Scene Parameter = {scene_parameters}")
        set_values(scene_parameters)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) and 0xFF == ord("q"):
            break
    video.release()
    cv2.destroyAllWindows()
#######################################################################################



    
