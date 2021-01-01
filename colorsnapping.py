from PIL import Image
from collections import Counter
import math

COLOR_DICT = {(255,51,51):'Red', (255,128,0):'Orange', (255,255,0):'Yellow', (0,255,0):'Green',(0,128,255):'Light Blue', (0,255,255):'Dark Blue', (127,0,255):'Purple',(255,0,255):'Magenta', (255,51,153):'Pink', (128,128,128):'Gray', (0,0,0):'Black', (255,255,255):'White'}

#Python version of the low-cost approximation formula of color distance from this website: https://www.compuphase.com/cmetric.htm
def get_color_distance(c1:(int), c2:(int))-> float:
    rmean = (c1[0] + c2[0]) / 2
    r = c1[0] - c2[0]
    g = c1[1] - c2[1]
    b = c1[2] - c2[2]
    return math.sqrt((2+rmean/256)*r*r + 4*g*g + (2+(255-rmean)/256)*b*b)

def color_snap(pixel:(int)) -> (int):
    global COLOR_DICT
    sDist = 10000000
    cColor = -1
    for color in COLOR_DICT.keys():
        dist = get_color_distance(color, pixel)
        if dist < sDist:
            sDist = dist
            cColor = color
    return COLOR_DICT[cColor]

def run():
    tests = ['test1.png', 'test2.png', 'test3.png', 'test4.png', 'test5.png', 'test6.png', 'test7.png', 'red.jpg']
    for test in tests:
        print(test)
        count = Counter()
        im = Image.open(test, 'r')
        pix_val = list(im.getdata())
        for val in pix_val:
            if len(val) == 3:
                count[color_snap(val)] += 1
            elif val[3] == 255:
                count[color_snap(val)] += 1
        if len(count.keys()) >= 5:
            top2 = count.most_common(5)
            print(top2[2][0] +  ', ' + top2[3][0] + ', ' + top2[4][0])
        else:
            print(count)

if __name__ == '__main__':
    run()