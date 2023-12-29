from cmu_cs3_graphics import *
import cmu_graphics.libs.pygame_loader as pg

lightTheme = {
    'tabColor': rgb(240, 240, 240),
    'tabBarColor': rgb(229, 229, 229),
    'leftToolBarColor': rgb(244, 244, 244),
    'rightToolBarColor': rgb(244, 244, 244),
    'layersListColor': rgb(210, 210, 210),
    'border': rgb(0,0,0),
    'imageBackground': rgb(225, 225, 225),
    'selectedBorder': rgb(255, 238, 3),
    'fontColor': rgb(0, 0, 0),
    'buttonColor': rgb(200, 200, 200),
    'buttonFontColor': rgb(0, 0, 0)
}

darkTheme = {
    'tabColor': rgb(90, 90, 90),
    'tabBarColor': rgb(75, 75, 75),
    'leftToolBarColor': rgb(60, 60, 60),
    'rightToolBarColor': rgb(60, 60, 60),
    'layersListColor': rgb(50, 50, 50),
    'border': rgb(0,0,0),
    'imageBackground': rgb(40, 40, 40),
    'selectedBorder': rgb(255, 238, 3),
    'fontColor': rgb(255, 255, 255),
    'buttonColor': rgb(200, 200, 200),
    'buttonFontColor': rgb(0, 0, 0)
}

# Looked at the RGB class in the shape_logic.py file.
def convertCMUToPG(CMUColor):
    return pg.Color(CMUColor.red, CMUColor.green, CMUColor.blue)