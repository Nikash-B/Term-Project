class Layer(object):
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
    
    def copy(self):
        return Layer(self.image.copy(), self.x, self.y)