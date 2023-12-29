# For citations for RGB to HSV conversion and vice versa, see citations.txt

# RGB to HSV Coversion: https://www.rapidtables.com/convert/color/rgb-to-hsv.html
def getHSVValues(r,g,b):
    r_adjusted = r/255
    g_adjusted = g/255
    b_adjusted = b/255

    C_max = max(r_adjusted, g_adjusted, b_adjusted)
    C_min = min(r_adjusted, g_adjusted, b_adjusted)
    change = C_max - C_min

    if (change == 0):
        hue = 0
    elif (C_max == r_adjusted):
        hue = 60 * (((g_adjusted - b_adjusted)/change) % 6)
    elif (C_max == g_adjusted):
        hue = 60 * (((b_adjusted - r_adjusted)/change) + 2)
    elif (C_max == b_adjusted):
        hue = 60 * (((r_adjusted - g_adjusted)/change) + 4)

    if (C_max == 0):
        saturation = 0
    else:
        saturation = change / C_max

    value = C_max

    return hue, saturation, value

# RGB to HSV Coversion: https://www.rapidtables.com/convert/color/rgb-to-hsv.html
def getRGBValues(hue, saturation, value):
    C = value * saturation
    X = C * (1- abs(((hue/60) % 2) - 1))
    m = value - C

    if (0 <= hue <= 60):
        r_adjusted, g_adjusted, b_adjusted = C, X, 0
    elif (60 <= hue <= 120):
        r_adjusted, g_adjusted, b_adjusted = X, C, 0
    elif (120 <= hue <= 180):
        r_adjusted, g_adjusted, b_adjusted = 0, C, X
    elif (180 <= hue <= 240):
        r_adjusted, g_adjusted, b_adjusted = 0, X, C
    elif (240 <= hue <= 300):
        r_adjusted, g_adjusted, b_adjusted = X, 0, C
    elif (300 <= hue <= 360):
        r_adjusted, g_adjusted, b_adjusted = C, 0, X

    r, g, b =  ((r_adjusted + m) * 255, (g_adjusted + m) * 255, (b_adjusted + m) * 255)
   
    return r, g, b