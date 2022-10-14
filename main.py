from tkinter import Y
from perlin_noise import PerlinNoise
from airfoil import *
import math
import pandas as pd
import random
import numpy as np
import cv2
import matplotlib.pyplot as plt

red1 = np.array((227, 68, 39, 255))
orange1 = np.array((241, 99, 35, 255))
yellow1 = np.array((255, 208, 33, 255))
black1 = np.array((75, 75, 75, 255))
white = np.array((255, 255, 255, 255))
transparent = np.array((255, 255, 255, 0))
eyeblack = np.array((0, 0, 0, 255))

WIDTH = 1280
HEIGTH = 1280
EYE_WIDTH = 60
EYE_THICKNESS = 20

KOI_THICKNESS_MAX = 0.30
KOI_THICKNESS_MIN = 0.18


def main():
    eye_x = int(random.uniform(0.075, 0.10) * WIDTH)
    thickness = random.uniform(KOI_THICKNESS_MIN, KOI_THICKNESS_MAX)

    x1 = np.linspace(0, WIDTH, WIDTH * 4)
    x2 = np.append(x1, np.flip(x1, 0))

    y1 = naca4_symmetric(thickness, WIDTH, x1)
    y2 = np.append(y1, np.flip(-y1, 0))
    y2 = y2 + HEIGTH/2

    # Pattern 1
    seed1 = random.randint(1,999999)
    octave1 = random.randint(1,6)
    threshold1 = random.uniform(-0.18, 0.2)
    pig1 = layering(y1, seed1, octave1, threshold1, orange1, True)

    # Pattern 2
    seed2 = random.randint(1,999999)
    octave2 = random.randint(1,6)
    threshold2 = random.uniform(-0.18, 0.2)
    pig2 = layering(y1, seed2, octave2, threshold2, red1)

    # Pattern 3
    seed3 = random.randint(1,999999)
    octave3 = random.randint(2,8)
    threshold3 = random.uniform(-0.18, 0.2)
    pig3 = layering(y1, seed3, octave3, threshold3, black1)

    eyelayer = eye_layer(y1, eye_x)

    koi = plt.figure()
    shape = koi.add_subplot(111)
    shape.plot(x2, y2, 'k-', lw=0.5)
    shape.axis([0, WIDTH, 0, HEIGTH])
    shape.axis('off')
    
    shape.imshow(pig1)
    shape.imshow(pig2)
    shape.imshow(pig3)
    shape.imshow(eyelayer)
    plt.show() 
    koi.savefig("koi.png", transparent=True)

def layering(shape : float, seed : int, octave : int, threshold : float,\
             color, first_layer : bool = False):

    noise = PerlinNoise(octaves=octave, seed=seed)
    layer = np.empty([WIDTH, HEIGTH, 4], dtype = int)

    for x in range(WIDTH):
        limit = shape[4*x]
        upper_limit =  limit + HEIGTH/2
        lower_limit = -limit + HEIGTH/2

        for y in range(HEIGTH):
            if y > lower_limit and y < upper_limit:
                pigment1_intensity = (noise([x/WIDTH, y/HEIGTH]))

                if pigment1_intensity > threshold:
                    layer[y, x] = color

                else:
                    if first_layer:
                        layer[y, x] = white
                    else:
                        layer[y, x] = transparent

            else:
                layer[y, x] = transparent

    return layer


def eye_layer(shape : float, eye_pos : int):
    layer = np.full([WIDTH, HEIGTH, 4], transparent)

    for i in range(EYE_WIDTH):
        for j in range(int(EYE_THICKNESS * math.sin(math.radians(-75 + 255 * i/EYE_WIDTH)))):
            layer[int(shape[4 * eye_pos + 4 * i] + HEIGTH/2) - j, eye_pos + i] = eyeblack
            layer[-int(shape[4 * eye_pos + 4 * i] + HEIGTH/2) + j, eye_pos + i] = eyeblack

    return layer


if __name__== "__main__":
    main()