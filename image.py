import cmu_graphics.libs.pygame_loader as pg

class Image(object):
    def __init__(self, name, width, height):
        self.layers = []
        self.width = width
        self.height = height
        self.name = name
    
    def saveImage(self):
        canvas = pg.Surface((self.width, self.height))
        canvas.set_alpha(255)

        for layer in self.layers[::-1]:
            canvas.blit(layer.image, (layer.x, layer.y))

        pg.image.save(canvas, f"Images/Edited {self.name.split('.')[0]}.png")