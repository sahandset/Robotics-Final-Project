def mapping (robot_coords, target_coords):
    my_dictionary = {}
    # Ensures that we have enough robots to make our shape
    if (len(robot_coords) == len(target_coords)):
        for i in range(len(robot_coords)):
            my_dictionary[robot_coords[i]]=target_coords[i]

    return my_dictionary


# Test 
# robot_coords = [(0,1,0),(0,2,4),(0,5,9)]
# target_coords = [(4,1,8),(5,3,6),(5,3,0)]

