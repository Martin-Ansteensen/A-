#!/usr/bin/env python3
import time
import copy
import pygame
import math

class Node:
    best_node = None
    lowest_cost = None

    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent
        self.has_been_parent = False

        self.x_from_start = abs(start[0] - self.x)
        self.y_from_start = abs(start[1] - self.y)
        self.x_from_end = abs(end[0] - self.x)
        self.y_from_end = abs(end[1] - self.y)
        
        self.cost = self.x_from_end + self.y_from_end + self.x_from_start**2 + self.y_from_start**2

    def is_valid(self):
        try:
            valid_conditions = [
                work_grid[self.x][self.y] != "-", # The cell is not an obstacle
                self.x in range(len(work_grid[self.x])), # The cells x is within the workspace
                self.y in range(len(work_grid)), # The cells y is within the workspace
                not self.already_exists() # Returns True if it already exists, therefor not
            ]
            
            if all(valid_conditions) or self.x == end_node.x and self.y == end_node.y: # The cell is valid of all conditions were met or if it has reached the end
                return True
            else:
                return False
        except(TypeError, IndexError): # The coordinates of the cell does not exist
            return False

    def already_exists(self): 
        status = False
        for node in all_nodes: # Checks all of the nodes that exist
            if node.x == self.x and node.y == self.y and node != self: # Checks if the cell has the same coordinate as an existing cell
                return True
        return status
        
    def draw(self): # GUI
        work_grid[self.x][self.y] = "i"

def find_path():
    solution_possible = True
    current_node_xy = start
    all_nodes.append(start_node) # Add the starting node to the list    
    solution_grid = copy.deepcopy(work_grid)
    start_time = time.time()
    while current_node_xy != end: # Run until the current node is the end node
        new_nodes_created = False
        # Finds the node closest to the end node
        Node.lowest_cost = all_nodes[-1].cost 
        for node in all_nodes:
            if node.cost <= Node.lowest_cost and node.has_been_parent == False:
                Node.lowest_cost = node.cost
                Node.best_node = node
                current_node_xy[0], current_node_xy[1] = node.x, node.y
                parent_nodes.append(node)
                node.has_been_parent = True
        
        # Create surrounding nodes
        for i in range(len(nodes_pattern)):
            all_nodes.append(Node(current_node_xy[0]+nodes_pattern[i][0], current_node_xy[1]+nodes_pattern[i][1], Node.best_node))
            if all_nodes[-1].is_valid() == True:
                new_nodes_created = True
                all_nodes[-1].draw()
                draw_cell_v2(all_nodes[-1].y, all_nodes[-1].x, (245,182,66))
            else:
                del all_nodes[-1]
            
        if not new_nodes_created:
            if len(all_nodes) == len(parent_nodes):
                print("No solutions available")
                solution_possible = False

                break
            # Print the grid
        
        # for x in range(rows):
        #     print(work_grid[x])
        # print("\n")
        wait()
    if solution_possible:
        solution = []     
        solution.append(parent_nodes[-1]) # The end node
        solution_grid[solution[-1].x][solution[-1].y] = "i"
        draw_cell_v2(solution[-1].y, solution[-1].x,  (0,0,255)) 
        
        # Backtracks
        while True:
            solution.append(solution[-1].parent) # Adds the
            solution_grid[solution[-1].x][solution[-1].y] = "i"
            draw_cell_v2(solution[-1].y, solution[-1].x,  (0,0,255)) 
            if solution[-1].x_from_start == 0 and solution[-1].y_from_start == 0:
                break
            
        for x in range(rows):
            print(work_grid[x])

        print("\n")
        for x in range(rows):
            print(solution_grid[x])

        print("--- %s seconds ---" % (time.time() - start_time))

block_size = 20
background_colour = (255, 255, 255)
block_colour = (96, 110, 100)
spacing = 1.05
rows = 30
cols = 30
next_step = True
height = int(rows*block_size*spacing)
width = int(cols*block_size*spacing)
grid_list = []


#rows = 10
#cols = 10
work_grid = [["0" for i in range(cols)] for j in range(rows)] 

start = [0, 0]
end = [0, 0]
start_node = Node(start[0], start[1], None)
end_node = Node(end[0], end[1], None)
parent_nodes = []
all_nodes = []
nodes_pattern = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]] # Right, left, up, down, upper right, upper left, down right, down left





# Set up the drawing window
pygame.init()
window = pygame.display.set_mode([height, width])

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                return

def drawGrid():
    for y in range(cols):
        grid_list.append([])
        for x in range(rows):
            rect = pygame.Rect(int(x*spacing*block_size), int(y*spacing*block_size), block_size, block_size)
            pygame.draw.rect(window, block_colour, rect, 0)
            grid_list[y].append([int(x*spacing*block_size), int(y*spacing*block_size)])
    

def draw_cell(in_x, in_y, colour):
    x, y, a, b = get_closest_cell(in_x, in_y)

    rect = pygame.Rect(x, y, block_size, block_size)
    pygame.draw.rect(window, colour, rect, 0)

def draw_cell_v2(x, y, colour):
    rect = pygame.Rect(x*block_size*spacing, y*block_size*spacing, block_size, block_size)
    pygame.draw.rect(window, colour, rect, 0)
    pygame.display.update()
    
def get_closest_cell(in_x, in_y):
    lowest_difference = 100
    closest_cell = [0,0]
    for y in range(len(grid_list)):
        for x in range(len(grid_list[y])):
            difference = abs(grid_list[y][x][0]- in_x) + abs(grid_list[y][x][1]- in_y)
            if difference < lowest_difference:
                lowest_difference = difference
                closest_cell = grid_list[y][x]
                closest_cell_x = x
                closest_cell_y = y

    return closest_cell[0], closest_cell[1], closest_cell_x, closest_cell_y

def walls():
    
    if pygame.mouse.get_pressed()[0]:
        draw_colour = (0,0,0)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= block_size/3 # take into account that the corner is counted as the origin of the cell
        mouse_y -= block_size/3 # take into account that the corner is counted as the origin of the cell
        draw_cell(mouse_x, mouse_y, draw_colour) # Give that cell "start node" status. If the key is pressed again the last node will "lose" its status and a new one wil be start node  
        a, b, x, y = get_closest_cell(mouse_x,mouse_y)
        work_grid[y][x] = "-"
        
    elif pygame.mouse.get_pressed()[2]:
        draw_colour = block_colour
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= block_size/3 # take into account that the corner is counted as the origin of the cell
        mouse_y -= block_size/3 # take into account that the corner is counted as the origin of the cell
        draw_cell(mouse_x, mouse_y, draw_colour) # Give that cell "start node" status. If the key is pressed again the last node will "lose" its status and a new one wil be start node  
        a, b, x, y = get_closest_cell(mouse_x,mouse_y)
        work_grid[y][x] = "0"


window.fill(background_colour)
drawGrid()
# Run until the user asks to quit
running = True



while running:
    # Has the user clicked the clos button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: # mark cell as start_node
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_x -= block_size/3 # take into account that the corner is counted as the origin of the cell
                mouse_y -= block_size/3 # take into account that the corner is counted as the origin of the cell
                
                a, b, x, y = get_closest_cell(mouse_x, mouse_y)
                start_node.x = y
                start_node.y = x
                start[0] = y
                start[1] = x
                draw_cell(mouse_x, mouse_y, (0,255,0)) # Give that cell "start node" status. If the key is pressed again the last node will "lose" its status and a new one wil be start node
                
            if event.key == pygame.K_e: # mark cell as end_node
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_x -= block_size/3 # take into account that the corner is counted as the origin of the cell
                mouse_y -= block_size/3 # take into account that the corner is counted as the origin of the cell
                a, b, x, y = get_closest_cell(mouse_x, mouse_y)
                end_node.x = y
                end_node.y = x
                end[0] = y
                end[1] = x
                draw_cell(mouse_x, mouse_y, (255,0,0)) # Give that cell "start node" status. If the key is pressed again the last node will "lose" its status and a new one wil be start node


            if event.key == pygame.K_SPACE: # mark cell as end_node
                find_path()

            #run algorith
    # Draw the grid and display the new image
    walls()
    pygame.display.update()


# Done! Time to quit.
pygame.quit()


