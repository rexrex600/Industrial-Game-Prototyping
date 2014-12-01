#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rexrex600
#
# Created:     27/11/2014
# Copyright:   (c) rexrex600 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import random
import math
from PIL import Image
import multiprocessing
import time

img_size = 256

def randomize():
    perm = range(256)
    random.shuffle(perm)
    perm += perm
    random.shuffle(perm)
    order = range(256)
    random.shuffle(order)
    dirs = [(math.cos(a * 2.0 * math.pi / 256),
    		 math.sin(a * 2.0 * math.pi / 256))
    		 for a in order]
    return perm, dirs

def noise(x, y, per, perm, dirs):
    def surflet(gridX, gridY):
        distX, distY = abs(x-gridX), abs(y-gridY)
        polyX = 1 - 6*distX**5 + 15*distX**4 - 10*distX**3
        polyY = 1 - 6*distY**5 + 15*distY**4 - 10*distY**3
        hashed = perm[perm[int(gridX)%per] + int(gridY)%per]
        grad = (x-gridX)*dirs[hashed][0] + (y-gridY)*dirs[hashed][1]
        return polyX * polyY * grad
    intX, intY = int(x), int(y)
    return (surflet(intX+0, intY+0) + surflet(intX+1, intY+0) +
            surflet(intX+0, intY+1) + surflet(intX+1, intY+1))

def fBm(x, y, per, octs, perm, dirs):
    val = 0
    for o in range(octs):
        val += 0.5**o * noise(x*2**o, y*2**o, per*2**o, perm, dirs)
    return val

def tile_gen(frequency):
    perm, dirs = randomize()
    frequency = float(frequency)
    size, freq, octs, data = img_size, 1/frequency, 5, []
    for y in range(size):
        for x in range(size):
            data.append(fBm(x*freq, y*freq, int(size*freq), octs, perm, dirs))
    return data



def gen_tile(tile_no):                                                      #My hackery from here
    frequency = 100
    size = img_size

    
    hdata = tile_gen(frequency)
    fdata = tile_gen(frequency)

    hmap = Image.new("L", (size, size))
    hmap.putdata(hdata, 128, 128)
    hmap.save("HMap%d.png"%tile_no)

    fmap = Image.new("L", (size,size))
    fmap.putdata(fdata, 128, 128)
    fmap.save("FMap%d.png"%tile_no)


    
    cmap = Image.new("RGB", (size, size))
    cdata = list(hmap.getdata())

    fdata1 = list(fmap.getdata())

    
    a = 0
    for i in cdata:
        if i < 110:
            cdata[a]=((0,int(i), 255,))
        elif i >= 180:
            cdata[a]=((int(i),int(i),int(i),))
        elif i >= 110 and i < 115:
            cdata[a]=((255,255,0,))
        else:
            fo = fdata1[a] / 2
            if fo <= 63:
                cdata[a] =((0,i,0))
            else:
                cdata[a] = ((0,fo,0))
        hdata[a] = 0
        a += 1

    for i in cdata:
        try:
            type(i) == tuple
        except:
            print i
    print cmap.size, len(cdata)    
    cmap.putdata(cdata, 128, 128)
    cmap.save("Tile%dcoloured.png"%tile_no)


start = time.time()

if __name__ == '__main__':
    active_process_list = multiprocessing.Queue()
    pool = multiprocessing.Pool(processes=10)
    pool.map(gen_tile,range(3))
    pool.close()
    pool.join()


##for i in range(1):
##    gen_tile(i)


end = time.time()

print end - start
