# Param robot_coords = List of Coords
# Param target_coords = List of Coords

def mapping (robot_coords, target_coords):
    my_dictionary = {}
    # Ensures that we have enough robots to make our shape
    if (len(robot_coords) == len(target_coords)):
        for i in range(len(robot_coords)):
            temp = []
            temp.append(target_coords[i])

            # Batch 1 - Top Left
            if (robot_coords[i][0] < 1 and robot_coords[i][1] == 1.95):
                temp.append(1)

            # Batch 2 - Top Right 
            elif (robot_coords[i][0] > 1 and robot_coords[i][1] == 1.95):
                temp.append(2)

            # Batch 3 - Bottom Left
            elif (robot_coords[i][0] < 1 and robot_coords[i][1] == 1.75):
                temp.append(3)

            # Batchn 4 - Bottom Right
            elif (robot_coords[i][0] > 1 and robot_coords[i][1] == 1.75):
                temp.append(4)

            my_dictionary[robot_coords[i]]=temp

    return my_dictionary

# Test 
rc = [(0.125,1.95),(1.125,1.95),(0.125,1.75),(1.125,1.75)]
tc = [(1,2),(2,3),(3,4),(4,5)]

print(mapping(rc,tc))




