import math
from controller import Robot, Motor, DistanceSensor
# import csci3302_lab3_supervisor
import numpy as np

import requests

# Robot Pose Values
pose_x = .375
# Multiply -1 then +1 
pose_y = 1.75
pose_theta =  3 * math.pi / 2

# Constants to help with the Odometry update
WHEEL_FORWARD = 1
WHEEL_STOPPED = 0
WHEEL_BACKWARD = -1

state = "send_pose" # End with the more complex feedback control method!
sub_state = "bearing" # TODO: It may be helpful to use sub_state to designate operation modes within the "turn_drive_turn_control" state

# create the Robot instance.
# csci3302_lab3_supervisor.init_supervisor()
# robot = csci3302_lab3_supervisor.supervisor
robot = Robot()

EPUCK_MAX_WHEEL_SPEED = 0.12880519 # Unnecessarily precise ePuck speed in m/s. REMINDER: motor.setVelocity() takes ROTATIONS/SEC as param, not m/s.
EPUCK_AXLE_DIAMETER = 0.053 # ePuck's wheels are 53mm apart.
EPUCK_WHEEL_RADIUS = 0.0205 # ePuck's wheels are 0.041m in diameter.

# get the time step of the current world.
SIM_TIMESTEP = int(robot.getBasicTimeStep())

# Initialize Motors
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)


def update_odometry(left_wheel_direction, right_wheel_direction, time_elapsed):
    '''
    Given the amount of time passed and the direction each wheel was rotating,
    update the robot's pose information accordingly
    '''
    global pose_x, pose_y, pose_theta, EPUCK_MAX_WHEEL_SPEED, EPUCK_AXLE_DIAMETER
    pose_theta += (right_wheel_direction - left_wheel_direction) * time_elapsed * EPUCK_MAX_WHEEL_SPEED / EPUCK_AXLE_DIAMETER;
    pose_x += math.cos(pose_theta) * time_elapsed * EPUCK_MAX_WHEEL_SPEED * (left_wheel_direction + right_wheel_direction)/2.;
    pose_y += math.sin(pose_theta) * time_elapsed * EPUCK_MAX_WHEEL_SPEED * (left_wheel_direction + right_wheel_direction)/2.;
    pose_theta = get_bounded_theta(pose_theta)

def get_bounded_theta(theta):
    '''
    Returns theta bounded in [-PI, PI]
    '''
    while theta > math.pi: theta -= 2.*math.pi
    while theta < -math.pi: theta += 2.*math.pi
    return theta


def main():
    global robot, state, sub_state
    global leftMotor, rightMotor, SIM_TIMESTEP, WHEEL_FORWARD, WHEEL_STOPPED, WHEEL_BACKWARDS
    global pose_x, pose_y, pose_theta

    last_odometry_update_time = None

    # Keep track of which direction each wheel is turning
    left_wheel_direction = WHEEL_STOPPED
    right_wheel_direction = WHEEL_STOPPED

    # Important IK Variable storing final desired pose
    target_pose = None # Populated by the supervisor, only when the target is moved.


    # Sensor burn-in period
    for i in range(10): robot.step(SIM_TIMESTEP)


    time_since_last_get = 0
    # Main Control Loop:
    while robot.step(SIM_TIMESTEP) != -1:
        server_x = None
        # Odometry update code -- do not modify
        if last_odometry_update_time is None:
            last_odometry_update_time = robot.getTime()
        time_elapsed = robot.getTime() - last_odometry_update_time
        update_odometry(left_wheel_direction, right_wheel_direction, time_elapsed)
        last_odometry_update_time = robot.getTime()

        # Get target location -- do not modify
        if target_pose is None:
            target_pose = [0.75,1.5,-.5]
            # target_pose = csci3302_lab3_supervisor.supervisor_get_relative_target_pose()
            # print("New IK Goal Received! Target: %s" % str(target_pose))

        # Your code starts here


        # Error
        bearing_error = math.atan2((target_pose[1] - pose_y),(target_pose[0] - pose_x)) - pose_theta
        distance_error = math.sqrt(((pose_x - target_pose[0])**2)+((pose_y - target_pose[1])**2))
        heading_error = target_pose[2] - pose_theta

        if state == "send_pose":
            ### post request w current location
            server_x = requests.post('http://127.0.0.1:5000/post_coordinates',data={'coordinates': str((pose_x,pose_y))})
            state = "no_target"

        elif state == "no_target":
            ### get request for target
            if time_since_last_get > 0.2:
                time_since_last_get = 0.0
                target_str_x = requests.get('http://127.0.0.1:5000/get_target', cookies=server_x.cookies)
                try:
                    target_pose = eval(target_str_x.text)
                    state =  "move_to_target"
                except SyntaxError, err:
                    pass
            else:
                time_since_last_get += SIM_TIMESTEP / 1000.0
        
                






        elif state == "move_to_target":
            p1= .1
            p2= .1
            p3= .1
            x= p1* distance_error

            if (distance_error > 0.02):

                 phi_l = (x - (bearing_error*EPUCK_AXLE_DIAMETER)/2)/EPUCK_WHEEL_RADIUS
                 phi_r = (x + (bearing_error*EPUCK_AXLE_DIAMETER)/2)/EPUCK_WHEEL_RADIUS
                 L = (phi_l / (abs(phi_l) + abs(phi_r)))
                 R = (phi_r / (abs(phi_l) + abs(phi_r)))
                 leftMotor.setVelocity( leftMotor.getMaxVelocity() * L)
                 rightMotor.setVelocity( rightMotor.getMaxVelocity() * R)
                 left_wheel_direction = WHEEL_FORWARD * L
                 right_wheel_direction = WHEEL_FORWARD * R
            elif  (distance_error <= 0.001):
                leftMotor.setVelocity(0)
                rightMotor.setVelocity(0)
                left_wheel_direction = WHEEL_STOPPED
                right_wheel_direction = WHEEL_STOPPED
            
                state = "send_pose"

            #      phi_l = (x - (((p3*heading_error)+(p2*bearing_error))*EPUCK_AXLE_DIAMETER/2)/EPUCK_WHEEL_RADIUS)
            #      phi_r = (x + (((p3*heading_error)+(p2*bearing_error))*EPUCK_AXLE_DIAMETER/2)/EPUCK_WHEEL_RADIUS)
            #      L = (phi_l / (abs(phi_l) + abs(phi_r)))
            #      R = (phi_r / (abs(phi_l) + abs(phi_r)))
            # 
            #      leftMotor.setVelocity(leftMotor.getMaxVelocity() * L)
            #      rightMotor.setVelocity(rightMotor.getMaxVelocity()* R)
            #      left_wheel_direction = WHEEL_FORWARD * L
            #      right_wheel_direction = WHEEL_FORWARD *  R
            # if abs(distance_error) < 0.001 and abs(heading_error) < 0.001:
            #      leftMotor.setVelocity(0)
            #      rightMotor.setVelocity(0)
            #      left_wheel_direction = WHEEL_STOPPED
            #      right_wheel_direction = WHEEL_STOPPED

        print("Current pose: [%5f, %5f, %5f]\t\t Target pose: [%5f, %5f, %5f]\t\t Errors: [%5f, %5f, %5f]" % (pose_x, pose_y, pose_theta, target_pose[0], target_pose[1], target_pose[2],bearing_error, distance_error, heading_error))

if __name__ == "__main__":
    main()
