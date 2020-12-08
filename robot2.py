##TODO : add this controller to the epucks in the final world
import math
from controller import Robot, Motor, DistanceSensor
# import csci3302_lab3_supervisor
import numpy as np

# Robot Pose Values

pose_x = 0
pose_y = 0
pose_theta = 0

# Constants to help with the Odometry update
WHEEL_FORWARD = 1
WHEEL_STOPPED = 0
WHEEL_BACKWARD = -1

state = "send_pose" # End with the more complex feedback control method!
sub_state = "bearing" # TODO: It may be helpful to use sub_state to designate operation modes within the "turn_drive_turn_control" state

# create the Robot instance.

robot = Robot()
# csci3302_lab3_supervisor.init_supervisor()
# robot = csci3302_lab3_supervisor.supervisor

EPUCK_MAX_WHEEL_SPEED = 0.12880519 # Unnecessarily precise ePuck speed in m/s. REMINDER: motor.setVelocity() takes ROTATIONS/SEC as param, not m/s.
EPUCK_AXLE_DIAMETER = 0.053 # ePuck's wheels are 53mm apart.
EPUCK_WHEEL_RADIUS = 0.0205 # ePuck's wheels are 0.041m in diameter.

# get the time step of the current world.
SIM_TIMESTEP = int(robot.getBasicTimeStep())
from controller import Compass
# get robot's Compass device
compass = robot.getCompass("compass")
# enable the Compass
compass.enable(SIM_TIMESTEP)


# Initialize Motors
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)


# def update_odometry(left_wheel_direction, right_wheel_direction, time_elapsed):
    # '''
    # Given the amount of time passed and the direction each wheel was rotating,
    # update the robot's pose information accordingly
    # '''
    # global pose_x, pose_y, pose_theta, EPUCK_MAX_WHEEL_SPEED, EPUCK_AXLE_DIAMETER
    # pose_theta += (right_wheel_direction - left_wheel_direction) * time_elapsed * EPUCK_MAX_WHEEL_SPEED / EPUCK_AXLE_DIAMETER;
    # pose_x += math.cos(pose_theta) * time_elapsed * EPUCK_MAX_WHEEL_SPEED * (left_wheel_direction + right_wheel_direction)/2.;
    # pose_y += math.sin(pose_theta) * time_elapsed * EPUCK_MAX_WHEEL_SPEED * (left_wheel_direction + right_wheel_direction)/2.;
    # pose_theta = get_bounded_theta(pose_theta)

# def get_bounded_theta(theta):
    # '''
    # Returns theta bounded in [-PI, PI]
    # '''
    # while theta > math.pi: theta -= 2.*math.pi
    # while theta < -math.pi: theta += 2.*math.pi
    # return theta
    
def update_odometry(left_wheel_direction, right_wheel_direction, time_elapsed):
    '''
    #Given the amount of time passed and the direction each wheel was rotating,
    #update the robot's pose information accordingly
    '''
    global pose_x, pose_y, pose_theta, EPUCK_MAX_WHEEL_SPEED, EPUCK_AXLE_DIAMETER
    
    
    r = 0
    l = 0
      
    Ld = EPUCK_MAX_WHEEL_SPEED*time_elapsed *left_wheel_direction
    Rd = EPUCK_MAX_WHEEL_SPEED*time_elapsed *right_wheel_direction
    x = (Ld+Rd)/2
    theta =(Rd-Ld)/EPUCK_AXLE_DIAMETER * .13368
    
    pose_theta += theta
    pose_x = pose_x + ( (math.cos(pose_theta)* x))
    pose_y = pose_y + (-( math.sin(pose_theta)* x))
    # print(pose_x, pose_y, pose_theta)
    
########## MY HELPERS ##################
    
def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))
    
def length(v):
  return math.sqrt(dotproduct(v, v))
  
def angle(A, B):
   
    return math.acos(dotproduct(A, B) / (length(A) * length(B)))

def dist(pointA, pointB):
    return (math.hypot(pointB[0] - pointA[0], pointB[1] - pointA[1]))
 
###############################################
  
def main():
    global robot, state, sub_state
    global leftMotor, rightMotor, SIM_TIMESTEP, WHEEL_FORWARD, WHEEL_STOPPED, WHEEL_BACKWARDS
    global pose_x, pose_y, pose_theta

    last_odometry_update_time = None

    # Keep track of which direction each wheel is turning
    left_wheel_direction = WHEEL_STOPPED
    right_wheel_direction = WHEEL_STOPPED
    

    
    target_pose = None
    
    if state == "send_pose":
            ### post request w current location
        state = "no_target"
           
    if state == "no_target":
        ### get request for target
         if target_pose is None:
            ##setting target
          
            state =  "move_to_target"
            

    # Sensor burn-in period
    for i in range(10): robot.step(SIM_TIMESTEP)
   
    # Main Control :
    while robot.step(SIM_TIMESTEP) != -1:
        # Odometry update code -- do not modify
        if last_odometry_update_time is None:
            last_odometry_update_time = robot.getTime()
        time_elapsed = robot.getTime() - last_odometry_update_time
        update_odometry(left_wheel_direction, right_wheel_direction, time_elapsed)
        last_odometry_update_time = robot.getTime()
        # print("compass:", compass.getValues())
       
   
        
        if state == "move_to_target": 
            sub_state = "starting" 
            
            ## These should be adjused based on which e-puck is currently located and it's target goal
            # goal_angle = angle((-0.625,-0.75), (-.5,-.5))
            
            ###################################
                ## ADJUST THESE VALUES ##
            goal_angle=.37
            goal_dist = dist((-0.625,-0.75), (-.5,-.5)) +.04
            
            ####################################
            if sub_state == "starting":
                guess2 = abs(compass.getValues()[2])
                print("guess2", guess2)
                if guess2 < goal_angle:
                
              
                    leftMotor.setVelocity( -1* (leftMotor.getMaxVelocity()))
                    rightMotor.setVelocity( (rightMotor.getMaxVelocity()))
                    left_wheel_direction = -WHEEL_FORWARD 
                    right_wheel_direction = WHEEL_FORWARD 
                    
                else: 
                    sub_state = "stopped"
                   
                    sub_state = "towards"
                    
            if sub_state == "towards":
                 #TURNING
                if  math.sqrt((pose_x**2 + pose_y**2)) < goal_dist:
                    
                    leftMotor.setVelocity(leftMotor.getMaxVelocity())
                    rightMotor.setVelocity(rightMotor.getMaxVelocity())  
                    left_wheel_direction = WHEEL_FORWARD 
                    right_wheel_direction = WHEEL_FORWARD  
                    
                            
                else:
              
                    sub_state = "stopped"
                    
                    
            if sub_state == "stopped":
            
                leftMotor.setVelocity(0)
                rightMotor.setVelocity(0)
                left_wheel_direction = WHEEL_STOPPED
                right_wheel_direction = WHEEL_STOPPED
            
                    
   
if __name__ == "__main__":
    main()
