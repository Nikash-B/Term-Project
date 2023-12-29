# For citations, see citations.txt

from cmu_cs3_graphics import *
import cmu_graphics.libs.pygame_loader as pg
import image_display_fix
import filters, constants, tabs, toolbars, themes

'''
TODO:
Copy and paste for layers
Be able to put images on top of each other.
Sliders on the toolbars
Loading files from finder.
Name the layers.
More tools for the photo editor:
    - Sharpen Image filter
    - Drawing on the image
    - Seam carving
View photos in gallery on LHS of screen if within a folder --> folder manipulation, scaling images, and scrolling
Sharing image on social media (instagram, twitter, facebook)
Dark mode / themes --> convert dictionary keys to dark1, dark2, light1, light2, etc.
Turn the photo editor into an executable file.
'''

def onAppStart(app):
    tabs.initialize(app)
    app.width = 1000 + constants.LEFT_TOOLBAR_WIDTH + constants.RIGHT_TOOLBAR_WIDTH
    app.height = 800 + constants.TAB_BAR_HEIGHT
    app.theme = themes.darkTheme #Can change the theme of the application by choosing
    # either themes.darkTheme or themes.lightTheme before compiling the code
    toolbars.initializeTools(app)

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = app.theme['imageBackground'])
    tabs.drawTabs(app)
    toolbars.drawLeftToolbar(app, 0, 0)
    toolbars.drawRightToolbar(app, app.width - constants.RIGHT_TOOLBAR_WIDTH, 0)
    toolbars.drawLayersList(app, 0, app.height- constants.LAYER_LIST_HEIGHT)
    if (not app.image):
        drawLabel('Open an image to start editing!', app.width // 2, app.height // 2, size = 25, fill = app.theme['fontColor'])
    else:
        scaleFactor = getScaleFactor(app)
        centerX, centerY = getCenterXAndCenterY(app)
        drawRect(centerX - 1, centerY - 1, scaleFactor * app.image.width + 2, scaleFactor * app.image.height + 2,
                 border='black', borderWidth=1, fill=None)

def drawImage(app, screen):
    if (app.image):
        canvas = pg.Surface((app.image.width, app.image.height))
        canvas.set_alpha(255)
        scaleFactor = getScaleFactor(app)

        for layer in app.image.layers[::-1]:
            canvas.blit(layer.image, (layer.x, layer.y))

        canvas = pg.transform.scale(canvas, (round(canvas.get_width() * scaleFactor), round(canvas.get_height() * scaleFactor)))

        layerOutline = pg.Surface((round(app.selectedLayer.image.get_width() * scaleFactor), 
                                   round(app.selectedLayer.image.get_height() * scaleFactor)))
        layerOutline.set_alpha(255)

        for x in range(layerOutline.get_width()):
            layerOutline.set_at((x, 0), themes.convertCMUToPG(app.theme['selectedBorder']))
            layerOutline.set_at((x, layerOutline.get_height() - 1), themes.convertCMUToPG(app.theme['selectedBorder']))

        for y in range(layerOutline.get_width()):
            layerOutline.set_at((0, y), themes.convertCMUToPG(app.theme['selectedBorder']))
            layerOutline.set_at((layerOutline.get_width() - 1, y), themes.convertCMUToPG(app.theme['selectedBorder']))

        canvas.blit(layerOutline, (round(app.selectedLayer.x * scaleFactor), round(app.selectedLayer.y * scaleFactor)))
        centerX, centerY = getCenterXAndCenterY(app)
        screen.blit(canvas, (centerX, centerY)) 

def onMousePress(app, mouseX, mouseY):
    if (constants.LEFT_TOOLBAR_WIDTH < mouseX < constants.TAB_WIDTH * len(app.tabs) + constants.LEFT_TOOLBAR_WIDTH
        and 0 < mouseY < constants.TAB_BAR_HEIGHT):
        tabs.tabMouseHandler(app, mouseX - constants.LEFT_TOOLBAR_WIDTH, mouseY)
    if (app.width - constants.RIGHT_TOOLBAR_WIDTH < mouseX):
        toolbars.rightToolBarMouseHandler(app, mouseX - app.width + constants.RIGHT_TOOLBAR_WIDTH, mouseY)
    if (mouseX < constants.LEFT_TOOLBAR_WIDTH and mouseY < app.height - constants.LAYER_LIST_HEIGHT):
        toolbars.leftToolBarMouseHandler(app, mouseX, mouseY)
    if (mouseX < constants.LEFT_TOOLBAR_WIDTH and mouseY > app.height - constants.LAYER_LIST_HEIGHT):
        toolbars.layerListMouseHandler(app, mouseX, mouseY - app.height + constants.LAYER_LIST_HEIGHT)
    if (constants.LEFT_TOOLBAR_WIDTH < mouseX < app.width - constants.RIGHT_TOOLBAR_WIDTH and 
        constants.TAB_BAR_HEIGHT < mouseY < app.height and app.image):
        scaleFactor = getScaleFactor(app)
        centerX, centerY = getCenterXAndCenterY(app)
        toolbars.imageMouseHandler(app, (mouseX - centerX) / scaleFactor, (mouseY - centerY) / scaleFactor)

def onMouseDrag(app, mouseX, mouseY):
    if (constants.LEFT_TOOLBAR_WIDTH < mouseX < app.width - constants.RIGHT_TOOLBAR_WIDTH and 
        constants.TAB_BAR_HEIGHT < mouseY < app.height and app.image):
        scaleFactor = getScaleFactor(app)
        centerX, centerY = getCenterXAndCenterY(app)
        toolbars.imageDragHandler(app, (mouseX - centerX) / scaleFactor, (mouseY - centerY) / scaleFactor)

def onMouseRelease(app, mouseX, mouseY):
    if (constants.LEFT_TOOLBAR_WIDTH < mouseX < app.width - constants.RIGHT_TOOLBAR_WIDTH and 
        constants.TAB_BAR_HEIGHT < mouseY < app.height and app.image):
        scaleFactor = getScaleFactor(app)
        centerX, centerY = getCenterXAndCenterY(app)
        toolbars.imageReleaseHandler(app, (mouseX - centerX) / scaleFactor, (mouseY - centerY) / scaleFactor)

def getScaleFactor(app):
    maxWidth = app.width - constants.LEFT_TOOLBAR_WIDTH - constants.RIGHT_TOOLBAR_WIDTH - constants.IMAGE_BORDER
    maxHeight = app.height - constants.TAB_BAR_HEIGHT - constants.IMAGE_BORDER
    scaleFactor = min([1, maxWidth / app.image.width, maxHeight / app.image.height])
    return scaleFactor

def getCenterXAndCenterY(app):
    scaleFactor = getScaleFactor(app)
    centerX = ((app.width - constants.LEFT_TOOLBAR_WIDTH - constants.RIGHT_TOOLBAR_WIDTH) // 2) +\
                constants.LEFT_TOOLBAR_WIDTH - (scaleFactor * app.image.width // 2)
    centerY = ((app.height - constants.TAB_BAR_HEIGHT) // 2) + constants.TAB_BAR_HEIGHT -  (scaleFactor * app.image.height // 2)
    return centerX, centerY

runApp(title='Photo Editor')