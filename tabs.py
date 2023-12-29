import cmu_graphics.libs.pygame_loader as pg
import constants, layers, image
from cmu_cs3_graphics import *

def initialize(app):
    app.tabs = []
    app.image = None

def drawTabs(app):
    drawRect(constants.LEFT_TOOLBAR_WIDTH, 0, app.width - constants.LEFT_TOOLBAR_WIDTH - constants.RIGHT_TOOLBAR_WIDTH,    
             constants.TAB_BAR_HEIGHT, fill=app.theme['tabBarColor'], borderWidth=1, border=app.theme['border'])
    for i, tab in enumerate(app.tabs):
        borderColor = app.theme['border']
        if (app.image == tab):
            borderColor = app.theme['selectedBorder']
        drawRect(constants.LEFT_TOOLBAR_WIDTH + i * constants.TAB_WIDTH, 0, constants.TAB_WIDTH,    
                 constants.TAB_BAR_HEIGHT, fill=app.theme['tabColor'], borderWidth=1, border=borderColor)
        tabLabel = tab.name
        if (len(tabLabel) > 15):
            tabLabel = tabLabel[:14] + '...'
        drawLabel(tabLabel, constants.LEFT_TOOLBAR_WIDTH + i * constants.TAB_WIDTH + constants.TAB_LABEL_BORDER, constants.TAB_BAR_HEIGHT // 2,
                  align='left',fill=app.theme['fontColor'])
        drawRect((constants.LEFT_TOOLBAR_WIDTH + i * constants.TAB_WIDTH) + (0.8 * constants.TAB_WIDTH), 0.1 * constants.TAB_BAR_HEIGHT, 
                  0.8 * constants.TAB_BAR_HEIGHT, 0.8 * constants.TAB_BAR_HEIGHT, fill=app.theme['tabColor'], borderWidth=1, border=app.theme['buttonColor'])  
        x1 = (constants.LEFT_TOOLBAR_WIDTH + i * constants.TAB_WIDTH) + (0.8 * constants.TAB_WIDTH) + (0.1 * (0.8 * constants.TAB_BAR_HEIGHT))
        x2 = (constants.LEFT_TOOLBAR_WIDTH + i * constants.TAB_WIDTH) + (0.8 * constants.TAB_WIDTH) + (0.9 * (0.8 * constants.TAB_BAR_HEIGHT))
        y1 = (0.2 * constants.TAB_BAR_HEIGHT)
        y2 = (0.8 * constants.TAB_BAR_HEIGHT)     
        drawLine(x1, y1, x2, y2, fill=app.theme['fontColor'])
        drawLine(x1, y2, x2, y1, fill=app.theme['fontColor'])

def tabMouseHandler(app, mouseX, mouseY):
    tabSelected = mouseX // constants.TAB_WIDTH

    if (tabSelected < len(app.tabs)):
        x1 = (tabSelected * constants.TAB_WIDTH) + (0.8 * constants.TAB_WIDTH) + (0.1 * (0.8 * constants.TAB_BAR_HEIGHT))
        x2 = (tabSelected * constants.TAB_WIDTH) + (0.8 * constants.TAB_WIDTH) + (0.9 * (0.8 * constants.TAB_BAR_HEIGHT))
        y1 = (0.2 * constants.TAB_BAR_HEIGHT)
        y2 = (0.8 * constants.TAB_BAR_HEIGHT)    
        if (x1 < mouseX < x2 and y1 < mouseY < y2):
            closeTab(app, tabSelected)
        else:    
            app.image = app.tabs[tabSelected]
            app.selectedLayer = app.image.layers[0]
            
def openImage(app, imagePath):
    if ((len(app.tabs) + 1) * constants.TAB_WIDTH <= app.width - constants.RIGHT_TOOLBAR_WIDTH - constants.LEFT_TOOLBAR_WIDTH):
        rawImage = pg.image.load(imagePath)
        photo = image.Image(imagePath.split('/')[-1],rawImage.get_width(), rawImage.get_height())
        photo.layers.append(layers.Layer(rawImage, 0, 0))
        app.tabs.append(photo)
        app.image = app.tabs[-1]
        app.selectedLayer = app.image.layers[0]

def closeTab(app, tabSelected=None):
    if (tabSelected == None):
        tabSelected = app.tabs.index(app.image)
    if (app.tabs[tabSelected] == app.image):
        app.tabs.pop(tabSelected)
        if (len(app.tabs) > 0):
            app.image = app.tabs[0]
            app.selectedLayer = app.image.layers[0]
        else:
            app.image = None
            app.selectedLayer = None
            app.selectedTool = None
    else:
        app.tabs.pop(tabSelected)