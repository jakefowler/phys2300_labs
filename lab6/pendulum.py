import numpy as np
from matplotlib import pyplot as plt
from vpython import *

g = 9.81    # m/s**2
l = 0.1     # meters
W = 0.002   # arm radius
R = 0.01    # ball radius
c = 0.5     # friction
framerate = 100
steps_per_frame = 2
theta_middle = []  # values of angle for graphing later
theta_right = []   # values of angle for graphing later
theta_left = []    # values of angle for graphing later
time_values = []
h = 1.0/(framerate * steps_per_frame)
offset = 2*l + 4*R # offset for the left and the right pendulums

def f_theta_omega(r):
    """
    Pendulum
    """
    theta = r[0]
    omega = r[1]
    ftheta = omega
    fomega = -(g/l)*np.sin(theta) - c*omega
    return np.array([ftheta, fomega], float)

def rung_kutta(angles):
    """
    Funtion that calculates the 4th order Rung-Kutta and returns it
    """
    k1 = h*f_theta_omega(angles)
    k2 = h*f_theta_omega(angles+0.5*k1)
    k3 = h*f_theta_omega(angles+0.5*k2)
    k4 = h*f_theta_omega(angles+k3)
    angles += (k1 + 2*k2 + 2*k3 + k4)/6
    return angles

def update_pos(angles, ball, arm, x_offset):
    """
    Function that gets the new x and y coordinates based on the angles passed in
    It then changes the pos of the ball passed in and the axis of the arm passed in
    """
    x = l*np.sin(angles[0])
    y = -l*np.cos(angles[0])
    ball.pos = vector(x + x_offset, y, 0)
    arm.axis = vector(x, y, 0)

def set_scene():
    """
    Function to create the parts in the scene that don't move
    """
    # stand for pendulum thats based around the size of the arm and ball
    top_stand = box(pos=vector(0, 0, -R), size=vector(R, W, 4*R), color=color.blue) # top of stand
    joint_stand = cylinder(pos=vector(0, 0, -W), axis=vector(0, 0, W*2), radius=R/2, color=color.blue) # cylinder that connects stand to arm
    back_stand = box(pos=vector(0, -(l + 2*R)/2, -R - 2*R), size=vector(R, l + 2*R, W), color = color.blue) # vertical part of stand
    bottom_stand = box(pos=vector(0, -(l + 2*R), -R), size=vector(R, W, 4*R), color=color.blue) # base of stand
    stand = compound([top_stand, joint_stand, back_stand, bottom_stand]) # groups all the parts of the stand together
    stand_left = stand.clone() 
    stand_left.pos.x -= offset # moves it to the left based on how long the arms and the radius of the ball
    stand_right = stand.clone()
    stand_right.pos.x += offset # moves it to the right based on how long the arms and the radius of the ball
    box(pos=vector(0, -(l + 2*R) - W, 0), size=vector(R*70, W, R*10)) # ground   
 
def animatePendulums():
    # Set up initial values
    angles_middle = np.array([np.pi*179/180, 0], float)
    angles_right = np.array([np.pi*30/180, 0], float)
    angles_left = np.array([np.pi*90/180, 0], float)
    # Initial x and y
    x = l*np.sin(angles_middle[0])
    y = -l*np.cos(angles_middle[0])
    # setup the three pendulums
    ball_middle = sphere(pos=vector(x, y, 0), radius=R, color=color.red)
    ball_right = ball_middle.clone()
    ball_right.pos.x += offset
    ball_left = ball_middle.clone()
    ball_left.pos.x -= offset
    arm_middle = cylinder(pos=vector(0, 0, 0), axis=vector(x, y, 0), radius=W)
    arm_right = arm_middle.clone()
    arm_right.pos.x += offset
    arm_left = arm_middle.clone()
    arm_left.pos.x -= offset
    # Loop over some time interval
    dt = 0.01
    t = 0
    while t < 15:
            rate(100)
            for i in range(steps_per_frame):
                angles_middle = rung_kutta(angles_middle)
                angles_right = rung_kutta(angles_right)
                angles_left = rung_kutta(angles_left)

                update_pos(angles_middle, ball_middle, arm_middle, 0)
                update_pos(angles_right, ball_right, arm_right, offset)
                update_pos(angles_left, ball_left, arm_left, -offset)

                theta_middle.append(angles_middle[0]) # used for graphing
                theta_right.append(angles_right[0]) # used for graphing
                theta_left.append(angles_left[0]) # used for graphing
                time_values.append(t)
            t += dt
    return time_values, theta_middle, theta_right, theta_left

def plotPoints(time_values, theta_middle, theta_right, theta_left):
    plt.plot(time_values, theta_middle, label="Middle Pendulum")
    plt.plot(time_values, theta_right, label="Right Pendulum")
    plt.plot(time_values, theta_left, label="Left Pendulum")
    plt.ylabel("Angle in Radians")
    plt.xlabel("Time in Seconds")
    plt.title("Angle of Pendulum over time")
    plt.legend()
    plt.show()   

def main():
    """
    Function that gets everything going
    """
    set_scene()
    time_values, theta_middle, theta_right, theta_left = animatePendulums() 
    plotPoints(time_values, theta_middle, theta_right, theta_left)
    
if __name__ == "__main__":
    main()