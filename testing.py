from asyncio.windows_events import NULL
from concurrent.futures import thread
import tkinter as tk
from airfoil import *
import numpy as np
import time
from Koi import Koi
from tkKoi import tkKoi
from queue import Empty, Queue
from threading import Thread
from multiprocessing import Process, Queue as processQueue 
import matplotlib.pyplot as plt
import os


red1 = np.array((227, 68, 39, 255))
orange1 = np.array((241, 99, 35, 255))
yellow1 = np.array((255, 208, 33, 255))
black1 = np.array((75, 75, 75, 255))
white = np.array((255, 255, 255, 255))
transparent = np.array((255, 255, 255, 0))
eyeblack = np.array((0, 0, 0, 255))

color_list = [ red1,
                orange1,
                yellow1,
                black1
                ]

WIDTH = 1000
HEIGHT = 1000
MARGIN = 50

thrd = []
q = processQueue()
queue = []
t = []
fish = []
tk_fish = []
new_loc = []

number_of_koi = 3
dev_mode = False

def main():
    koi_number = np.random.randint(1,11)
    generate_kois(number_of_koi)
    
    while q.qsize() != number_of_koi:
        if dev_mode: print(str(q.qsize()))
        continue

    time.sleep(0.15)
    q.put(None)

    print(q.qsize()-1)
    for koi in iter(q.get, None):
        fish.append(koi)
        generate_koi_img(koi)
    print(len(fish))

    window = tk.Tk()
    canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg='skyblue')
    canvas.pack()

    for i in range(len(fish)):
        x, y = random_location()
        tk_fish.append(tkKoi(window, canvas, x, y, fish[i].filename))
        t.append(Thread(target=new_location, args=(np.random.randint(2,4),)))
        queue.append(Queue(maxsize=1))
        new_location(i, 0)
        new_loc.append(None)

    while True:
        for i in range(len(fish)):
            if queue[i].empty():
                if not t[i].is_alive():
                    t[i] = None
                    t[i] = Thread(target=new_location, args=(i,np.random.randint(2,12),))
                    t[i].start()

            else:
                new_loc[i] = queue[i].get()

            tk_fish[i].move(new_loc[i])

        window.update()
        time.sleep(0.01)

    window.mainloop()


def generate_kois(n : int):
    for i in range(n):
        color_num = np.random.randint(1,4)
        layer = None
        layer = []
        for j in range(color_num):
            layer.append(color_list[np.random.randint(0,4)])

        thrd.append(Process(target=enqueue_koi, args=(i, layer, q)))
        if dev_mode: print(str(i) + " started")
        thrd[i].start()


def enqueue_koi(index : int, layer : list , queue : processQueue):
    koi = Koi(("Koi_"+ str(index + 1)), layer)
    queue.put(koi)


def generate_koi_img(koi : Koi):
    # path = os.path.abspath(__file__)
    full_path = "koi_folder/" + koi.name + ".png"
    image = plt.figure()
    layers = image.add_subplot(111)
    layers.plot(koi.shape[0], koi.shape[1], 'k-', lw=0.5)
    layers.axis([0, 600, 0, 600])
    layers.axis('off')

    for pigment in koi.pig_layers:
        layers.imshow(pigment)
    layers.imshow(koi.eye)
    image.savefig(full_path, transparent=True, format = 'png')
    koi.filename = full_path
    image.clf()
    plt.close()


def new_location(q_index : int, delay : int):
    time.sleep(delay)
    queue[q_index].put(random_location())


def random_location():
    x = np.random.randint(MARGIN, WIDTH - MARGIN)
    y = np.random.randint(MARGIN, HEIGHT - MARGIN)
    if dev_mode: print(x, y)
    return [x, y]


if __name__== "__main__":
    main()