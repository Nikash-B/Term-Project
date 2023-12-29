from cmu_graphics import shape_logic
from cmu_graphics.libs import pygame_loader as pygame
import cmu_graphics

# This function is a modified version of the redrawAll function in cmu_graphics.py
def customRedrawAll(self, screen, cairo_surface, ctx):
    shape = shape_logic.Rect({
        'noGroup': True,
        'top': 0,
        'left': 0,
        'width': self.width,
        'height': self.height,
        'fill': self.background,
    })
    shape.draw(ctx)

    ctx.save()
    try:
        self._tlg._shape.draw(ctx)
    finally:
        ctx.restore()

    ctx.save()
    try:
        if self.shouldDrawInspector():
            self.inspector.draw(ctx)
    finally:
        ctx.restore()

    # Get the cairo buffer and convert it from BGRA to RGBA
    data_string = cairo_surface.get_data()

    # Create PyGame surface
    pygame_surface = pygame.image.frombuffer(data_string, (self.width, 
                     self.height), 'RGBA')

    # Show PyGame surface
    screen.blit(pygame_surface, (0,0))

    self.callUserFn('drawImage', [screen])

cmu_graphics.cmu_graphics.App.redrawAll = customRedrawAll