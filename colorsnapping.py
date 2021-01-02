from PIL import Image
from collections import Counter
import math

COLOR_DICT = {(255,51,51):'Red', (255,128,0):'Orange', (255,255,0):'Yellow', (0,255,0):'Green',(0,128,255):'Light Blue',
              (0,255,255):'Dark Blue', (127,0,255):'Purple',(255,0,255):'Magenta', (255,51,153):'Pink', (128,128,128):'Gray',
              (0,0,0):'Black', (255,255,255):'White'}

COLOR_DICT_V2 = {(0,0,0):'Black',(255,255,255):'White',(255,0,0):'Red',(0,255,0):'Light Green',(0,0,255):'Blue',(255,255,0):'Yellow',
                 (255,215,0):'Gold',(0,255,255):'Light Blue',(255,140,0):'Orange',(255,0,255):'Magenta',(75,0,130):'Indigo',
                 (191,191,191):'Silver',(128,128,128):'Gray',(128,0,0):'Dark Red',(0,128,0):'Green',
                 (220,202,152):'Tan',(128,0,128):'Purple',(0,128,128):'Blue Green',(0,0,128):'Dark Blue'}

PAIRED_COLORS = {'Black': ['Gray'], 'Gray': ['Black', 'Silver'], 'Silver': ['Gray'], 'White': ['Silver', 'Tan'],
                 'Tan': ['Yellow'], 'Yellow': ['Tan', 'Gold'], 'Gold': ['Orange', 'Yellow '], 'Orange': ['Gold', 'Red'],
                 'Red': ['Orange', 'Dark Red', 'Magenta'], 'Dark Red': ['Red '], 'Magenta': ['Red', 'Purple'],
                 'Light Green': ['Green'], 'Green': ['Light Green', 'Olive Green', 'Blue Green'], 'Olive Green': ['Green'],
                 'Blue Green': ['Green', 'Blue'], 'Light Blue': ['Blue'], 'Blue': ['Light Blue', 'Dark Blue', 'Blue Green', 'Indigo'],
                 'Dark Blue': ['Blue'], 'Indigo': ['Dark Blue', 'Blue'], 'Purple': ['Indigo', 'Magenta']}

MAIN_COLORS = {'Black': ['Black'], 'Gray': ['Gray'], 'Silver': ['White'], 'White': ['White'], 'Tan': ['Yellow'],
               'Yellow': ['Yellow'], 'Gold': ['Yellow'], 'Orange': ['Orange'], 'Red': ['Red'], 'Dark Red': ['Red'],
               'Magenta': ['Pink'], 'Light Green': ['Green'], 'Green': ['Green'], 'Olive Green': ['Dark Green'],
               'Blue Green': ['Blue'], 'Light Blue': ['Blue'], 'Blue': ['Blue'], 'Dark Blue': ['Blue'],
               'Indigo': ['Purple'], 'Purple': ['Purple']}

#Python version of the low-cost approximation formula of color distance from this website: https://www.compuphase.com/cmetric.htm
def lab_conversion(c1:(int), c2:(int))-> float:
    rmean = (c1[0] + c2[0]) / 2
    r = c1[0] - c2[0]
    g = c1[1] - c2[1]
    b = c1[2] - c2[2]
    return (2+rmean/256)*r*r + 4*g*g + (2+(255-rmean)/256)*b*b

def color_snap(pixel:(int)) -> (int):
    global COLOR_DICT_V2
    sDist = 10000000
    cColor = -1
    for color in COLOR_DICT_V2.keys():
        dist = lab_conversion(color, pixel)
        if dist < sDist:
            sDist = dist
            cColor = color
    return cColor

def collapse_counter(count:Counter) -> [()]:
    global MAIN_COLORS
    #print(count)
    nCount = Counter()
    for key in count.keys():
        value = count[key]
        for val in MAIN_COLORS[key]:
            nCount[val] += value
    return nCount.most_common(min(len(nCount.keys()),3))

def run():
    global COLOR_DICT_V2
    tests = ['1.png','2.png','3.png','4.png','5.png','6.png','7.png', '8.png', '9.png']
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
                count[COLOR_DICT_V2[c]] += 1
            elif val[3] == 255:
                c = color_snap(val)
                #Code For Producing the Image Without Black or Gray in it.
                '''
                if COLOR_DICT_V2[c] == 'Black' or COLOR_DICT_V2[c]=='Gray':
                    nList.append((0,0,0,0))
                else:
                    nList.append(c)
                '''
                nList.append(c)
                count[COLOR_DICT_V2[c]] += 1
            else:
                nList.append(val)
        percent_black = (count['Black']+count['Gray'])/ sum(count.values())
        percent_white = count['White']/sum(count.values())
        #print(percent_black, percent_white)
        if percent_black < .75 and percent_white < .1:
            count['Black'] = 0
            count['Gray'] = 0
        print(collapse_counter(count))

        #Code for Saving image

        #im2.putdata(nList)
        #im2.save('outputcd2/'+test)


if __name__ == '__main__':
    run()