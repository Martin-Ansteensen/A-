#!/usr/bin/env python3

### If start or end is clicked then the last has to be removed
#Create user-input popup at the beginning to give size of grid and blocks
#Create box to restart
#Popup solution found/not possible
#validate user input (both in grid size and coordinates of start and end before they are allowed to press find_path)
#Find out why the grid must be quadratic (and fix)
#Slider to vary speed of steps in algorithm
#Find out why boxes can not be smaller than 10 pixels
#Add buttton for next step
#Fix cost for diagonals
#Cleanup of code



import time
import copy
import pygame
import math

class Node:
    best_node = None
    lowest_cost = None

    def __init__(self, x, y, parent):
        # All calculations inside node operates in array-coordinates
        # If the node has a position of (5,10) (x,y), then it has (10,5) (y,x) inside node
        # This is because the array operates in xy

        self.x = y
        self.y = x
        self.parent = parent  # Which node it origin from
        self.has_been_parent = False
        self.start_cost = self.parent.start_cost + math.sqrt((self.parent.x-self.x)**2+ (self.parent.y-self.y)**2)  # The cost from this node to the start node, using the current path
        self.end_cost = math.sqrt((end[1] - self.x)**2 + (end[0] - self.y)**2)  # The estimated cost to the end, calculated using pythagoras
        # End operates in xy, node operates in yx
        self.cost = self.start_cost + self.end_cost  # The overall cost of the node

    def is_valid(self):
        try:
            valid_conditions = [
                work_grid[self.x][self.y] != "-", # The cell is not an obstacle
                self.x in range(len(work_grid)), # The cells x is within the workspace
                self.y in range(len(work_grid[self.y])), # The cells y is within the workspace
                not self.already_exists() # Returns True if it already exists, therefor not
            ]
            
            if all(valid_conditions) or self.x == end_node.y and self.y == end_node.x: # The cell is valid if all conditions were met or if it has reached the end
                return True
            else:
                return False
        except(TypeError, IndexError):  # The coordinates of the cell does not exist
            return False

    def already_exists(self): 
        status = False
        for node in all_nodes:  # Checks all of the nodes that exist
            if node.x == self.x and node.y == self.y and node != self: # Checks if the cell has the same coordinate as an existing cell
                status = True
        return status
        
    def draw(self): # GUI
        work_grid[self.x][self.y] = "i"
        if self.has_been_parent:
            draw_cell_v2(Node.best_node.x, Node.best_node.y, parent_colour)
        else:
            draw_cell_v2(self.x, self.y, path_block_colour)


class UserNodes(Node):
    def __init__(self, x, y, parent):
        self.x = y
        self.y = x
        self.parent = parent
        self.has_been_parent = False
        self.cost, self.start_cost = 0, 0

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = block_colour
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color =  parent_colour if self.active else block_colour
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE: # The user tried to remove text
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
        return None

    def draw(self, window):
        # Blit the text.
        window.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(window, self.color, self.rect, 2)
        
def text(x, y, colour, text):
    txt_surface = FONT.render(text, True, colour)
    window.blit(txt_surface, (x,y))

def button(x, y, w, h, ic, ac, text, action=None):
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(window, ic,(x,y,w,h))

    # textSurf, textRect = text_objects(text, FONT)
    # textRect.center = ( (x+(w/2)), (y+(h/2)) )
    # window.blit(textSurf, textRect)

    txt_surface = FONT.render(text, True, ic)
    window.blit(txt_surface, (x+(w/2), y+(h/2)))


def wait_for_user_input():
    height = 200
    width = 200
    window = pygame.display.set_mode((width, height))
    
    x = InputBox(75, 20, 100, 38)    
    y = InputBox(75, 70, 100, 38)

    input_boxes = [x,y]
    done = False

    while not done:
        window.fill(path_block_colour)  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.draw(window)
        text(5, 20, obstacle_colour, 'Width:')
        text(5, 70, obstacle_colour, 'Height:')
        button(50, 130, 100, 38, block_colour, parent_colour, "Submit")#, wait())

        pygame.display.flip()

def find_path():
    solution_possible = True
    current_node_xy = copy.deepcopy(start)
    all_nodes.append(start_node) # Add the starting node to the list    
    solution_grid = copy.deepcopy(work_grid)
    start_time = time.time()

    while current_node_xy != end: # Run until the current node is the end node
        new_nodes_created = False
        # Finds the node closest to the end node
        Node.lowest_cost = all_nodes[-1].cost 
        for node in all_nodes:
            if node.cost <= Node.lowest_cost and not node.has_been_parent:
                Node.lowest_cost = node.cost
                Node.best_node = node
                current_node_xy[0], current_node_xy[1] = node.y, node.x #xy to yx       
        
        parent_nodes.append(Node.best_node)
        Node.best_node.has_been_parent = True
        Node.best_node.draw()
        
        # Create surrounding nodes
        for i in range(len(nodes_pattern)):
            all_nodes.append(Node(current_node_xy[0]+nodes_pattern[i][0], current_node_xy[1]+nodes_pattern[i][1], Node.best_node)) # if we have switched between two nodes with the same cost it will fuck up
            if all_nodes[-1].is_valid() == True:
                new_nodes_created = True
                all_nodes[-1].draw()
            else:
                del all_nodes[-1]
                
        if not new_nodes_created:
            if len(all_nodes) == len(parent_nodes):
                print("No solutions available")
                solution_possible = False
                break
    wait()

    if solution_possible:
        print("solution posssible")

        solution = []     
        solution.append(Node.best_node)
        solution_grid[solution[-1].x][solution[-1].y] = "i"
        draw_cell_v2(solution[-1].y, solution[-1].x,  solution_colour) 
        
        # Backtracks
        while solution[-1].start_cost != 0:
            solution.append(solution[-1].parent) # Adds the
            solution_grid[solution[-1].x][solution[-1].y] = "i"
            draw_cell_v2(solution[-1].y, solution[-1].x,  solution_colour) 

        for x in range(vertical):
            print(work_grid[x])

        print("\n")
        for x in range(vertical):
            print(solution_grid[x])

        print("finish")
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        pass

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                return

def drawGrid():
    for y in range(vertical):
        grid_list.append([])
        for x in range(horizontal):
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
    pygame.display.flip()  # Partially updates screen
    
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
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= block_size/3 # take into account that the corner is counted as the origin of the cell
        mouse_y -= block_size/3 # take into account that the corner is counted as the origin of the cell
        draw_cell(mouse_x, mouse_y, obstacle_colour) # Give that cell "start node" status. If the key is pressed again the last node will "lose" its status and a new one wil be start node  
        a, b, x, y = get_closest_cell(mouse_x,mouse_y)
        work_grid[y][x] = "-"
        
    elif pygame.mouse.get_pressed()[2]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= block_size/3 # take into account that the corner is counted as the origin of the cell
        mouse_y -= block_size/3 # take into account that the corner is counted as the origin of the cell
        draw_cell(mouse_x, mouse_y, block_colour) # Give that cell "start node" status. If the key is pressed again the last node will "lose" its status and a new one wil be start node  
        a, b, x, y = get_closest_cell(mouse_x,mouse_y)
        work_grid[y][x] = "0"

def main():
    
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
                    
                    draw_cell_v2(start[1], start[0], block_colour) # Give that cell "start node" status. If the key is pressed again the last node will "lose" its status and a new one wil be start node

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
                    draw_cell_v2(end[1], end[0], block_colour) # Give that cell "start node" status. If the key is pressed again the last node will "lose" its status and a new one wil be start node
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
        pygame.display.flip()

if __name__ == '__main__':
    # Set up the drawing window
    pygame.init()
    window = pygame.display.set_mode([200,200])


    block_size = 20
    background_colour = (0, 0, 0)
    block_colour = (255, 165, 91)
    
    path_block_colour = (255,116, 0)
    parent_colour = (172, 78, 0)

    solution_colour = (105,75,31) #(115,53,40)#(91,49,2)
    obstacle_colour = (23,15,9)

    spacing = 1.05
    start = [0, 0]
    end = [0, 0]
    
    horizontal = 40
    vertical = 30
    height = int(horizontal*block_size*spacing)
    width = int(vertical*block_size*spacing)
    grid_list = []
    
    FONT = pygame.font.SysFont("comicsansms", 20)

    #wait_for_user_input()


    work_grid = [["0" for i in range(horizontal)] for j in range(vertical)] 
    
    start_node = UserNodes(start[0], start[1], None)
    end_node = UserNodes(end[0], end[1], None)
    parent_nodes = []
    all_nodes = []
    nodes_pattern = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]] # Right, left, up, down, upper right, upper left, down right, down left


    window = pygame.display.set_mode([height, width])


    main()
    pygame.quit()


# Done! Time to quit.
pygame.quit()


