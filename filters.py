# For citations for RGB to HSV conversion and vice versa, see citations.txt

import cmu_graphics.libs.pygame_loader as pg
import image_utilities
import math

# Box Blur: https://en.wikipedia.org/wiki/Box_blur
# Takes the average of the neighboring pixels.
def blur(app):
    def findAverage(copyOfImage, r, c, width):
        r_sum, g_sum, b_sum, a_sum = 0, 0, 0, 0
        count = 0
        for i in range(max(r-width, 0), min(r + width + 1, copyOfImage.get_width())):
            for j in range(max(c-width, 0), min(c + width + 1, copyOfImage.get_height())):
                r, g, b, a = copyOfImage.get_at((i,j))
                r_sum += r
                g_sum += g
                b_sum += b
                a_sum += a
                count += 1
        return r_sum // count, g_sum // count, b_sum // count, a_sum // count

    copyOfImage = app.selectedLayer.image.copy()
    for i in range(app.selectedLayer.image.get_width()):
        for j in range(app.selectedLayer.image.get_height()):
            r, g, b, a = findAverage(copyOfImage, i, j, 1)
            app.selectedLayer.image.set_at((i, j), pg.Color(r, g, b, a))

# Takes the average of r, g, and b values of the pixels and sets that for the 
# r, g, and b values so they are all equal.
def grayScale(app):
    for i in range(app.selectedLayer.image.get_width()):
        for j in range(app.selectedLayer.image.get_height()):
            r, g, b, a = app.selectedLayer.image.get_at((i,j))
            average = (r+g+b)//3
            app.selectedLayer.image.set_at((i, j), pg.Color(average,average,average, a))

def rotateCounterClockwise(app):
    rotatedImage = pg.Surface((app.selectedLayer.image.get_height(), app.selectedLayer.image.get_width()))
    rotatedImage.set_alpha(255)
    for i in range(app.selectedLayer.image.get_width()):
        for j in range(app.selectedLayer.image.get_height()):
            rotatedImage.set_at((j, app.selectedLayer.image.get_width() - i), app.selectedLayer.image.get_at((i,j)))
    app.selectedLayer.image = rotatedImage

def rotateClockwise(app):
    rotatedImage = pg.Surface((app.selectedLayer.image.get_height(), app.selectedLayer.image.get_width()))
    rotatedImage.set_alpha(255)
    for i in range(app.selectedLayer.image.get_width()):
        for j in range(app.selectedLayer.image.get_height()):
            rotatedImage.set_at((app.selectedLayer.image.get_height() - j, i), app.selectedLayer.image.get_at((i,j)))
    app.selectedLayer.image = rotatedImage

def invertColors(app):
    for i in range(app.selectedLayer.image.get_width()):
        for j in range(app.selectedLayer.image.get_height()):
            r, g, b, a = app.selectedLayer.image.get_at((i,j))
            r,g,b = 255 - r, 255 - g, 255 - b
            app.selectedLayer.image.set_at((i, j), pg.Color(r, g, b, a))

# For the following filters, each pixel was converted from RGB to HSV, where H
# is the Hue of the pixel, S is the saturation of the pixel and V is the value 
# or birghtness of the pixel. Each of the following filters then takes an 
# injective function applied to one of these three properties. For example, 
# for the brighten method, each pixel has its brightness adjusted relative to
# how bright the pixel originally was.

# Someone helped to outline the implementation of the Filter class, 
# the SaturateFilter class, and the DesaturateFilter class.

class Filter(object):
    def getS(self, s):
        return s    

    def getV(self, v):
        return v

    def run(self, app):
        for i in range(app.selectedLayer.image.get_width()):
            for j in range(app.selectedLayer.image.get_height()):
                r, g, b, a = app.selectedLayer.image.get_at((i,j))
                h, s, v = image_utilities.getHSVValues(r, g, b)
                s = self.getS(s)
                v = self.getV(v)
                r,g,b = image_utilities.getRGBValues(h, s, v)
                app.selectedLayer.image.set_at((i, j), pg.Color(round(r), round(g), round(b), a))

class BrightenFilter(Filter):
    def __init__(self):
        self.filterAmount = 1.5
        self.filterConstant =  1 / (self.filterAmount ** 2)

    def getV(self, v):
        return (v + (v * self.filterConstant)) / (v + self.filterConstant)

class DarkenFilter(Filter):
    def __init__(self):
        self.filterAmount = 1
        self.filterConstant = 1 / (self.filterAmount ** 2)

    def getV(self, v):
        return (self.filterConstant * v) / (1 + self.filterConstant - v)

class IncreaseContrastFilter(Filter):
    def __init__(self):
        self.filterAmount = 5
        self.filterConstant = ((math.e ** (self.filterAmount/2)) + 1) / ((math.e ** (self.filterAmount/2)) - 1)

    def getV(self, v):
        return (self.filterConstant / (1 + math.e ** (-self.filterAmount * (v - 0.5)))) - ((self.filterConstant - 1) / 2)

class DecreaseContrastFilter(Filter):
    def __init__(self):
        self.filterAmount = 5
        self.filterConstant = ((math.e ** (self.filterAmount/2)) + 1) / ((math.e ** (self.filterAmount/2)) - 1)

    def getV(self, v):
        return (2 * v) - ((self.filterConstant / (1 + math.e ** (-self.filterAmount * (v - 0.5)))) - ((self.filterConstant - 1) / 2))

class SaturateFilter(Filter):
    def __init__(self):
        self.filterAmount = 1
        self.filterConstant = 1 / (self.filterAmount ** 2)

    def getS(self, s):
        return (s + (s * self.filterConstant)) / (s + self.filterConstant)

class DesaturateFilter(Filter):
    def __init__(self):
        self.filterAmount = 1
        self.filterConstant = 1 / (self.filterAmount ** 2)

    def getS(self, s):
        return (self.filterConstant * s) / (1 + self.filterConstant - s)

brighten = BrightenFilter().run
darken = DarkenFilter().run
increaseContrast = IncreaseContrastFilter().run
decreaseContrast = DecreaseContrastFilter().run
desaturate = DesaturateFilter().run
saturate = SaturateFilter().run
