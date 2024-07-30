import flaschen
import time

UDP_IP = 'localhost'
UDP_PORT = 1337
rows = 64
cols = 64

ft = flaschen.Flaschen(UDP_IP, UDP_PORT, cols, rows)

r = 0
g = 0
b = 0
while True:
    for y in range(0, ft.height):
        for x in range(0, ft.width):
            ft.set(x, y, (r,g,b))
    ft.send()

    time.sleep(3)

    r = (r + 10) % 256
    g = (r + 20) % 256
    b = (r + 14) % 256
