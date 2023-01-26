'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1A of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			task_1a.py
# Functions:		detect_traffic_signals, detect_horizontal_roads_under_construction, detect_vertical_roads_under_construction,
#					detect_medicine_packages, detect_arena_parameters
# 					[ xy_coordinate, x_coordinates, y_coordinates, reshape, find_package_color, shape_details ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import cv2
import numpy as np
##############################################################

def get_unit(image):
    x_dict = {}
    y_dict = {}

    # define labels
    x_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    y_labels = ['1', '2', '3', '4', '5', '6', '7']

    # get x_coordinates, y_coordinates of intersection_node: (image, blue)
    x = list(np.unique(x_coordinates(xy_coordinate(image, [255,0,0]))))
    y = list(np.unique(y_coordinates(xy_coordinate(image, [255,0,0]))))	
    for i in range(len(x)):
        x_dict[f'{x_labels[i]}'] = x[i]

    for j in range(len(y)):
        y_dict[f'{y_labels[j]}'] = y[j]
    return x, y, x_dict, y_dict
def setImage(image):
    global mazeImage
    mazeImage = image
def getImage():
    return mazeImage

def get_node(image, coords):
    coordinate = get_unit(image)
    _,_, x_dict, y_dict = coordinate
    x_t = []	
    y_t = []	
    for coord in coords:
        x_t.append(coord[0])
        y_t.append(coord[1])
    l_x = []								
    l_y = []								
    for i in range(len(x_t)):
        x_coord = x_t[i]					
        y_coord = y_t[i]					
        l_x.append([i for i in x_dict if x_dict[i]==x_coord])
        l_y.append([i for i in y_dict if y_dict[i]==y_coord])
    output= []
    output.append(l_x)
    output.append(l_y)
    return output


################# ADD UTILITY FUNCTIONS HERE #################

# get the coordinate of traffic_light, intersection_node
def xy_coordinate(maze_image, color):
    dx = [0,0,1,1,-1,-1]
    dy = [1,-1,1,-1,1,-1]
    visited = {}
    def dfs(x, y):
        visited[(x,y)] = 2
        i = 0
        while i<6:
            new_x = x+dx[i]
            new_y = y+dy[i]
            if(not((new_x, new_y)in visited)):
                i+=1
                continue

            if(visited[(new_x, new_y)] == 2):
                i+=1
                continue

            dfs(new_x, new_y)
            i+=1

    X,Y = np.where(np.all(maze_image==color, axis=2))

    for pixel in np.column_stack((X,Y)):
        x = pixel[1]
        y = pixel[0]
        visited[(x,y)] = 1

    result = []
    for pixel in np.column_stack((X,Y)):
        x = pixel[1]
        y = pixel[0]
        if visited[(x,y)] == 1:
            result.append((x,y))
            dfs(x,y)
    return result	# return x,y coordinates of particular color in the image

    # get the unique xy-coordinates 
def x_coordinates(intersect_cord_x):	# x_coordinates 
    x_cds = []	
    for coords in intersect_cord_x:
        x_cds.append(coords[0])	
    return x_cds

def y_coordinates(intersect_cord_y):	# y_coordinates
    y_cds = []	
    for coords in intersect_cord_y:
        y_cds.append(coords[1])
    return y_cds

# reshape the roi of the image to shpe coordinates
def reshape(maze_image):
    x, w = 0, 750
    y, h = 113, 75
    resize_img = maze_image[y:y+h, x:x+w]
    return resize_img

# get the color of shape of interest
def find_package_color(x, y, maze_image):
    color_dict = {
        'Green':[0,255,0],
        'Pink':[180,0,255],
        'Orange':[0,127,255],
        'Skyblue':[255,255,0]
    }

    # find and return the color match of the detected shape (coordinate)
    color = list(maze_image[y][x])
    shape_color = [i for i in color_dict if color_dict[i]==color]
    return shape_color

# get the centroid_coordinate of package
def shape_details(contour, maze_image, shape):

    # get x_coordinate of intersection_node (image, blue)
    # one need not need to find the y-coordinate, since shop location differs only in x-coordinates
    x = list(np.unique(x_coordinates(xy_coordinate(maze_image, [255,0,0]))))

    shop_1=['Shop_1']	# store shop_1 details
    shop_2=['Shop_2'] 	# store shop_2 details
    shop_3=['Shop_3']	# store shop_3 details
    shop_4=['Shop_4'] 	# store shop_4 details
    shop_5=['Shop_5']	# store shop_5 details
    shop_6=['Shop_6']	# sotre shop_6 details

    # finding centroid-coordinates of the shape using the contour
    M = cv2.moments(contour)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])	# x-coordinate
        cy = int(M['m01']/M['m00']) # y-coordinate

        # check shop_number
        if cx>x[0] and cx<x[1]:	# shop_1
            color = find_package_color(cx, cy+113, maze_image)	# since we resized image from y, do y->y+113 to get actual coordinates
            shop_1.append("".join(str(j) for j in color))
            shop_1.append(shape)
            shop_1.append([cx, cy+113])

        elif cx>x[1] and cx<x[2]:	# shop_2
            color = find_package_color(cx, cy+113, maze_image)
            shop_2.append("".join(str(j) for j in color))
            shop_2.append(shape)
            shop_2.append([cx, cy+113])

        elif cx>x[2] and cx<x[3]:	# shop_3
            color = find_package_color(cx, cy+113, maze_image)
            shop_3.append("".join(str(j) for j in color))
            shop_3.append(shape)
            shop_3.append([cx, cy+113])

        elif cx>x[3] and cx<x[4]:	# shop_4
            color = find_package_color(cx, cy+113, maze_image)
            shop_4.append("".join(str(j) for j in color))
            shop_4.append(shape)
            shop_4.append([cx, cy+113])

        elif cx>x[4] and cx<x[5]:	# shop_5
            color = find_package_color(cx, cy+113, maze_image)
            shop_5.append("".join(str(j) for j in color))
            shop_5.append(shape)
            shop_5.append([cx, cy+113])

        elif cx>x[5] and cx<x[6]:	# shop_6
            color = find_package_color(cx, cy+113, maze_image)
            shop_6.append("".join(str(j) for j in color))
            shop_6.append(shape)
            shop_6.append([cx, cy+113])

    # return details
        if len(shop_1) > 2:
            return shop_1
        if len(shop_2) > 2:
            return shop_2
        if len(shop_3) > 2:
            return shop_3
        if len(shop_4) > 2:
            return shop_4
        if len(shop_5) > 2:
            return shop_5
        if len(shop_6) > 2:
            return shop_6
##############################################################
def detect_all_nodes(image):
    """
    Purpose:
    ---
    This function takes the image as an argument and returns a list of
    nodes in which traffic signals, start_node and end_node are present in the image

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `traffic_signals, start_node, end_node` : [ list ], str, str
            list containing nodes in which traffic signals are present, start and end node too

    Example call:
    ---
    traffic_signals, start_node, end_node = detect_all_nodes(maze_image)
    """    
    traffic_signals = []
    start_node = ""
    end_node = ""

    ##############	ADD YOUR CODE HERE	##############
    output = []
    setImage(image)
    traffic_cord = xy_coordinate(image, [0,0,255])		
    traffic_node = get_node(image, traffic_cord)
    for i in range(len(traffic_node[0])):
        output.append("".join(str(j) for j in ((traffic_node[0])[i]+(traffic_node[1])[i])))    
    output = sorted(output)	
    for i in range(len(output)):
        traffic_signals.append(output[i])

    start_coord = xy_coordinate(image, [0,255,0])
    start_node = get_node(image, start_coord)
    for i in range(len(start_node[0])):
        if start_node[0][i]!= []:
            start_node = ("".join(start_node[0][i]+ start_node[1][i]))

    # ending node
    end_coord = xy_coordinate(image, [189, 43, 105])
    end_node = get_node(image, end_coord)
    for i in range(len(end_node[0])):
        if end_node[0][i]!= []:
            end_node = ("".join(end_node[0][i]+ end_node[1][i]))

    ##################################################
    return traffic_signals, start_node, end_node

def detect_horizontal_roads_under_construction(maze_image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a list
    containing the missing horizontal links

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `horizontal_roads_under_construction` : [ list ]
            list containing missing horizontal links
    
    Example call:
    ---
    horizontal_roads_under_construction = detect_horizontal_roads_under_construction(maze_image)
    """    
    horizontal_roads_under_construction = []

    ##############	ADD YOUR CODE HERE	##############
    x,y,x_dict, y_dict = get_unit(maze_image)

	# using line detection, store x,y coordinates of missing horizontal road 
    x_t = []	
    y_t = []	
    for i in range(len(y)):			
        for j in range(len(x)-1):	
            if((maze_image[y[i], x[j]+50])&[255, 255, 255]).any():
                x_t.append(x[j])	
                y_t.append(y[i])	

    # store ouput in the form of labels using coordinates & dictionary mapping
    l_x_1 = []							
    l_x_2 = []
    l_y = []								
    for i in range(len(x_t)):
        y_coord = y_t[i]					
        x_coord = x_t[i]					
        l_y.append([i for i in y_dict if y_dict[i]==y_coord])
        l_x_1.append([i for i in x_dict if x_dict[i]==x_coord])
        l_x_2.append([i for i in x_dict if x_dict[i]==x_coord+100])

    # output = sorted (l_x_1(x_label)l_y (y_label) - l_x_2(x_label)l_y(y_label))
    output = []
    for i in range(len(l_y)):
        output.append(("".join(str(j) for j in (l_x_1[i]+l_y[i])))+'-'+("".join(str(j) for j in (l_x_2[i]+l_y[i]))))
    output = sorted(output)

    for i in range(len(output)):
        horizontal_roads_under_construction.append(output[i])	

    ##################################################
    
    return horizontal_roads_under_construction	

def detect_vertical_roads_under_construction(maze_image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a list
    containing the missing vertical links

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `vertical_roads_under_construction` : [ list ]
            list containing missing vertical links
    
    Example call:
    ---
    vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
    """    
    vertical_roads_under_construction = []

    ##############	ADD YOUR CODE HERE	##############

    # define dictionary
    x, y, x_dict, y_dict = get_unit(maze_image)
    # using line detection, store x,y coordinates of missing vertical road 
    x_t = []	
    y_t = []	
    for i in range(len(x)):			
        for j in range(len(y)-1):	
            if((maze_image[y[j]+50,x[i]])&[255, 255, 255]).any():
                x_t.append(x[i])	
                y_t.append(y[j])	
        
    # store ouput in the form labels using coordinates & dictionary mapping
    l_x = []								
    l_y_1 = []
    l_y_2 = []								
    for i in range(len(x_t)):
        x_coord = x_t[i]					
        y_coord = y_t[i]					
        l_x.append([i for i in x_dict if x_dict[i]==x_coord])
        l_y_1.append([i for i in y_dict if y_dict[i]==y_coord])
        l_y_2.append([i for i in y_dict if y_dict[i]==y_coord+100])

    # output = sorted (l_x(x_label)l_y_1(y_label) - l_x(x_label)l_y_2(y_label))
    output = []
    for i in range(len(l_x)):
        output.append((("".join(str(j) for j in (l_x[i]+l_y_1[i])))+'-'+("".join(str(j) for j in (l_x[i]+l_y_2[i])))))
    output = sorted(output)

    for i in range(len(output)):
        vertical_roads_under_construction.append(output[i])	

    ##################################################
    
    return vertical_roads_under_construction


def detect_medicine_packages(maze_image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a nested list of
    details of the medicine packages placed in different shops

    ** Please note that the shop packages should be sorted in the ASCENDING order of shop numbers 
    as well as in the alphabetical order of colors.
    For example, the list should first have the packages of shop_1 listed. 
    For the shop_1 packages, the packages should be sorted in the alphabetical order of color ie Green, Orange, Pink and Skyblue.

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `medicine_packages` : [ list ]
            nested list containing details of the medicine packages present.
            Each element of this list will contain 
            - Shop number as Shop_n
            - Color of the package as a string
            - Shape of the package as a string
            - Centroid co-ordinates of the package
    Example call:
    ---
    medicine_packages = detect_medicine_packages(maze_image)
    """    
    medicine_packages_present = []

    ##############	ADD YOUR CODE HERE	##############
    # store shape details
    circles = []
    triangles = []
    squares = []

    # reshape the images
    img = reshape(maze_image)

    # determine contours
    imgGry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _,thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
    contours,_= cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # determine shaps using contours size
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)

        if len(approx) == 3:	# triangle
            triangle = shape_details(contour, maze_image, 'Triangle')
            triangles.append(triangle)

        elif len(approx) == 4 :	
            x, y , w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            if aspectRatio >= 0.95 and aspectRatio < 1.05:	# square
                square = shape_details(contour, maze_image, 'Square')
                squares.append(square)

        else:	# circle
            circle = shape_details(contour, maze_image, 'Circle')
            circles.append(circle)
            
    # update medicine_package with sorted output
    output = (triangles+circles+squares)
    medicine_packages_present = sorted(output)

    ##################################################
    return medicine_packages_present

def detect_arena_parameters(maze_image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns a dictionary
    containing the details of the different arena parameters in that image

    The arena parameters are of four categories:
    i) traffic_signals : list of nodes having a traffic signal
    ii) horizontal_roads_under_construction : list of missing horizontal links
    iii) vertical_roads_under_construction : list of missing vertical links
    iv) medicine_packages : list containing details of medicine packages

    These four categories constitute the four keys of the dictionary

    Input Arguments:
    ---
    `maze_image` :	[ numpy array ]
            numpy array of image returned by cv2 library
    Returns:
    ---
    `arena_parameters` : { dictionary }
            dictionary containing details of the arena parameters
    
    Example call:
    ---
    arena_parameters = detect_arena_parameters(maze_image)
    """    
    arena_parameters = {}

    ##############	ADD YOUR CODE HERE	##############
    # find
    traffic_signals = detect_all_nodes(maze_image)[0]
    start_node = detect_all_nodes(maze_image)[1]
    end_node = detect_all_nodes(maze_image)[2]
    horizontal_roads_construction = detect_horizontal_roads_under_construction(maze_image)
    vertical_roads_construction = detect_vertical_roads_under_construction(maze_image)
    medicine_package = detect_medicine_packages(maze_image)


    # update
    arena_parameters['traffic_signals'] = traffic_signals
    arena_parameters['start_node']= start_node
    arena_parameters['end_node']= end_node
    arena_parameters['horizontal_roads_under_construction'] = horizontal_roads_construction
    arena_parameters['vertical_roads_under_construction'] = vertical_roads_construction
    arena_parameters['medicine_packages'] = medicine_package

    ##################################################
    
    return arena_parameters

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

    # path directory of images in test_images folder
    img_dir_path = "public_test_images/"

    # path to 'maze_0.png' image file
    file_num = 0
    img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
    
    # read image using opencv
    maze_image = cv2.imread(img_file_path)
    
    print('\n============================================')
    print('\nFor maze_' + str(file_num) + '.png')

    # detect and print the arena parameters from the image
    arena_parameters = detect_arena_parameters(maze_image)

    print("Arena Prameters: " , arena_parameters)

    # display the maze image
    cv2.imshow("image", maze_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')
    
    if choice == 'y':

        for file_num in range(1, 15):
            
            # path to maze image file
            img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
            
            # read image using opencv
            maze_image = cv2.imread(img_file_path)
    
            print('\n============================================')
            print('\nFor maze_' + str(file_num) + '.png')
            
            # detect and print the arena parameters from the image
            arena_parameters = detect_arena_parameters(maze_image)

            print("Arena Parameter: ", arena_parameters)
                
            # display the test image
            cv2.imshow("image", maze_image)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
