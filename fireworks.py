import os
import time
import math
from random import random
from vector2d import Vector2D
from colorama import Fore, Style

FPS = 240
VEL = 0
ACC = 700
RAD = 0
BOR = 2

COLORS = (Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE,
          Fore.MAGENTA, Fore.CYAN, Fore.WHITE)


def get_frame_height():
    return (os.get_terminal_size().lines - 1) * 2


def get_frame_width():
    return os.get_terminal_size().columns


class Frame:
    def __init__(self, width=get_frame_width(), height=get_frame_height()):
        self.width = width
        self.height = height
        self.buffer = [False] * (self.width * self.height)

    def reset(self):
        self.width = get_frame_width()
        self.height = get_frame_height()
        self.buffer = [False] * (self.width * self.height)


def move_home():
    print("\033[0;0H", end='')


def circle(center: Vector2D, radius: int | float, border: int | float, frame: Frame):
    top_left = center - Vector2D(radius, radius)
    bottom_right = center + Vector2D(radius, radius)

    for y in range(max(int(top_left.y), 0), min(math.ceil(bottom_right.y) + 1, frame.height)):
        for x in range(max(int(top_left.x), 0), min(math.ceil(bottom_right.x) + 1, frame.width)):
            point = Vector2D(x+0.5, y+0.5)
            dif = point.distance_to(center)
            if (dif <= radius and dif >= (radius-border)):
                if (0 <= x and x < frame.width and 0 <= y and y < frame.height):
                    frame.buffer[y*frame.width + x] = True
    return frame.buffer


def show(frame: Frame, color: str):
    frame_string = ''
    row = [''] * frame.width
    table = ((' ', ','), ('\'', '#'))
    for y in range(int(frame.height/2)):
        for x in range(frame.width):
            top = frame.buffer[(2*y + 0)*frame.width + x]
            btm = frame.buffer[(2*y + 1)*frame.width + x]
            row[x] = table[1 if top else 0][1 if btm else 0]
        row_string = ''.join(row)
        frame_string = frame_string + row_string  # + '\n'
    move_home()
    print(color + frame_string)
    # R  | G  | Y  | B  | M  | C  | W
    # 31 | 32 | 33 | 34 | 35 | 36 | 37


def main():
    frame = Frame()
    cen = Vector2D(frame.width / 2, frame.height / 2)
    rad = RAD
    vel = VEL
    deltaT = 1 / FPS
    color = Style.BRIGHT + COLORS[int(random() * len(COLORS))]
    # direction = (random() - 0.5)
    target = Vector2D(frame.width * random() * 1.5,
                      frame.height * random() * 1.5)

    start_time = time.time()

    while (True):
        try:
            frame.reset()
            if 4 * rad * rad > frame.width * frame.width + frame.height * frame.height:
                cen = Vector2D(frame.width * (0.33 + random() * 0.34),
                               frame.height * (0.33 + random() * 0.34))
                rad = RAD
                vel = VEL
                color = Style.BRIGHT + COLORS[int(random() * len(COLORS))]
                # direction = (random() - 0.5)
                target = Vector2D(frame.width * random() * 1.5,
                                  frame.height * random() * 1.5)
            frame.buffer = circle(cen, rad, BOR, frame)
            # frame.buffer = circle(cen, int(rad / 2), BOR, frame)
            frame.buffer = circle(cen, int(rad / 2), int(rad / 2), frame)
            show(frame, color)
            # print("DT: %.4f ms, FPS: %.4f, vel: %.4f" %
            #       (1000 * deltaT, (1/deltaT), vel), end='')
            temp_dt = time.time() - start_time
            time.sleep(max(0, 1 / FPS - temp_dt))
            deltaT = time.time() - start_time
            start_time = time.time()
            rad = rad + (vel * deltaT)
            cen = cen + (cen - target) * vel * deltaT * 0.02
            vel = vel + ACC * deltaT
        except (KeyboardInterrupt):
            print(Style.RESET_ALL)
            break


if __name__ == '__main__':
    main()
