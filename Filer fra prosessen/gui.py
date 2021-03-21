import pygame
import time

block_size = 40
background_colour = (255, 255, 255)
block_colour = (96, 110, 100)
spacing = 1.05
rows = 10
cols = 10

height = int(rows*block_size*spacing)
width = int(cols*block_size*spacing)
grid_list = []

# Set up the drawing window
pygame.init()
window = pygame.display.set_mode([height, width])


def drawGrid():
    for y in range(cols):
        grid_list.append([])
        for x in range(rows):
            rect = pygame.Rect(int(x*spacing*block_size), int(y*spacing*block_size), block_size, block_size)
            pygame.draw.rect(window, block_colour, rect, 0)
            grid_list[y].append([int(x*spacing*block_size), int(y*spacing*block_size)])
    

def draw_cell(in_x, in_y, colour):
    x, y = get_closest_cell(in_x, in_y)

    rect = pygame.Rect(x, y, block_size, block_size)
    pygame.draw.rect(window, colour, rect, 0)

def get_closest_cell(in_x, in_y):
    lowest_difference = 100
    closest_cell = [0,0]
    for y in range(len(grid_list)):
        for x in range(len(grid_list[y])):
            difference = abs(grid_list[y][x][0]- in_x) + abs(grid_list[y][x][1]- in_y)
            if difference < lowest_difference:
                lowest_difference = difference
                closest_cell = grid_list[y][x]
    print(closest_cell)
    return closest_cell

def walls():
    button_clicked = False
    if pygame.mouse.get_pressed()[0]:
        draw_colour = (0,0,0)
        button_clicked = True
    elif pygame.mouse.get_pressed()[2]:
        draw_colour = block_colour
        button_clicked = True

    if button_clicked:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= block_size/3 # take into account that the corner is counted as the origin of the cell
        mouse_y -= block_size/3 # take into account that the corner is counted as the origin of the cell
        draw_cell(mouse_x, mouse_y, draw_colour) # Give that cell "start node" status. If the key is pressed again the last node will "lose" its status and a new one wil be start node  


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
                draw_cell(mouse_x, mouse_y, (0,255,0)) # Give that cell "start node" status. If the key is pressed again the last node will "lose" its status and a new one wil be start node
                
            if event.key == pygame.K_e: # mark cell as end_node
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_x -= block_size/3 # take into account that the corner is counted as the origin of the cell
                mouse_y -= block_size/3 # take into account that the corner is counted as the origin of the cell
                draw_cell(mouse_x, mouse_y, (255,0,0)) # Give that cell "start node" status. If the key is pressed again the last node will "lose" its status and a new one wil be start node
           
            if event.key == pygame.K_SPACE: # mark cell as end_node
                pass
                #run algorithm

    # Draw the grid and display the new image
    walls()
    pygame.display.update()

# Done! Time to quit.
pygame.quit()
