'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3A of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			task_3a.py
# Functions:		detect_all_nodes,detect_paths_to_graph, detect_arena_parameters, path_planning, paths_to_move
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import numpy as np
import cv2
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
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

def euclidean_distance(node, target_node):
	# need to find x_dict and -dc
	x1,x2, y1, y2 = compare_coordinate(node, target_node)
	e_distance = ((x2-x1)**2 + (y2-y1)**2)**0.5
	return e_distance
def generate_children(graph, node):
	children = graph[node]
	return children
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

def coordinate_get(image, coords):
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
    
def compare_coordinate(node, target_node):
    coordinate = get_unit(getImage())
    _,_, x_dict, y_dict = coordinate
    current_node = list(node)
    next_node = list(target_node)
    x1= x_dict[current_node[0]]
    y1= y_dict[current_node[1]]
    x2 = x_dict[next_node[0]]
    y2 = y_dict[next_node[1]]
    return x1, x2, y1, y2
def check_path(graph, current_node, closed_list, target_node):
	new_path = {}
	children = generate_children(graph, current_node)
	for key in children.keys():
		if key not in closed_list:
			new_path[key] = euclidean_distance(key, target_node)
	return new_path

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
	traffic_node = coordinate_get(image, traffic_cord)
	for i in range(len(traffic_node[0])):
		output.append("".join(str(j) for j in ((traffic_node[0])[i]+(traffic_node[1])[i])))    
	output = sorted(output)	
	for i in range(len(output)):
		traffic_signals.append(output[i])
	
	start_coord = xy_coordinate(image, [0,255,0])
	start_node = coordinate_get(image, start_coord)
	for i in range(len(start_node[0])):
		if start_node[0][i]!= []:
			start_node = ("".join(start_node[0][i]+ start_node[1][i]))
	
	# ending node
	end_coord = xy_coordinate(image, [189, 43, 105])
	end_node = coordinate_get(image, end_coord)
	for i in range(len(end_node[0])):
		if end_node[0][i]!= []:
			end_node = ("".join(end_node[0][i]+ end_node[1][i]))
	
	##################################################
	return traffic_signals, start_node, end_node


def detect_paths_to_graph(image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary of the
	connect path from a node to other nodes and will be used for path planning

	HINT: Check for the road besides the nodes for connectivity 

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`paths` : { dictionary }
			Every node's connection to other node and set it's value as edge value 
			Eg. : { "D3":{"C3":1, "E3":1, "D2":1, "D4":1}, 
					"D5":{"C5":1, "D2":1, "D6":1 }  }

			Why edge value 1? -->> since every road is equal

	Example call:
	---
	paths = detect_paths_to_graph(maze_image)
	"""    

	paths = {}
	##############	ADD YOUR CODE HERE	##############
	coordinate = get_unit(image)
	x,y, x_dict, y_dict = coordinate
	x_t = []	
	y_t = []	
	neighbourList= {}    
	for i in range(len(y)):			
		x_coord = x[i]					
		y_coord = y[i]					
		x_t.append([i for i in x_dict if x_dict[i]==x_coord])
		y_t.append([i for i in y_dict if y_dict[i]==y_coord])
	for i in range(len(y)):
		for j in range(len(x)):
			# check for the left neighbouring node
			if not ((image[y[i], x[j]-50])&[255, 255, 255]).any():
				neighbourList["".join(x_t[j-1]+y_t[i])]=1
			# check for the top neighbouring node
			if not ((image[y[i]-50, x[j]])&[255, 255, 255]).any():
				neighbourList["".join(x_t[j]+ y_t[i-1])]=1
		
			#check for the right neighbourign node
			if not ((image[y[i], x[j]+50])&[255, 255, 255]).any():
				neighbourList["".join(x_t[j+1]+y_t[i])]=1
			# check for the bottom neighbourign node
			if not ((image[y[i]+50, x[j]])&[255, 255, 255]).any():
				neighbourList["".join(x_t[j]+ y_t[i+1])]=1
			paths["".join(x_t[j]+y_t[i])] = neighbourList
			neighbourList = {}    
	##################################################
	return paths


def detect_arena_parameters(maze_image):
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) start_node : Start node which is mark in light green
	iii) end_node : End node which is mark in Purple
	iv) paths : list containing paths

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

	Eg. arena_parameters={"traffic_signals":[], 
	                      "start_node": "E4", 
	                      "end_node":"A3", 
	                      "paths": {}}
	"""    
	arena_parameters = {}

	##############	ADD YOUR CODE HERE	##############
	arena_parameters['traffic_signals'] = detect_all_nodes(maze_image)[0]
	arena_parameters['start_node'] = detect_all_nodes(maze_image)[1]
	arena_parameters['end_node']= detect_all_nodes(maze_image)[2]
	arena_parameters['paths'] = detect_paths_to_graph(maze_image)

	##################################################
	
	return arena_parameters

def path_planning(graph, start, end):

	"""
	Purpose:
	---
	This function takes the graph(dict), start and end node for planning the shortest path

	** Note: You can use any path planning algorithm for this but need to produce the path in the form of 
	list given below **

	Input Arguments:
	---
	`graph` :	{ dictionary }
			dict of all connecting path
	`start` :	str
			name of start node
	`end` :		str
			name of end node


	Returns:
	---
	`backtrace_path` : [ list of nodes ]
			list of nodes, produced using path planning algorithm

		eg.: ['C6', 'C5', 'B5', 'B4', 'B3']
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)
	"""    

	backtrace_path=[]

	##############	ADD YOUR CODE HERE	##############
	open_list = []
	closed_list = []
	distance = {}
	open_list.append(start)
	current_node = open_list[0]
	target_found = False
	death_end = False
	children = {}
	while not target_found:
		children = generate_children(graph, current_node)
		if len(children) > 0 :
			backtrace_path.append(current_node)
			for key in children.keys():
				if key not in closed_list:
					if key == end:
						current_node = key
						backtrace_path.append(current_node)
						target_found = True
						break
					else:
						#need to avoid node with traffic signal
						distance[key] = euclidean_distance( key, end)
			if len(distance) > 0:
				open_list.pop(0)
				closed_list.append(current_node)
				# choosing the node with minimum euclidean 
				current_node = min(distance, key= distance.get)
				open_list.append(current_node)
			else:
				if current_node != end:
					death_end = True
		if death_end: # reach the death end
			# check if current  node has other children  not in the closed list
			# if so take that path 
			# else loop through the children of closed list. and stop when its has children not in the closed list
			backtrace_path = []
			distance = {}
			closed_list.append(current_node)
			current_node = start
			backtrace_path.append(current_node)
			distance = check_path( graph, current_node, closed_list, end)
			if len(distance) > 0:
				current_node = min(distance, key = distance.get)
			else:
				# no children 
				for i in closed_list:
					if i != current_node:
						distance = check_path( graph, i, closed_list, end)
					if len(distance) > 0:
						current_node = min(distance, key = distance.get)
						break
			death_end = False
			
		distance = {}
		children = {}

	##################################################

	return backtrace_path

def paths_to_moves(paths, traffic_signal):

	"""
	Purpose:
	---
	This function takes the list of all nodes produces from the path planning algorithm
	and connecting both start and end nodes

	Input Arguments:
	---
	`paths` :	[ list of all nodes ]
			list of all nodes connecting both start and end nodes (SHORTEST PATH)
	`traffic_signal` : [ list of all traffic signals ]
			list of all traffic signals
	---
	`moves` : [ list of moves from start to end nodes ]
			list containing moves for the bot to move from start to end

			Eg. : ['UP', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN']
	
	Example call:
	---
	moves = paths_to_moves(paths, traffic_signal)
	"""    
	
	list_moves=[]

	##############	ADD YOUR CODE HERE	##############
	direction = 'north'
    
	for i in range(len(paths)-1):
		current_node = paths[i]
		next_node = paths[i+1]
		coordinate = compare_coordinate(current_node, next_node)
		if current_node in traffic_signal:
			list_moves.append("WAIT_5")
		if direction == 'north':

			if coordinate[0] == coordinate[1]: # x same and y different
				if coordinate[2] > coordinate[3]:
					list_moves.append("STRAIGHT")
					direction = 'north'
				elif coordinate[2] < coordinate[3]:
					list_moves.append("REVERSE")
					direction = 'south'
				continue
			elif coordinate[2]== coordinate[3]:# y same and x different
				if coordinate[0] > coordinate[1]:
					list_moves.append("LEFT")
					direction = 'west'
				elif coordinate[0] < coordinate[1]:
					list_moves.append('RIGHT')
					direction = 'east'
				continue
		if direction == "west":
			
			if coordinate[0] == coordinate[1]: # x same and y different
				if coordinate[2] > coordinate[3]:
					list_moves.append("RIGHT")
					direction = 'north'
				elif coordinate[2] < coordinate[3]:
					list_moves.append("LEFT")
					direction = 'south'
				continue
			elif coordinate[2]== coordinate[3]:# y same and x different
				if coordinate[0] > coordinate[1]:
					list_moves.append("STRAIGHT")
					direction = 'west'
				elif coordinate[0] < coordinate[1]:
					list_moves.append('REVERSE')
					direction = 'east'
				continue
		if direction =="east":
		
			if coordinate[0] == coordinate[1]: # x same and y different
				if coordinate[2] > coordinate[3]:
					list_moves.append("LEFT")
					direction = 'north'
				elif coordinate[2] < coordinate[3]:
					list_moves.append("RIGHT")
					direction = 'south'
				continue
			elif coordinate[2]== coordinate[3]:# y same and x different
				if coordinate[0] > coordinate[1]:
					list_moves.append("REVERSE")
					direction = 'west'
				elif coordinate[0] < coordinate[1]:
					list_moves.append('STRAIGHT')
					direction = 'east'
				continue
		if direction =="south":

			if coordinate[0] == coordinate[1]: # x same and y different
				if coordinate[2] > coordinate[3]:
					list_moves.append("REVERSE")
					direction = 'north'
				elif coordinate[2] < coordinate[3]:
					list_moves.append("STRAIGHT")
					direction = 'south'
				continue
			elif coordinate[2]== coordinate[3]:# y same and x different
				if coordinate[0] > coordinate[1]:
					list_moves.append("RIGHT")
					direction = 'west'
				elif coordinate[0] < coordinate[1]:
					list_moves.append('LEFT')
					direction = 'east'
				continue
		
	##################################################
	return list_moves

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

	# # path directory of images
	img_dir_path = "test_images/"

	for file_num in range(0,10):
		
			img_key = 'maze_00' + str(file_num)
			img_file_path = img_dir_path + img_key  + '.png'
			# read image using opencv
			image = cv2.imread(img_file_path)
			
			# detect the arena parameters from the image
			arena_parameters = detect_arena_parameters(image)
			print('\n============================================')
			print("IMAGE: ", file_num)
			print(arena_parameters["start_node"], "->>> ", arena_parameters["end_node"] )
			
			# path planning and getting the moves
			back_path=path_planning(arena_parameters["paths"], arena_parameters["start_node"], arena_parameters["end_node"])
			moves=paths_to_moves(back_path, arena_parameters["traffic_signals"])

			print("PATH PLANNED: ", back_path)
			print("MOVES TO TAKE: ", moves)

			# display the test image
			cv2.imshow("image", image)
			cv2.waitKey(0)
			cv2.destroyAllWindows()