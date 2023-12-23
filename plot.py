from typing import List, Tuple
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
 
def input_to_lines(input): 
    with open(input, 'r') as file:
        lines = file.read().splitlines()
    return lines    

lines = input_to_lines("plot_input")

cubes:List[Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]] = []
min_x = None
min_y = None
min_z = None
max_x = None
max_y = None
max_z = None
for pos, line in enumerate(lines):
    if "#" in line:
        continue
    if ':' in line:
        id, rest = line.split(":")
        line = rest.strip()
        id = int(id)
    else: 
        id = pos
    p1, p2 = line.split(" => ")
    x1, y1, z1 = [int(d) for d in p1.split(",")]
    x2, y2, z2 = [int(d) for d in p2.split(",")]
    if min_x == None: 
        min_x = min(x1, x2)
        min_y = min(y1, y2)
        min_z = min(z1, z2)
        max_x = max(x1, x2)
        max_y = max(y1, y2)
        max_z = max(z1, z2)
    else: 
        min_x = min(min_x, x1, x2)
        min_y = min(min_y, y1, z2)
        min_z = min(min_z, z1, z2)
        max_x = max(max_x, x1, x2)
        max_y = max(max_y, y1, z2)
        max_z = max(max_z, z1, z2)
    cubes.append((id, (x1, y1, z1), (x2, y2, z2)))

# Create axis
max_axis = max(max_x, max_y, max_z)
axes = [max_axis + 2, max_axis + 2, max_axis + 2]

# Control colour
colours = np.empty(axes + [4], dtype=np.float32)

# Control Transparency
alpha = 0.9
 
# Create Data
data = np.zeros(axes, dtype=bool)
colour_list = [
    [1, 0, 0, alpha],
    [1, 1, 0, alpha],
    [1, 0, 1, alpha],
    [0, 1, 0, alpha]
]
for c in cubes:
    id, p1, p2 = c
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    for x in range(min(x1, x2), max(x1, x2) + 1):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            for z in range(min(z1, z2), max(z1, z2) + 1):
                data[x][y][z] = True
                colours[x][y][z] = colour_list[id % len(colour_list)]
 
 

 
# Plot figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
 
# Voxels is used to customizations of the
# sizes, positions and colors.
ax.voxels(data, facecolors=colours)


plt.show()

