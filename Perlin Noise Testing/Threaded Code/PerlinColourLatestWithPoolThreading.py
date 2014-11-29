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
    dirs = [(math.cos(a * 2.0 * math.pi / 256),
    		 math.sin(a * 2.0 * math.pi / 256))
    		 for a in range(256)]
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
    data = tile_gen(frequency)
    size = img_size

    #forest_data = tile_gen(frequency)

    im = Image.new("L", (size, size))
    im.putdata(data, 128, 128)
    im.save("Tile%d.png"%tile_no)
    im1 = Image.new("RGB", (size, size))
    data1 = []
    del data[:]
    data = list(im.getdata())
    for i in data:
        if i < 110:
            data1.append((0,int(i), 255))
        elif i >= 180:
            data1.append((int(i),int(i),int(i)))
        elif i >= 110 and i < 115:
            data1.append((255,255,0))
        else:
            a = random.randint(0,2)
            if a == 0:
                data1.append((0,int(i/2),0))
            else:
                data1.append((0,int(i),0))
    im1.putdata(data1, 128, 128)
    im1.save("Tileb%dcoloured.png"%tile_no)


start = time.time()

if __name__ == '__main__':
    active_process_list = multiprocessing.Queue()
    pool = multiprocessing.Pool(processes=10)
    pool.map(gen_tile,range(100))
    pool.close()
    pool.join()


##for i in range(1):
##    gen_tile(i)


end = time.time()

print end - start
