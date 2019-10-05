import math

def GPStoCartesian(longitude, latitude):
    longitude = longitude / 180 * math.pi
    latitude = latitude / 180 * math.pi
    r = 6371 * 10**3
    x = r * math.cos(latitude) * math.cos(longitude)
    y = r * math.cos(latitude) * math.sin(longitude)
    return (x, y)

def CartesianSpeed(pos_x, pos_y, last_pos_x, last_pos_y):
    vel_x = pos_x - last_pos_x
    vel_y = pos_y - last_pos_y
    return vel_x, vel_y