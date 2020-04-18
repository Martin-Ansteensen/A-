#!/usr/bin/env python3
import time
import copy
import pygame 
import math

#################################################
############### User instructions ###############
#################################################
# Use the keys e and s to mark start and end node
# Use r to reset the app
# Use c to clear the work of the algorithm,
# and keep the obstacles you have drawn
# Use space to start the algorithm
# Use right mouse button to draw obstacles
# Use left mouse button to remove obstacles
# Use arrow up to increase the delay between each
# step in the algorithm, and arrow down to decrease
#################################################


class Node:
    """ Keep track of all the nodes we create and
    their variables
    """
    best_node = None
    lowest_cost = None
    all_nodes = []
    parent_nodes = []
    priority_que = []

    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent  #  Which node it origin from
        self.has_been_parent = False
        self.start_cost = self.parent.start_cost + math.sqrt((self.parent.x-self.x)**2+ (self.parent.y-self.y)**2)  #  The cost from this node to the start node, using the current path
        self.end_cost = math.sqrt((end[0] - self.x)**2 + (end[1] - self.y)**2)  #  The estimated cost to the end, calculated using pythagoras
        self.cost = self.start_cost + self.end_cost  #  The overall cost of the node

    #  Checks if a node is valid
    def is_valid(self):
        try:
            valid_conditions = [
                work_grid[self.y][self.x] != "-", # The cell is not an obstacle
                self.x in range(vertical), # The cells x is within the workspace
                self.y in range(horizontal), # The cells y is within the workspace
                not self.already_exists() # Returns True if it already exists, therefor not
            ]
            if all(valid_conditions):
                self.draw()
                Node.priority_que.append(self)
            else:
               del Node.all_nodes[-1]
        except(IndexError):  # The coordinates of the cell does not exist
            del Node.all_nodes[-1]
   
    #  Checks if the node already exists
    def already_exists(self): 
        status = False
        for node in Node.all_nodes:  # Checks all of the nodes that exist
            if (node.x, node.y) == (self.x, self.y) and node != self: # Checks if the cell has the same coordinate as an existing cell
                if node.cost > self.cost:  # If the new cell (self) has a lower cost
                    Node.all_nodes.remove(self)
                    Node.all_nodes[Node.all_nodes.index(node)] = self  # Inserts itself in the former cells index in the all_nodes
                    if node.has_been_parent == True:  # Checks if the old cell has any children
                        for child_node in Node.all_nodes: 
                            if child_node.parent == node:
                                child_node.parent = self  # Sets the new cell as parent
                        
                        Node.parent_nodes.remove(self)
                        self.has_been_parent = True
                        Node.parent_nodes[Node.parent_nodes.index(node)] = self  # Inserts itself in the former cells index in the parent_nodes
                        break
                    else:
                        break
                else:   
                    return True  # Returns true because the new cell (self) does not have a better path option than the old one
        return status
        
    #  Inserts itsfel into the GUI and the array representing the grid
    def draw(self): 
        work_grid[self.y][self.x] = "i"
        if self.has_been_parent:
            draw_node(Node.best_node.y, Node.best_node.x, parent_colour, "xy")
        else:
            draw_node(self.y, self.x, path_block_colour, "xy")


class UserNodes(Node):
    """ Only includes start- and end node, 
    which have to be created to make the
    calculations in the super class (Node) work
    """
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent
        self.has_been_parent = False
        self.cost, self.start_cost = 0, 0


def find_path():
    """ Finds the shortest path between two points,
    using the A* algorithm
    """
    Node.parent_nodes = []
    Node.all_nodes = []
    Node.priority_que = []
    solution_possible = True
    solution_grid = copy.deepcopy(work_grid)
    Node.best_node = start_node  #  Set the start node as the best node
    Node.priority_que.append(Node.best_node)
    Node.all_nodes.append(Node.best_node)  #  Add the starting node to the list
    nodes_pattern = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]] # Right, left, up, down, upper right, upper left, down right, down left
    while [Node.best_node.x, Node.best_node.y] != end:  # Run until the current node is the end node
        
        for node in Node.all_nodes:
            if node not in Node.parent_nodes:
                Node.best_node = node

        for node in Node.all_nodes:
            if node.cost < Node.best_node.cost and not node.has_been_parent:  # Finds the node with the lowest cost
                Node.best_node = node
        
        Node.parent_nodes.append(Node.best_node)
        Node.best_node.has_been_parent = True 
        Node.best_node.draw() 
        
        
        # Create surrounding nodes to the best_node
        for i in range(len(nodes_pattern)):
            Node.all_nodes.append(Node(Node.best_node.x+nodes_pattern[i][0], Node.best_node.y+nodes_pattern[i][1], Node.best_node)) # if we have switched between two nodes with the same cost it will fuck up
            Node.all_nodes[-1].is_valid()

        if len(Node.all_nodes) == len(Node.parent_nodes):  
            print("No solution available")
            solution_possible = False
            break
        # Take a break to give the user time to see what has happend
        time.sleep(delay.delay)  

    if solution_possible:
        solution = []     
        solution.append(Node.best_node)
        solution_grid[solution[-1].y][solution[-1].x] = "i"
        draw_node(solution[-1].y, solution[-1].x,  solution_colour, "xy") 
        
        # Backtracks
        while solution[-1].parent != None:
            solution_grid[solution[-1].y][solution[-1].x] = "i"
            draw_node(solution[-1].y, solution[-1].x,  solution_colour, "xy") 
            solution.append(solution[-1].parent)  # Adds the parent of the current node
            time.sleep(delay.delay)
        
        # The while loop exits before it adds the start node
        solution_grid[start_node.y][start_node.x] = "i"
        draw_node(start_node.y, start_node.x,  solution_colour, "xy") 

        # Prints the grid where the algorithm worked
        for y in range(horizontal):
            print(work_grid[y])
        print("\n")
        #  Prints the solution in grid format
        for y in range(horizontal):
            print(solution_grid[y])
        print("Path created")
        
    else:
        pass


class Delay:
    def __init__(self):
        self.delay = 0


def drawGrid():
    """ Draws the GUI grid,
    and links the pixel coordinates to each box
    """
    for y in range(vertical):
        grid_list.append([])
        for x in range(horizontal):
            rect = pygame.Rect(int(x*spacing*block_size), int(y*spacing*block_size), block_size, block_size)
            pygame.draw.rect(window, block_colour, rect, 0)
            grid_list[y].append([int(x*spacing*block_size), int(y*spacing*block_size)])  


def draw_node(in_x, in_y, colour, datatype):
    """ Draws the given coordinates in the grid
    on the screen
    """
    # The given coordinates are pixels,
    # and we have to find the closest node to the mouse
    if datatype == "pixel":
        pixel_x, pixel_y, xy_x, xy_y = get_closest_node(in_x, in_y)
    elif datatype == "xy": # The coordinates are "grid" type
        pixel_x = in_x*block_size*spacing
        pixel_y = in_y*block_size*spacing

    rect = pygame.Rect(pixel_x, pixel_y, block_size, block_size)
    pygame.draw.rect(window, colour, rect, 0)
    pygame.display.flip()  # Partially updates screen  


def get_closest_node(in_x, in_y):
    """ Finds the closest node given a coordinate.
    Only accepts pixels as input,
    but outputs both pixels and coordinates
    """
    lowest_difference = 100
    closest_cell_pixel = [0,0]
    for y in range(len(grid_list)):
        for x in range(len(grid_list[y])):
            difference = abs(grid_list[y][x][0]- in_x) + abs(grid_list[y][x][1]- in_y)
            if difference < lowest_difference:
                lowest_difference = difference
                closest_cell_pixel = grid_list[y][x]
                closest_cell_xy_x = x
                closest_cell_xy_y = y
    # Returns pixel coordinates, and then the xy
    return closest_cell_pixel[0], closest_cell_pixel[1], closest_cell_xy_x, closest_cell_xy_y


def walls():
    """ Draws and removes obstacles where the mouse 
    pointer is, if the mousebutton is pressed
    """
    # Draw
    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= block_size/3  # Take into account that the corner is counted as the origin of the cell
        mouse_y -= block_size/3  # Take into account that the corner is counted as the origin of the cell
        draw_node(mouse_x, mouse_y, obstacle_colour, "pixel") # Give that cell "start node" status. If the key is pressed again the last node will "lose" its status and a new one wil be start node  
        pixel_x, pixel_y, xy_x, xy_y = get_closest_node(mouse_x,mouse_y)
        work_grid[xy_x][xy_y] = "-"
    # Remove  
    elif pygame.mouse.get_pressed()[2]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= block_size/3  # Take into account that the corner is counted as the origin of the cell
        mouse_y -= block_size/3  # Take into account that the corner is counted as the origin of the cell
        draw_node(mouse_x, mouse_y, block_colour, "pixel")
        pixel_x, pixel_y, xy_x, xy_y = get_closest_node(mouse_x,mouse_y)
        work_grid[xy_x][xy_y] = "0"


def main():
    original_grid = []
    window.fill(background_colour)
    drawGrid()
    draw_node(start[0], start[1], end_colour, "xy")
    draw_node(end[0], end[1], start_colour, "xy")   
    # Run until the user asks to quit
    running = True
    while running:
        for event in pygame.event.get():  # Has the user clicked the close button
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Mark the node as start node
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_x -= block_size/3  # Take into account that the corner is counted as the origin of the cell
                    mouse_y -= block_size/3  # Take into account that the corner is counted as the origin of the cell               
                    draw_node(start[1], start[0], block_colour, "xy")  # Make the former start node a normal node
                    pixel_x, pixel_y, xy_x, xy_y = get_closest_node(mouse_x, mouse_y)
                    start_node.x = xy_y
                    start_node.y = xy_x
                    start[0] = xy_y
                    start[1] = xy_x
                    work_grid[xy_x][xy_y] =  "0" # Remove obstacle status if it was former obstacle
                    draw_node(xy_x, xy_y, (0,255,0), "xy")  # Draw the new start node

                if event.key == pygame.K_e:  # Mark the node as end_node
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_x -= block_size/3  # Take into account that the corner is counted as the origin of the cell
                    mouse_y -= block_size/3  # Take into account that the corner is counted as the origin of the cell
                    draw_node(end[1], end[0], block_colour, "xy")  # Make the fomer end node a normal node
                    pixel_x, pixel_y, xy_x, xy_y = get_closest_node(mouse_x, mouse_y)
                    end_node.x = xy_y
                    end_node.y = xy_x
                    end[0] = xy_y
                    end[1] = xy_x
                    work_grid[xy_x][xy_y] =  "0" # Remove obstacle status if it was former obstacle
                    draw_node(xy_x, xy_y, (255,0,0), "xy")  # Draw the new end node 

                if event.key == pygame.K_DOWN:  # Reduce algorithm speed
                    delay.delay -= 0.01
                    if delay.delay < 0:
                        delay.delay = 0

                if event.key == pygame.K_UP:  # Increase algorithm speed
                    delay.delay += 0.01
                
                #  Clear the visualisation of the algorithm
                if event.key == pygame.K_c:
                    for i in range(len(original_grid)):
                        for j in range(len(original_grid[i])):
                            if original_grid[i][j] == "-":
                                draw_node(i, j, obstacle_colour, "xy")
                            else:
                                draw_node(i, j, block_colour, "xy")
                    # Draw the end and start node that we just removed
                    draw_node(start[1], start[0], end_colour, "xy")
                    draw_node(end[1], end[0], start_colour, "xy")

                #  Restart the game
                if event.key == pygame.K_r:
                    for i in range(len(original_grid)):
                        for j in range(len(original_grid[i])):
                                draw_node(i, j, block_colour, "xy")
                                work_grid[i][j] = "0"
                    # Draw end and start node
                    draw_node(start[1], start[0], end_colour, "xy")
                    draw_node(end[1], end[0], start_colour, "xy")
                    original_grid = copy.deepcopy(work_grid)

                if event.key == pygame.K_SPACE:  # Find path between end and start node
                    original_grid = copy.deepcopy(work_grid)
                    find_path()

        walls()  # Draw walls
        pygame.display.flip()  # Partially update screen

if __name__ == '__main__':
    # Set up the drawing window
    pygame.init()
    block_size = 20
    background_colour = (0, 0, 0)
    block_colour = (255, 165, 91)
    path_block_colour = (255,116, 0)
    parent_colour = (172, 78, 0)
    solution_colour = (105,75,31) #(115,53,40)#(91,49,2)
    obstacle_colour = (23,15,9)
    start_colour = (255, 0, 0)
    end_colour = (0, 255, 0)
    spacing = 1.1 # Make this number higher if you want to have a smaller box_size
    horizontal = 40
    vertical = 35
    width = int(horizontal*block_size*spacing)
    height = int(vertical*block_size*spacing)
    FONT = pygame.font.SysFont("comicsansms", 20)
    
    grid_list = []
    work_grid = [["0" for i in range(vertical)] for j in range(horizontal)] 
    start = [1, 1]
    end = [2, 2] 
    start_node = UserNodes(start[0], start[1], None)
    end_node = UserNodes(end[0], end[1], None)

    delay = Delay()
    window = pygame.display.set_mode([width, height])

    main()
    pygame.quit()

