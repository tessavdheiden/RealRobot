import math
import time
from support.gps import GPS

v_m = 0.1  # average-speed in m/s +++ for this first attempt the average-speed is a constant (it will depend on action)
FPS = 5  # ???
robot_gps = GPS('robot')

#  motor1 = Motor(23, 24)
#  motor2 = Motor(27, 17)


def get_odo_x():
    # obtaining x by GPS
    init_latitude = None
    current_time = time.time()
    last_frame_time = current_time
    robot_latitude = 0

    sleep_time = 1./FPS - (current_time - last_frame_time)
    if sleep_time > 0:
        time.sleep(sleep_time)
    if robot_gps.is_ready:
        if not init_latitude:
            init_latitude = robot_gps.latitude
        else:
            robot_latitude = robot_gps.latitude - init_latitude  # in m ???
    return robot_latitude


def get_odo_y():
    # obtaining y by GPS
    init_longitude = None
    current_time = time.time()
    last_frame_time = current_time
    robot_longitude = 0

    sleep_time = 1./FPS - (current_time - last_frame_time)
    if sleep_time > 0:
        time.sleep(sleep_time)
    if robot_gps.is_ready:
        if not init_longitude:
            init_longitude = robot_gps.longitude
        else:
            robot_longitude = robot_gps.longitude - init_longitude  # in m ???
    return robot_longitude


def get_odo_theta():  # pending .......
    # obtaining theta by previous trajectory
    theta = math.pi/2
    return theta


def pure_pursuit(x_new, y_new):
    y_1 = -math.sin(get_odo_theta()) * x_new + math.cos(get_odo_theta()) * y_new
    if y_1 >= 0:
        goal_behind = 0
    elif y_1 < 0:
        goal_behind = 1

    if goal_behind == 1:
        if (math.cos(get_odo_theta()) * x_new + math.sin(get_odo_theta()) * y_new) > 0:
            kappa = -1
        elif (math.cos(get_odo_theta()) * x_new + math.sin(get_odo_theta()) * y_new) <= 0:
            kappa = -2
    elif goal_behind == 0:
        current_x = get_odo_x()
        current_y = get_odo_y()
        current_theta = get_odo_theta()

        dx = x_new - current_x
        dy = y_new - current_y
        dl = math.sqrt(dy * dy + dx * dx)
        alpha = math.atan2(dy, dx) + current_theta
        kappa = (2 * math.sin(alpha)) / dl
    return kappa


def kappa_to_v(kappa):
    b = 0.22  # wheel distance in m +++ needs to be adjusted
    if kappa == -1:
        v = [v_m, -v_m]
    elif kappa == -2:
        v = [-v_m, v_m]
    elif kappa >= 0:
        print("converting kappa to v")
        v_l = v_m * (1 - kappa * b)
        v_r = v_m * (1 + kappa * b)
        v = [v_l, v_r]
    return v


def set_speed(v):  # pending .......
    # set output speed to motors
    factor = 1
    speed_left = factor*v[0]
    speed_right = factor*v[1]
    #  motor1.forward(speed_left)
    #  motor2.forward(speed_right)
