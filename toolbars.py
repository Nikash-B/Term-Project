# For citations, see citations.txt

from cmu_cs3_graphics import *
import constants, tabs, layers, filters, themes
import os, math
import cmu_graphics.libs.pygame_loader as pg

def drawLeftToolbar(app, x, y):
    drawRect(x, y, constants.LEFT_TOOLBAR_WIDTH, app.height - constants.LAYER_LIST_HEIGHT, fill = app.theme['leftToolBarColor'])
    if (app.selectedTool):
        app.leftToolBarMap[app.selectedTool](app)

def drawRightToolbar(app, x, y):
    drawRect(x, y, constants.RIGHT_TOOLBAR_WIDTH, app.height, fill = app.theme['rightToolBarColor'])
    for i in range(len(app.toolList)):
        borderColor = app.theme['border']
        if (app.selectedTool == app.toolList[i]):
            borderColor = app.theme['selectedBorder']
        drawRect(x, y + i * constants.TOOL_BUTTON_HEIGHT, constants.RIGHT_TOOLBAR_WIDTH,
              constants.TOOL_BUTTON_HEIGHT, fill = app.theme['rightToolBarColor'], borderWidth=1, border=borderColor)
        drawLabel(app.toolList[i], x + constants.RIGHT_TOOLBAR_WIDTH // 2, y + (i + 0.5) * constants.TOOL_BUTTON_HEIGHT, 
                  fill = app.theme['fontColor'])

def drawLayersList(app, x, y):
    drawRect(x, y, constants.LEFT_TOOLBAR_WIDTH, constants.LAYER_LIST_HEIGHT, fill = app.theme['layersListColor'])
    if (app.image):
        for i in range(len(app.image.layers)):
            borderColor = app.theme['border']
            if (app.image.layers[i] == app.selectedLayer):
                borderColor = app.theme['selectedBorder']
            drawRect(x, y + i * constants.TOOL_BUTTON_HEIGHT , constants.LEFT_TOOLBAR_WIDTH,
                     constants.TOOL_BUTTON_HEIGHT, fill = app.theme['layersListColor'], borderWidth=1, border=borderColor)
            drawLabel(f'Layer {i + 1}', x + constants.LEFT_TOOLBAR_WIDTH // 2, y + (i + 0.5) * constants.TOOL_BUTTON_HEIGHT,
                      fill = app.theme['fontColor'])


def initializeTools(app):
    app.toolList = ['Open Image', 'Save Image', 'Change Theme', 'Gray Scale', 'Invert Colors', 'Brightness Tools', 'Blur', 'Contrast Tools', 'Saturation Tools', 
                    'Rotate Image', 'Layer Tools', 'Move Layer', 'Lasso']
    app.selectedTool = None
    app.leftToolBarMap = {'Save Image': saveImageLeftToolBar,'Change Theme': changeThemeLeftToolBar, 'Gray Scale': grayScaleLeftToolBar, 'Invert Colors': invertColorsLeftToolBar, 
                          'Brightness Tools': brightnessToolsLeftToolBar, 'Blur': blurLeftToolBar, 'Contrast Tools': contrastToolsLeftToolBar, 
                          'Saturation Tools': saturationToolsLeftToolBar, 'Open Image': openImageLeftToolBar, 'Rotate Image': rotationToolsLeftToolBar, 
                          'Layer Tools': layerToolsLeftToolBar, 'Move Layer': moveLayerLeftToolBar, 'Lasso': lassoLeftToolBar}
    app.leftToolBarMouseHandler = {'Save Image': saveImageMouseHandler, 'Change Theme': changeThemeMouseHandler, 'Gray Scale': grayScaleMouseHandler, 'Invert Colors': invertColorsMouseHandler, 
                                   'Brightness Tools': brightnessToolsMouseHandler, 'Blur': blurMouseHandler, 'Contrast Tools': contrastToolsMouseHandler, 
                                   'Saturation Tools': saturationToolsMouseHandler, 'Open Image': openImageMouseHandler, 'Rotate Image': rotationToolsMouseHandler,
                                   'Layer Tools': layerToolsMouseHandler,}
    app.layerTools = ['Duplicate Layer', 'Delete Layer', 'Change Layer Order Up', 'Change Layer Order Down', 'Merge Down']

def leftToolBarMouseHandler(app, mouseX, mouseY):
    if (app.selectedTool):
        app.leftToolBarMouseHandler[app.selectedTool](app, mouseX, mouseY)

def rightToolBarMouseHandler(app, mouseX, mouseY):
    toolIndex = mouseY // constants.TOOL_BUTTON_HEIGHT
    if (toolIndex < len(app.toolList)):
        if (toolIndex == 0 or toolIndex == 2 or app.tabs):
            app.selectedTool = app.toolList[toolIndex]

def layerListMouseHandler(app, mouseX, mouseY):
    layerIndex = mouseY // constants.TOOL_BUTTON_HEIGHT
    if (layerIndex < len(app.image.layers)):
        app.selectedLayer = app.image.layers[layerIndex]

def saveImageLeftToolBar(app):
    drawLabel('Click the Save Image button to save', constants.LEFT_TOOLBAR_WIDTH / 15, constants.TAB_BAR_HEIGHT // 2, fill = app.theme['fontColor'], align = 'left')
    drawLabel('the image.', constants.LEFT_TOOLBAR_WIDTH / 15, constants.TAB_BAR_HEIGHT, fill = app.theme['fontColor'], align = 'left')
    drawRect(constants.LEFT_TOOLBAR_WIDTH / 8, 2 * constants.TAB_BAR_HEIGHT, 3 * constants.LEFT_TOOLBAR_WIDTH / 4, constants.TAB_BAR_HEIGHT,
             fill = app.theme['buttonColor'], border = app.theme['border'])
    drawLabel('Save Image', constants.LEFT_TOOLBAR_WIDTH / 6, 2.5 * constants.TAB_BAR_HEIGHT, fill = app.theme['buttonFontColor'], align = 'left')

def changeThemeLeftToolBar(app):
    drawLabel('Change the theme by clicking', constants.LEFT_TOOLBAR_WIDTH / 15, constants.TAB_BAR_HEIGHT // 2, fill = app.theme['fontColor'], align = 'left')
    drawLabel('one of the buttons below.', constants.LEFT_TOOLBAR_WIDTH / 15, constants.TAB_BAR_HEIGHT, fill = app.theme['fontColor'], align = 'left')
    
    lightThemeButtonBorderColor = app.theme['border']
    if (app.theme == themes.lightTheme):
        lightThemeButtonBorderColor = app.theme['selectedBorder']

    darkThemeButtonBorderColor = app.theme['border']
    if (app.theme == themes.darkTheme):
        darkThemeButtonBorderColor = app.theme['selectedBorder']

    drawRect(constants.LEFT_TOOLBAR_WIDTH / 8, 2 * constants.TAB_BAR_HEIGHT, 3 * constants.LEFT_TOOLBAR_WIDTH / 4, constants.TAB_BAR_HEIGHT,
             fill = app.theme['buttonColor'], border = lightThemeButtonBorderColor)
    drawLabel('Light Theme', constants.LEFT_TOOLBAR_WIDTH / 6, 2.5 * constants.TAB_BAR_HEIGHT, fill = app.theme['buttonFontColor'], align = 'left')
    drawRect(constants.LEFT_TOOLBAR_WIDTH / 8, 3.5 * constants.TAB_BAR_HEIGHT, 3 * constants.LEFT_TOOLBAR_WIDTH / 4, constants.TAB_BAR_HEIGHT,
             fill = app.theme['buttonColor'], border = darkThemeButtonBorderColor)
    drawLabel('Dark Theme', constants.LEFT_TOOLBAR_WIDTH / 6, 4 * constants.TAB_BAR_HEIGHT, fill = app.theme['buttonFontColor'], align = 'left')


def grayScaleLeftToolBar(app):
    drawLabel('Apply grayscale to the image.', constants.LEFT_TOOLBAR_WIDTH / 8, constants.TAB_BAR_HEIGHT // 2, fill = app.theme['fontColor'], align = 'left')
    drawRect(constants.LEFT_TOOLBAR_WIDTH / 8, constants.TAB_BAR_HEIGHT, 3 * constants.LEFT_TOOLBAR_WIDTH / 4, constants.TAB_BAR_HEIGHT,
             fill = app.theme['buttonColor'], border = app.theme['border'])
    drawLabel('Apply Grayscale', constants.LEFT_TOOLBAR_WIDTH / 6, 1.5 * constants.TAB_BAR_HEIGHT, fill = app.theme['buttonFontColor'], align = 'left')
    
def invertColorsLeftToolBar(app):
    drawLabel('Invert the colors of the image.', constants.LEFT_TOOLBAR_WIDTH / 8, constants.TAB_BAR_HEIGHT // 2, fill = app.theme['fontColor'], align = 'left')
    drawRect(constants.LEFT_TOOLBAR_WIDTH / 8, constants.TAB_BAR_HEIGHT, 3 * constants.LEFT_TOOLBAR_WIDTH / 4, constants.TAB_BAR_HEIGHT,
             fill = app.theme['buttonColor'], border = app.theme['border'])
    drawLabel('Invert Colors', constants.LEFT_TOOLBAR_WIDTH / 6, 1.5 * constants.TAB_BAR_HEIGHT, fill = app.theme['buttonFontColor'], align = 'left')
    

def brightnessToolsLeftToolBar(app):
    drawLabel('Make the image brighter or darker.', constants.LEFT_TOOLBAR_WIDTH / 15, constants.TAB_BAR_HEIGHT // 2, fill = app.theme['fontColor'], align = 'left')
    drawRect(constants.LEFT_TOOLBAR_WIDTH / 8, constants.TAB_BAR_HEIGHT, 3 * constants.LEFT_TOOLBAR_WIDTH / 4, constants.TAB_BAR_HEIGHT,
             fill = app.theme['buttonColor'], border = app.theme['border'])
    drawLabel('Brighten Image', constants.LEFT_TOOLBAR_WIDTH / 6, 1.5 * constants.TAB_BAR_HEIGHT, fill = app.theme['buttonFontColor'], align = 'left')
    drawRect(constants.LEFT_TOOLBAR_WIDTH / 8, 2.5 * constants.TAB_BAR_HEIGHT, 3 * constants.LEFT_TOOLBAR_WIDTH / 4, constants.TAB_BAR_HEIGHT,
             fill = app.theme['buttonColor'], border = app.theme['border'])
    drawLabel('Darken Image', constants.LEFT_TOOLBAR_WIDTH / 6, 3 * constants.TAB_BAR_HEIGHT, fill = app.theme['buttonFontColor'], align = 'left')

def blurLeftToolBar(app):
    drawLabel('Blur the image.', constants.LEFT_TOOLBAR_WIDTH / 8, constants.TAB_BAR_HEIGHT // 2, fill = app.theme['fontColor'], align = 'left')
    drawRect(constants.LEFT_TOOLBAR_WIDTH / 8, constants.TAB_BAR_HEIGHT, 3 * constants.LEFT_TOOLBAR_WIDTH / 4, constants.TAB_BAR_HEIGHT,
             fill = app.theme['buttonColor'], border = app.theme['border'])
    drawLabel('Blur Image', constants.LEFT_TOOLBAR_WIDTH / 6, 1.5 * constants.TAB_BAR_HEIGHT, fill = app.theme['buttonFontColor'], align = 'left')


def contrastToolsLeftToolBar(app):
    drawLabel('Change the contrast of the colors', constants.LEFT_TOOLBAR_WIDTH / 15, constants.TAB_BAR_HEIGHT // 2, fill = app.theme['fontColor'], align = 'left')
    drawLabel('in the image.', constants.LEFT_TOOLBAR_WIDTH / 15, constants.TAB_BAR_HEIGHT, fill = app.theme['fontColor'], align = 'left')
    drawRect(constants.LEFT_TOOLBAR_WIDTH / 8, 2 * constants.TAB_BAR_HEIGHT, 3 * constants.LEFT_TOOLBAR_WIDTH / 4, constants.TAB_BAR_HEIGHT,
             fill = app.theme['buttonColor'], border = app.theme['border'])
    drawLabel('Increase Constrast', constants.LEFT_TOOLBAR_WIDTH / 6, 2.5 * constants.TAB_BAR_HEIGHT, fill = app.theme['buttonFontColor'], align = 'left')
    drawRect(constants.LEFT_TOOLBAR_WIDTH / 8, 3.5 * constants.TAB_BAR_HEIGHT, 3 * constants.LEFT_TOOLBAR_WIDTH / 4, constants.TAB_BAR_HEIGHT,
             fill = app.theme['buttonColor'], border = app.theme['border'])
    drawLabel('Decrease Constrast', constants.LEFT_TOOLBAR_WIDTH / 6, 4 * constants.TAB_BAR_HEIGHT, fill = app.theme['buttonFontColor'], align = 'left')


def saturationToolsLeftToolBar(app):
    drawLabel('Change the saturation of the colors', constants.LEFT_TOOLBAR_WIDTH / 15, constants.TAB_BAR_HEIGHT // 2, fill = app.theme['fontColor'], align = 'left')
    drawLabel('in the image.', constants.LEFT_TOOLBAR_WIDTH / 15, constants.TAB_BAR_HEIGHT, fill = app.theme['fontColor'], align = 'left')
    drawRect(constants.LEFT_TOOLBAR_WIDTH / 8, 2 * constants.TAB_BAR_HEIGHT, 3 * constants.LEFT_TOOLBAR_WIDTH / 4, constants.TAB_BAR_HEIGHT,
             fill = app.theme['buttonColor'], border = app.theme['border'])
    drawLabel('Increase Saturation', constants.LEFT_TOOLBAR_WIDTH / 6, 2.5 * constants.TAB_BAR_HEIGHT, fill = app.theme['buttonFontColor'], align = 'left')
    drawRect(constants.LEFT_TOOLBAR_WIDTH / 8, 3.5 * constants.TAB_BAR_HEIGHT, 3 * constants.LEFT_TOOLBAR_WIDTH / 4, constants.TAB_BAR_HEIGHT,
             fill = app.theme['buttonColor'], border = app.theme['border'])
    drawLabel('Decrease Saturation', constants.LEFT_TOOLBAR_WIDTH / 6, 4 * constants.TAB_BAR_HEIGHT, fill = app.theme['buttonFontColor'], align = 'left')

def rotationToolsLeftToolBar(app):
    drawLabel('Rotate the image in the clockwise', constants.LEFT_TOOLBAR_WIDTH / 15, constants.TAB_BAR_HEIGHT // 2, fill = app.theme['fontColor'], align = 'left')
    drawLabel('or counter-clockwise orientation.', constants.LEFT_TOOLBAR_WIDTH / 15, constants.TAB_BAR_HEIGHT, fill = app.theme['fontColor'], align = 'left')
    drawRect(constants.LEFT_TOOLBAR_WIDTH / 8, 2 * constants.TAB_BAR_HEIGHT, 3 * constants.LEFT_TOOLBAR_WIDTH / 4, constants.TAB_BAR_HEIGHT,
             fill = app.theme['buttonColor'], border = app.theme['border'])
    drawLabel('Rotate Clockewise', constants.LEFT_TOOLBAR_WIDTH / 6, 2.5 * constants.TAB_BAR_HEIGHT, fill = app.theme['buttonFontColor'], align = 'left')
    drawRect(constants.LEFT_TOOLBAR_WIDTH / 8, 3.5 * constants.TAB_BAR_HEIGHT, 3 * constants.LEFT_TOOLBAR_WIDTH / 4, constants.TAB_BAR_HEIGHT,
             fill = app.theme['buttonColor'], border = app.theme['border'])
    drawLabel('Rotate Counter-Clockewise', constants.LEFT_TOOLBAR_WIDTH / 6, 4 * constants.TAB_BAR_HEIGHT, fill = app.theme['buttonFontColor'], align = 'left')

def layerToolsLeftToolBar(app):
    for i in range (len(app.layerTools)):
        drawRect(0, i * constants.TOOL_BUTTON_HEIGHT, constants.LEFT_TOOLBAR_WIDTH,
              constants.TOOL_BUTTON_HEIGHT, fill = app.theme['leftToolBarColor'], borderWidth=1, border=app.theme['border'])
        drawLabel(app.layerTools[i], constants.LEFT_TOOLBAR_WIDTH // 2, (i + 0.5) * constants.TOOL_BUTTON_HEIGHT, 
                  fill = app.theme['fontColor'])


def moveLayerLeftToolBar(app):
    drawLabel('Drag the mouse to move the layer', constants.LEFT_TOOLBAR_WIDTH / 15, constants.TAB_BAR_HEIGHT // 2, fill = app.theme['fontColor'], align = 'left')
    drawLabel('around the screen.', constants.LEFT_TOOLBAR_WIDTH / 15, constants.TAB_BAR_HEIGHT, fill = app.theme['fontColor'], align = 'left')
    

def lassoLeftToolBar(app):
    drawLabel('Drag the mouse to form the shape', constants.LEFT_TOOLBAR_WIDTH / 15, constants.TAB_BAR_HEIGHT // 2, fill = app.theme['fontColor'], align = 'left')
    drawLabel('of the layer you want to create.', constants.LEFT_TOOLBAR_WIDTH / 15, constants.TAB_BAR_HEIGHT, fill = app.theme['fontColor'], align = 'left')
    

def openImageLeftToolBar(app):
    imageList = os.listdir('Images')
    imageList = [image for image in imageList if image.split('.')[-1] in constants.VALID_FILE_TYPES]
    for i in range(len(imageList)):
        imageName = imageList[i].split('/')[-1]
        drawRect(0, i * constants.TOOL_BUTTON_HEIGHT, constants.LEFT_TOOLBAR_WIDTH,
              constants.TOOL_BUTTON_HEIGHT, fill = app.theme['leftToolBarColor'], borderWidth=1, border=app.theme['border'])
        drawLabel(imageName, constants.LEFT_TOOLBAR_WIDTH // 2, (i + 0.5) * constants.TOOL_BUTTON_HEIGHT, 
                  fill = app.theme['fontColor'])

def saveImageMouseHandler(app, mouseX, mouseY):
    if (constants.LEFT_TOOLBAR_WIDTH / 8 < mouseX <  (7/8) * constants.LEFT_TOOLBAR_WIDTH and 
        (7/4) * constants.TAB_BAR_HEIGHT < mouseY < (11/4) *  constants.TAB_BAR_HEIGHT):
        app.image.saveImage()

def changeThemeMouseHandler(app, mouseX, mouseY):
    if (constants.LEFT_TOOLBAR_WIDTH / 8 < mouseX <  (7/8) * constants.LEFT_TOOLBAR_WIDTH and 
        (7/4) * constants.TAB_BAR_HEIGHT < mouseY < (11/4) *  constants.TAB_BAR_HEIGHT):
        app.theme = themes.lightTheme
    elif(constants.LEFT_TOOLBAR_WIDTH / 8 < mouseX <  (7/8) * constants.LEFT_TOOLBAR_WIDTH and 
        3.5 * constants.TAB_BAR_HEIGHT < mouseY < 4.5 *  constants.TAB_BAR_HEIGHT):
        app.theme = themes.darkTheme

def grayScaleMouseHandler(app, mouseX, mouseY):
    if (constants.LEFT_TOOLBAR_WIDTH / 8 < mouseX <  (7/8) * constants.LEFT_TOOLBAR_WIDTH and 
        (3/4) * constants.TAB_BAR_HEIGHT < mouseY < (7/4) *  constants.TAB_BAR_HEIGHT):
        filters.grayScale(app)

def invertColorsMouseHandler(app, mouseX, mouseY):
    if (constants.LEFT_TOOLBAR_WIDTH / 8 < mouseX <  (7/8) * constants.LEFT_TOOLBAR_WIDTH and 
        (3/4) * constants.TAB_BAR_HEIGHT < mouseY < (7/4) *  constants.TAB_BAR_HEIGHT):
        filters.invertColors(app)

def brightnessToolsMouseHandler(app, mouseX, mouseY):
    if (constants.LEFT_TOOLBAR_WIDTH / 8 < mouseX <  (7/8) * constants.LEFT_TOOLBAR_WIDTH and 
        (3/4) * constants.TAB_BAR_HEIGHT < mouseY < (7/4) *  constants.TAB_BAR_HEIGHT):
        filters.brighten(app)
    elif(constants.LEFT_TOOLBAR_WIDTH / 8 < mouseX <  (7/8) * constants.LEFT_TOOLBAR_WIDTH and 
        2.5 * constants.TAB_BAR_HEIGHT < mouseY < 3.5 *  constants.TAB_BAR_HEIGHT):
        filters.darken(app)

def blurMouseHandler(app, mouseX, mouseY):
    if (constants.LEFT_TOOLBAR_WIDTH / 8 < mouseX <  (7/8) * constants.LEFT_TOOLBAR_WIDTH and 
        (3/4) * constants.TAB_BAR_HEIGHT < mouseY < (7/4) *  constants.TAB_BAR_HEIGHT):
        filters.blur(app)

def contrastToolsMouseHandler(app, mouseX, mouseY):
    if (constants.LEFT_TOOLBAR_WIDTH / 8 < mouseX <  (7/8) * constants.LEFT_TOOLBAR_WIDTH and 
        (7/4) * constants.TAB_BAR_HEIGHT < mouseY < (11/4) *  constants.TAB_BAR_HEIGHT):
        filters.increaseContrast(app)
    elif(constants.LEFT_TOOLBAR_WIDTH / 8 < mouseX <  (7/8) * constants.LEFT_TOOLBAR_WIDTH and 
        3.5 * constants.TAB_BAR_HEIGHT < mouseY < 4.5 *  constants.TAB_BAR_HEIGHT):
        filters.decreaseContrast(app)

def saturationToolsMouseHandler(app, mouseX, mouseY):
    if (constants.LEFT_TOOLBAR_WIDTH / 8 < mouseX <  (7/8) * constants.LEFT_TOOLBAR_WIDTH and 
    (7/4) * constants.TAB_BAR_HEIGHT < mouseY < (11/4) *  constants.TAB_BAR_HEIGHT):
        filters.saturate(app)
    elif(constants.LEFT_TOOLBAR_WIDTH / 8 < mouseX <  (7/8) * constants.LEFT_TOOLBAR_WIDTH and 
    3.5 * constants.TAB_BAR_HEIGHT < mouseY < 4.5 *  constants.TAB_BAR_HEIGHT):
        filters.desaturate(app)

def rotationToolsMouseHandler(app, mouseX, mouseY):
    if (constants.LEFT_TOOLBAR_WIDTH / 8 < mouseX <  (7/8) * constants.LEFT_TOOLBAR_WIDTH and 
        (7/4) * constants.TAB_BAR_HEIGHT < mouseY < (11/4) *  constants.TAB_BAR_HEIGHT):
        filters.rotateClockwise(app)
    elif(constants.LEFT_TOOLBAR_WIDTH / 8 < mouseX <  (7/8) * constants.LEFT_TOOLBAR_WIDTH and 
        3.5 * constants.TAB_BAR_HEIGHT < mouseY < 4.5 *  constants.TAB_BAR_HEIGHT):
        filters.rotateCounterClockwise(app)

def layerToolsMouseHandler(app, mouseX, mouseY):
    toolIndex = mouseY // constants.TOOL_BUTTON_HEIGHT
    if (toolIndex < len(app.layerTools)):
        layerTool = app.layerTools[toolIndex]
        layerIndex = app.image.layers.index(app.selectedLayer)
        
        if (layerTool == 'Duplicate Layer'):
            app.image.layers.insert(layerIndex, app.selectedLayer.copy())
        elif (layerTool == 'Delete Layer'):
            app.image.layers.pop(layerIndex)
            if (len(app.image.layers) == 0):
                tabs.closeTab(app)
            else:
                app.selectedLayer = app.image.layers[0]
        elif (layerTool == 'Change Layer Order Up'):
            if (layerIndex != 0):
                app.image.layers[layerIndex], app.image.layers[layerIndex - 1] = app.image.layers[layerIndex - 1], app.image.layers[layerIndex]
                app.selectedLayer = app.image.layers[layerIndex - 1]
        elif (layerTool == 'Change Layer Order Down'):
            if (layerIndex != len(app.image.layers) - 1):
                app.image.layers[layerIndex], app.image.layers[layerIndex + 1] = app.image.layers[layerIndex + 1], app.image.layers[layerIndex]
                app.selectedLayer = app.image.layers[layerIndex + 1]
        elif (layerTool == 'Merge Down'):
            if (layerIndex != len(app.image.layers) - 1):
                minX = min(app.selectedLayer.x, app.image.layers[layerIndex + 1].x)
                minY = min(app.selectedLayer.y, app.image.layers[layerIndex + 1].y)
                maxX = max(app.selectedLayer.x + app.selectedLayer.image.get_width(), 
                           app.image.layers[layerIndex + 1].x + app.image.layers[layerIndex + 1].image.get_width())
                maxY = max(app.selectedLayer.y + app.selectedLayer.image.get_height(),
                           app.image.layers[layerIndex + 1].y + app.image.layers[layerIndex + 1].image.get_height())
                
                newImage = pg.Surface((maxX - minX + 1, maxY - minY + 1))
                newImage.set_alpha(255)

                newImage.blit(app.image.layers[layerIndex + 1].image, (app.image.layers[layerIndex + 1].x - minX,
                              app.image.layers[layerIndex + 1].y - minY))
                newImage.blit(app.selectedLayer.image, (app.selectedLayer.x - minX, app.selectedLayer.y - minY))

                newLayer = layers.Layer(newImage, minX, minY)
                app.image.layers.pop(layerIndex)
                app.image.layers.pop(layerIndex)
                app.image.layers.insert(layerIndex, newLayer)
                app.selectedLayer = newLayer

def openImageMouseHandler(app, mouseX, mouseY):
    imageList = os.listdir('Images')
    imageList = ['Images/' + image for image in imageList if image.split('.')[-1] in constants.VALID_FILE_TYPES]
    imageIndex = mouseY // constants.TOOL_BUTTON_HEIGHT
    if (imageIndex < len(imageList)):
        tabs.openImage(app, imageList[imageIndex])

def imageMouseHandler(app, mouseX, mouseY):
    if (app.selectedTool == 'Move Layer'):
        app.initialClickPosition = (mouseX, mouseY)
        app.initialLayerPosition = (app.selectedLayer.x, app.selectedLayer.y)
    if (app.selectedTool == 'Lasso'):
        app.lassoList = [(mouseX, mouseY)]

def imageDragHandler(app, mouseX, mouseY):
    if (app.selectedTool == 'Move Layer' and app.initialLayerPosition and app.initialClickPosition):
        app.selectedLayer.x = app.initialLayerPosition[0] - app.initialClickPosition[0] + mouseX
        app.selectedLayer.y = app.initialLayerPosition[1] - app.initialClickPosition[1] + mouseY
    if (app.selectedTool == 'Lasso'):
        app.lassoList.append((mouseX, mouseY))

def imageReleaseHandler(app, mouseX, mouseY):
    if (app.selectedTool == 'Move Layer'):
        app.initialLayerPosition = None
        app.clickPosition = None
    if (app.selectedTool == 'Lasso'):
        makeLassoLayer(app)

# The makeLassoLayer method, starts with a selection of points which surrounds
# the area that should be copied. Then those points were connected by finding
# neighbors which get each point closer to the next point in the polygon. This 
# forms the border for the polygon. Then a flood fill was used to find all of 
# the points in a rectangle surrounding the polygon which were outside of the
# polygon. Lastly, the pixels that are not in that set of pixels are copied on
# to the new layer.  

# Enumerate method: https://docs.python.org/3/library/functions.html#enumerate
# Flood Fill: https://www.geeksforgeeks.org/flood-fill-algorithm/
# Finding neigherbors: https://en.wikipedia.org/wiki/Moore_neighborhood
def makeLassoLayer(app):
    for i, element in enumerate(app.lassoList):
        x = round(element[0])
        y = round(element[1])
        x = min(x, app.image.width)
        x = max(0, x)
        y = min(y, app.image.height)
        y = max(0, y)
        app.lassoList[i] = (x, y)

    
    minX = min(x for x, y in app.lassoList) - 1
    maxX = max(x for x, y in app.lassoList) + 1
    minY = min(y for x, y in app.lassoList) - 1
    maxY = max(y for x, y in app.lassoList) + 1

    image = pg.Surface((maxX - minX + 1, maxY - minY + 1))
    image.set_alpha(255)

    def distance(point1, point2):
        return ((point2[0] - point1[0])**2) + ((point2[1] - point1[1])**2)

    boundaryPoints = set(app.lassoList)
    for i in range(len(app.lassoList)):
        start = app.lassoList[i]
        end = app.lassoList[(i + 1) % len(app.lassoList)]
        
        while (start != end):
            boundaryPoints.add(start)
            neighbors = [(start[0] - 1, start[1] - 1), (start[0], start[1] - 1), (start[0] + 1, start[1] - 1), 
                          (start[0] - 1, start[1]), (start[0] + 1, start[1]), (start[0] - 1, start[1] + 1),
                          (start[0], start[1] + 1), (start[0] + 1, start[1] + 1)]
            start = min(neighbors, key = lambda point: distance(point, end))

    exteriorPoints = set()
    queue = [(minX, minY)]

    while(queue):
        x, y = queue.pop()
        if ((x,y) in exteriorPoints or x < minX or x > maxX or  y < minY or y > maxY 
            or (x, y) in boundaryPoints):
            continue
        exteriorPoints.add((x, y))
        queue.extend([(x, y-1), (x+1, y), (x, y+1), (x-1, y)])

    for x in range(max(0, minX), min(app.image.width, maxX)):
        for y in range(max(0, minY), min(app.image.height, maxY)):
            if ((x, y) not in exteriorPoints):
                image.set_at((x - minX, y - minY), app.selectedLayer.image.get_at((x, y)))

    newLayer = layers.Layer(image, minX, minY)
    app.image.layers.insert(0, newLayer)
    app.selectedLayer = newLayer