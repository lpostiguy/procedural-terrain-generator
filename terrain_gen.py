import numpy as np
import math

# In this project, I decided to generate terrain randomly, meaning that each time the program is run, it generates OPENSCAD code randomly. 
# The position, height, and size of the islands, as well as the number of trees, rocks, and docks, are generated randomly.

# Additionally, we can play with the following parameters to obtain different results. Proportional formulas are used to control the number 
# of islands relative to the terrain's size_x and size_y. Thus, the fewer islands are generated, the greater their chances of being large, 
# and the more islands are generated, the more likely they are to be small.

# Terrain configuration
size_x = 100      # Terrain size x
size_y = 100      # Terrain size y
ocean_height = 3  # Height of the ocean plate
max_height = 25   # Maximum terrain elevation 
num_islands = 7   # Number of islands generated
tree_height = 3   # Height of generated trees
rock_height = 1   # Height of generated rocks
# Maximum number of docks total in terrain generation
max_total_docks = math.ceil(num_islands / 2)


# Function that generates a pine tree
# As a parameter, you can use "leaf_color" to change the color of the tree leaves
def pine_tree(current_height, tree_height, leaf_color, x, y, f):
    # Trunk
    offset = np.random.uniform(0.7,1.2)
    offset_angle = np.random.uniform(0.9,1.1)
    num_leaves = math.ceil(int(tree_height / 0.3) * offset)
    tree_height = math.ceil(tree_height * offset)
    trunk_radius = 0.15 * offset
    for i in range(num_leaves):
        r = trunk_radius * (1 - 0.2 * i/num_leaves)
        z = current_height + i * 0.3
        f.write(
            f"translate([{x}, {y}, {z}]) "
            f"color([0.45,0.20,0]) "
            f"cylinder(h=0.3, r={r}, $fn=12);\n"
        )

    # Leaves
    z_coord = current_height + tree_height
    leaf_length = 1.5 * offset
    leaf_width = 0.06 * offset
    for angle in range(0, 360, 20):
        for i in range(0, tree_height, 1):
            f.write(
                f"translate([{x}, {y}, {z_coord - i + 0.5}]) "
                f"rotate([0, {70 * (offset_angle)}, {angle}]) "
                f"color({leaf_color}) "
                f"cube([{leaf_length}, {leaf_width}, {leaf_width}]);\n"
            )


# Function that generates a palm tree
def palm_tree(current_height, tree_height, x, y, f):
    # Trunk
    num_leaves = int(tree_height / 0.3)
    trunk_radius = 0.25
    for i in range(num_leaves):
        r = trunk_radius * (1 - 0.2 * i/num_leaves)
        z = current_height + i * 0.3
        f.write(
            f"translate([{x}, {y}, {z}]) "
            f"color([0.55,0.27,0.07]) "
            f"cylinder(h=0.3, r={r}, $fn=12);\n"
        )

    # Leaves
    z_coord = current_height + tree_height
    leaf_length = 1.5
    leaf_width = 0.2
    leaf_angle = 45
    # 1st leaf set
    for angle in range(0, 360, 60):
        f.write(
            f"translate([{x}, {y}, {z_coord}]) "
            f"rotate([0,0,{angle}]) "
            f"rotate([{leaf_angle},0,0]) "
            f"color([0,0.8,0]) "
            f"cube([{leaf_length}, {leaf_width}, {leaf_width}]);\n"
        )
    # 2nd leaf set
    for angle in range(0, 360, 80):
        f.write(
            f"translate([{x}, {y}, {z_coord}]) "
            f"rotate([0,0,{angle}]) "
            f"rotate([{leaf_angle},15,]) "
            f"color([0,0.6,0]) "
            f"cube([{leaf_length}, {leaf_width}, {leaf_width}]);\n"
        )


# Function that generates a bush
def bush(current_height, x, y, f):
    number_particles = np.random.randint(30, 60)
    
    for i in range(number_particles):
        pos_x = np.random.uniform(-0.7, 0.7)
        pos_y = np.random.uniform(-0.7, 0.7)
        pos_z = np.random.uniform(0, 0.5)
        f.write(f"translate([{x + pos_x}, {y + pos_y}, {current_height + pos_z}]) color({[0, 0.85, 0]}) cube([{0.1}, {0.1}, {0.1}]);\n")


# Function that generates a rock
def rock(current_height, rock_height, x, y, f):
    rock_color = np.random.uniform(0.4, 0.6)
    num_stones = np.random.randint(1, 16)
    
    f.write(f"translate([{x}, {y}, {current_height}]) color({[rock_color, rock_color, rock_color]}) cube([{1}, {1}, {rock_height}]);\n")
    for i in range(num_stones):
        offset_x = np.random.uniform(-2, 2)
        offset_y = np.random.uniform(-2, 2)
        offset_height = np.random.uniform(0.5, 2)
        f.write(f"translate([{x - offset_x}, {y - offset_y}, {current_height - offset_height}]) color({[rock_color, rock_color, rock_color]}) cube([{1}, {1}, {offset_height}]);\n")


# Function that generates a dock    
def dock(ocean_height, x, y, f):
    dock_length = np.random.randint(8, 16)
    if(dock_length % 4 != 0): dock_length += dock_length % 2
    for i in range(0, dock_length + 1):
        f.write(f"translate([{x - 0.5}, {y + i}, {ocean_height + 1}]) color({[150/255, 75/255, 0]}) cube([{3}, {1}, {0.5}]);\n")
        if(i % 4 == 0):
            f.write(f"translate([{x - 0.25}, {y + i}, {ocean_height}]) color({[100/255, 50/255, 0]}) cube([{0.5}, {0.5}, {1}]);\n")
            f.write(f"translate([{x + 1.75}, {y + i}, {ocean_height}]) color({[100/255, 50/255, 0]}) cube([{0.5}, {0.5}, {1}]);\n")


# Function that generates the terrain based on configuration parameters
def generate_world():
    with open("generated_terrain.scad", "w") as f:
        f.write("// Automatically generated terrain\n")
        f.write("union() {\n")
        
        # Ocean with engraving underneath
        f.write("difference() {\n")
        f.write(f"translate([0, 0, 0]) color([0, 0.4, 1]) cube([{size_x}, {size_y}, {ocean_height}]);\n")
        f.write(f"translate([{size_x/2}, {size_y/2}, {0.5}])\n")
        f.write("mirror([1,0,0]) mirror([0,0,1])\n")
        f.write("linear_extrude(height=1)\n")
        f.write("text(\"LP0 - AM - IFT2125\", size=4, halign=\"center\", valign=\"center\");\n")
        f.write("    }\n")

        total_docks = 0
        total_island_radius = 0

        # Island generation
        for i in range(num_islands):
            xc = np.random.randint(0, size_x * 1.05)  # Island x position
            yc = np.random.randint(0, size_y * 1.05)  # Island y position
            
            # Island size factor based on total island count, existing generated island sizes, and total terrain size in x and y
            radius_multiplier = abs(size_x / 100 - ((num_islands + total_island_radius / size_x) / 20)) / (max(size_x, size_y) / 80)
            
            # Minimum island radius
            min_radius = math.ceil(50 / num_islands)
            
            # Maximum island radius
            max_radius = min(size_x, size_y) * radius_multiplier
            radius = np.random.randint(min_radius, max_radius)
            
            # Random parameters for size, shape, and height of islands
            total_island_radius += radius
            height_factor = np.random.uniform(0.2, 1.0)
            stretch_factor_x = np.random.uniform(0.8, 1.5)
            stretch_factor_y = np.random.uniform(0.8, 1.5)
            max_docks_per_island = math.ceil(radius / 15)
            docks_per_island = 0

            # Island generation
            for x in range(xc - radius, xc + radius, 1):
                for y in range(yc - radius, yc + radius, 1):
                    if 0 <= x < size_x and 0 <= y < size_y:
                        distance = np.sqrt(max(0, ((x - xc) * stretch_factor_x) ** 2 + ((y - yc) * stretch_factor_y) ** 2))
                        if distance < radius:
                            # Closer to center = higher elevation
                            relative_height = (1 - (distance / radius))
                            height = ocean_height + relative_height * (max_height - ocean_height) * height_factor
                            
                            # Random parameter to offset block color to create natural gradients
                            material_offset = np.random.uniform(0.7, 1.2)
                            
                            tree_color_offset = np.random.uniform(0.7, 1.1)

                            # Noise map for block height
                            noise_map = np.random.uniform(-1, 1, size=(size_x, size_y))
                            noise_value = noise_map[x % size_x, y % size_y]
                            height += noise_value * 0.15

                            # Block color based on height for gradient effect
                            if height < ocean_height + (max_height - ocean_height) * 0.15 * material_offset:
                                color = [0.90, 0.90, 0.50]  # Sand
                            elif height > ocean_height + (max_height - ocean_height) * 0.80 * material_offset:
                                color = [1, 1, 1]  # Snow
                            elif height > ocean_height + (max_height - ocean_height) * 0.70 * material_offset:
                                color = [128/255, 128/255, 128/255]  # Rock
                            else:
                                color = [0, 1 / (height / 4), 0]  # Grass

                            f.write(f"translate([{x}, {y}, {ocean_height}]) color({color}) cube([{1}, {1}, {height - ocean_height}]);\n")
                            
                            # Palm tree generation based on elevation and rarity (2% chance per block)
                            if(np.random.randint(0,50) == 1 and height < ocean_height + (max_height - ocean_height) * 0.30 and height > ocean_height + (max_height - ocean_height) * 0.05 and ((x + 2) < size_x) and ((y + 2) < size_y) and ((x - 2) > 0) and ((y - 2) > 0)):
                                palm_tree(height, tree_height, x, y, f)
                            
                            # Pine tree generation based on elevation and rarity (12.5% chance per block)
                            if(np.random.randint(0,8) == 1 and height < ocean_height + (max_height - ocean_height) * 0.55 and height > ocean_height + (max_height - ocean_height) * 0.25 and ((x + 1) < size_x) and ((y + 1) < size_y) and ((x - 1) > 0) and ((y - 1) > 0)):
                                pine_tree(height, tree_height, [0,0.7 * tree_color_offset,0], x, y, f)
                            
                            # Snow pine tree generation based on elevation and rarity (12.5% chance per block)
                            if(np.random.randint(0,8) == 1 and height < ocean_height + (max_height - ocean_height) * 0.80 and height > ocean_height + (max_height - ocean_height) * 0.55 and ((x + 1) < size_x) and ((y + 1) < size_y) and ((x - 1) > 0) and ((y - 1) > 0)):
                                pine_tree(height, tree_height, [1,1,1], x, y, f)
                            
                            # Bush generation based on elevation and rarity (10% chance per block)
                            if(np.random.randint(0,10) == 1 and height < ocean_height + (max_height - ocean_height) * 0.50 and height > ocean_height + (max_height - ocean_height) * 0.20 and ((x + 2) < size_x) and ((y + 2) < size_y) and ((x - 2) > 0) and ((y - 2) > 0)):
                                bush(height, x, y, f)
                            
                            # Rock generation based on elevation and rarity (0.5% chance per block)
                            if(np.random.randint(0,200) == 1 and height < ocean_height + (max_height - ocean_height) * 0.80 and ((x + 10) < size_x) and ((y + 10) < size_y) and ((x - 10) > 0) and ((y - 10) > 0)):
                                rock(height, rock_height, x, y, f)
                            
                            # Dock generation based on elevation and rarity (10% chance per block)
                            if(np.random.randint(0,10) == 1 and total_docks < max_total_docks and height < ocean_height + (max_height - ocean_height) * 0.05 and ((x + 20) < size_x) and ((y + 20) < size_y) and ((x - 20) > 0) and ((y - 20) > 0 and docks_per_island < max_docks_per_island)):
                                dock(ocean_height, x, y, f)
                                total_docks += 1
                                docks_per_island += 1
        f.write("}\n")


# Execute the function to generate the terrain
generate_world()
