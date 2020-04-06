#!/usr/bin/env python3
rows = 10
cols = 10
#grid = [["0" for i in range(cols)] for j in range(rows)] 
#grid2 = [["0" for i in range(cols)] for j in range(rows)] 


grid = [
["0", "0", "0", "-1", "0", "0", "0", "0", "0", "0"],
["0", "0", "0", "-1", "0", "0", "0", "0", "0", "0"],
["0", "0", "0", "-1", "0", "-1", "0", "0", "0", "0"],
["0", "0", "0", "-1", "0", "-1", "0", "0", "0", "0"],
["0", "0", "0", "-1", "0", "-1", "0", "0", "0", "0"],
["0", "0", "0", "-1", "0", "-1", "0", "0", "0", "0"],
["0", "0", "0", "-1", "0", "-1", "-1", "-1", "-1", "0"],
["0", "0", "0", "-1", "0", "-1", "0", "0", "0", "0"],
["0", "0", "0", "0", "0", "-1", "0", "-1", "-1", "-1"],
["0", "0", "0", "0", "0", "-1", "0", "0", "0", "0"]
]

grid2 = [
["0", "0", "0", "-1", "0", "0", "0", "0", "0", "0"],
["0", "0", "0", "-1", "0", "0", "0", "0", "0", "0"],
["0", "0", "0", "-1", "0", "-1", "0", "0", "0", "0"],
["0", "0", "0", "-1", "0", "-1", "0", "0", "0", "0"],
["0", "0", "0", "-1", "0", "-1", "0", "0", "0", "0"],
["0", "0", "0", "-1", "0", "-1", "0", "0", "0", "0"],
["0", "0", "0", "-1", "0", "-1", "-1", "-1", "-1", "0"],
["0", "0", "0", "-1", "0", "-1", "0", "0", "0", "0"],
["0", "0", "0", "0", "0", "-1", "0", "-1", "-1", "-1"],
["0", "0", "0", "0", "0", "-1", "0", "0", "0", "0"]
]


start = [0, 0]
end = [9, 9]

grid[end[0]][end[1]] = "x"
grid[start[0]][start[1]] = "x"
grid2[end[0]][end[1]] = "x"
grid2[start[0]][start[1]] = "x"


current_node_xy = start
all_nodes = []
valid_nodes = []

class Node:

    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent
        self.has_been_parent = False

        self.x_from_start = abs(start[0] - self.x)
        self.y_from_start = abs(start[1] - self.y)
        self.x_from_end = abs(end[0] - self.x)
        self.y_from_end = abs(end[1] - self.y)
        self.cost = self.x_from_end**2 +self.y_from_end**2 + self.x_from_start**2 + self.y_from_start**2
    
    def is_valid(self):
        try:
            rules = [grid[self.x][self.y] != "-1",
            self.x >= 0,
            self.y >= 0,
            ]
            a = True
            for node in valid_nodes:
                if node.x == self.x and node.y == self.y:
                    a = False

            if all(rules) and a or self.x == end[0] and self.y == end[1]:
                return True
            else:
                return False
        except(TypeError, IndexError):
            return False
    
    def draw(self):
        grid[self.x][self.y] = "i"


start_node = Node(start[0], start[1], None)
current_node_xy[0] = start_node.x
current_node_xy[1] = start_node.y
all_nodes.append(start_node) 
valid_nodes.append(start_node) 
parent_nodes = []


lowest_cost = 0
best_node = 0

all_nodes_pattern = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]] # Right, left, up, down, upper right, upper left, down right, down left
while current_node_xy != end:
    lowest_cost = valid_nodes[0].cost 
    best_node = 0

    for node in valid_nodes:
        if node.cost <= lowest_cost and node.has_been_parent == False:
            lowest_cost = node.cost
            best_node = valid_nodes.index(node)
            current_node_xy[0] = node.x
            current_node_xy[1] = node.y
            parent_nodes.append(node)
            node.has_been_parent = True

    for i in range(len(all_nodes_pattern)):
        all_nodes.append(Node(current_node_xy[0]+all_nodes_pattern[i][0], current_node_xy[1]+all_nodes_pattern[i][1], valid_nodes[best_node]))

        if all_nodes[-1].is_valid() == True:
            valid_nodes.append(all_nodes[-1])
            valid_nodes[-1].draw()
        else:
            pass

    for x in range(rows):
        print(grid[x])
    print("\n")
    all_nodes = []

solution = []       
for node in valid_nodes:
    if node.x == end[0] and node.y == end[1]:   
        solution.append(node)
        break

counter = 0
while True:
    solution.append(solution[counter].parent)
    counter +=1
    if solution[-1].x_from_start == 0 and solution[-1].y_from_start == 0:
        break

for node in solution:
    grid2[node.x][node.y] = "i"

for x in range(rows):
    print(grid[x])

print("\n")
for x in range(rows):
    print(grid2[x])
