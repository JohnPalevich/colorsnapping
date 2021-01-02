from PIL import Image
from collections import Counter
import math

COLOR_DICT = {(255,51,51):'Red', (255,128,0):'Orange', (255,255,0):'Yellow', (0,255,0):'Green',(0,128,255):'Light Blue', (0,255,255):'Dark Blue', (127,0,255):'Purple',(255,0,255):'Magenta', (255,51,153):'Pink', (128,128,128):'Gray', (0,0,0):'Black', (255,255,255):'White'}
COLOR_DICT_V2 = {(0,0,0):'Black',(255,255,255):'White',(255,0,0):'Red',(0,255,0):'Lime',(0,0,255):'Blue',(255,255,0):'Yellow',(0,255,255):'Cyan',(255,0,255):'Magenta',(191,191,191):'Silver',(128,128,128):'Gray',(128,0,0):'Maroon',(128,128,0):'Olive',(0,128,0):'Green',(128,0,128):'Purple',(0,128,128):'Teal',(0,0,128):'Navy'}

#Python version of the low-cost approximation formula of color distance from this website: https://www.compuphase.com/cmetric.htm
def lab_conversion(c1:(int), c2:(int))-> float:
    rmean = (c1[0] + c2[0]) / 2
    r = c1[0] - c2[0]
    g = c1[1] - c2[1]
    b = c1[2] - c2[2]
    return math.sqrt((2+rmean/256)*r*r + 4*g*g + (2+(255-rmean)/256)*b*b)

#def hsl_conversion(c1:(int), c2:(int)) -> float:


def color_snap(pixel:(int)) -> (int):
    global COLOR_DICT
    sDist = 10000000
    cColor = -1
    for color in COLOR_DICT.keys():
        dist = lab_conversion(color, pixel)
        if dist < sDist:
            sDist = dist
            cColor = color
    return cColor

def run():
    global COLOR_DICT
    tests = ['1.png','2.png','3.png','4.png','5.png','6.png','7.png']
    for test in tests:
        print(test)
        count = Counter()
        im = Image.open('testimages/' + test, 'r')
        pix_val = list(im.getdata())
        im2 = Image.new(im.mode, im.size)
        nList = []
        for val in pix_val:
            if len(val) == 3:
                c = color_snap(val)
                nList.append(c)
                count[COLOR_DICT[c]] += 1
            elif val[3] == 255:
                c = color_snap(val)
                nList.append(c)
                count[COLOR_DICT[c]] += 1
            else:
                nList.append(val)
        print(count)
        im2.putdata(nList)
        im2.save('outputcd1/'+test)

if __name__ == '__main__':
    run()