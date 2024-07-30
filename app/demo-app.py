import math
import time

import lib.flaschen as flaschen

UDP_IP = 'localhost'
UDP_PORT = 1337
height = 64
width = 64

ft = flaschen.Flaschen(UDP_IP, UDP_PORT, width, height, layer=0)

def distance(x, y, width, height):
    return math.sqrt((width - x)**2 + (height - y)**2)

far_corner_distance = distance(0,0,width,height)

for y in range(0, ft.height):
    for x in range(0, ft.width):
        ft.set(x, y, (0,0,0))
ft.send()
time.sleep(3)

while True:
    for y in range(0, ft.height):
        for x in range(0, ft.width):
            scaled_dist = int(distance(x, y, width, height) / far_corner_distance * 255)
            dist_color = (scaled_dist, scaled_dist, scaled_dist)
            ft.set(x, y, dist_color)
    ft.send()
    time.sleep(3)

    for y in range(0, ft.height):
        for x in range(0, ft.width):
            scaled_dist = 255 - int(distance(x, y, width, height) / far_corner_distance * 255)
            dist_color = (scaled_dist, scaled_dist, scaled_dist)
            ft.set(x, y, dist_color)
    ft.send()
    time.sleep(3)
