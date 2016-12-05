import math
import random
import time
import os
from tkinter import *
from PIL import Image, ImageTk


class Mandelbrot(Frame):
    def __init__(self, xCenter, yCenter, delta, h, w, bailout, parent):
        Frame.__init__(self, parent)
        self.h = h
        self.w = w
        self.xCenter = xCenter
        self.yCenter = yCenter
        self.delta = delta
        self.xmin = xCenter - delta  # more of the same...
        self.xmax = xCenter + delta
        self.ymin = yCenter + delta
        self.ymax = yCenter - delta
        self.bailout = bailout
        self.c, self.z = 0, 0
        self.zoomFactor = 0.2
        self.setPalette()
        self.parent = parent
        self.parent.title("Mandelbrot")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.pixels = []
        self.draw()
        parent.bind("<Button-1>", self.clickEvent)

    def clickEvent(self, event):
        self.xCenter = translate(event.x, 0, self.w, self.xmin, self.xmax)
        self.yCenter = translate(event.y, self.h, 0, self.ymin, self.ymax)
        self.update(self.zoomFactor)
        print("Current canvas center: ", self.xCenter, self.yCenter)

    def update(self, factor):
        self.delta *= factor
        self.xmax = self.xCenter + self.delta
        self.ymax = self.yCenter - self.delta
        self.xmin = self.xCenter - self.delta
        self.ymin = self.yCenter + self.delta
        print('-' * 20)
        self.draw()

    def draw(self):
        start = time.time()
        self.getOrbits()
        print("Orbits: {} seconds".format(time.time() - start))
        start = time.time()
        self.drawPixels(self.pixels)
        self.canvas.create_image(10, 10, image=self.background, anchor=NW)
        print("Pixels: {} seconds".format(time.time() - start))
        self.canvas.pack(fill=BOTH, expand=1)

    def getOrbits(self):
        pixels = []
        for x in range(self.w):
            for y in range(self.h):
                self.setC(x, y)
                escapeTime = self.getEscapeTime(0, self.c, self.bailout)
                pixels.append((x, y, self.palette[escapeTime % 256]))
        self.pixels = pixels

    def setC(self, col, row):
        re = translate(col, 0, self.w, self.xmin, self.xmax)
        im = translate(row, 0, self.h, self.ymax, self.ymin)
        self.c = complex(re, im)

    def drawPixels(self, colorList):
        img = Image.new('RGB', (self.w, self.h), "black")
        pixels = img.load()  # create the pixel map
        for p in colorList:
            pixels[p[0], p[1]] = p[2]
        photoimg = ImageTk.PhotoImage(img)
        self.background = photoimg

    def getEscapeTime(self, z, c, bailout):
        for i in range(bailout):
            if abs(z) > 2:
                return i
            z = z*z + c
        return 0

    def setPalette(self):
        palette = [(0, 0, 0)]
        redb = 2 * math.pi / (random.randint(0, 128) + 128)
        redc = 256 * random.random()
        greenb = 2 * math.pi / (random.randint(0, 128) + 128)
        greenc = 256 * random.random()
        blueb = 2 * math.pi / (random.randint(0, 128) + 128)
        bluec = 256 * random.random()
        for i in range(256):
            r = clamp(int(256 * (0.5 * math.sin(redb * i + redc) + 0.5)))
            g = clamp(int(256 * (0.5 * math.sin(greenb * i + greenc) + 0.5)))
            b = clamp(int(256 * (0.5 * math.sin(blueb * i + bluec) + 0.5)))
            palette.append((r, g, b))
            # palette.append("#{0:02x}{1:02x}{2:02x}".format(r, g, b))
        self.palette = palette


def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)


def clamp(x):
    return max(0, min(x, 255))


def main():
    master = Tk()
    height = width = round(master.winfo_screenheight()*0.9)
    render = Mandelbrot(-0.7, 0, 1.7, height, width, 70, master)
    master.geometry("{}x{}".format(width, height))
    master.mainloop()

main()
