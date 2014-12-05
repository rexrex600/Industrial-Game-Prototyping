#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      L11JoDav
#
# Created:     02/12/2014
# Copyright:   (c) L11JoDav 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import random, math

class perlin_map:

    def __init__(self, size, frequency):
        #map size
        self.size = size
        self.frequency = float(frequency)


        #Pseudorandomisation and Direction Map
        self.pseudorand = list(range(256))
        random.shuffle(self.pseudorand)
        self.pseudorand += self.pseudorand
        self.dirs = [(math.cos(a * 2.0 * math.pi / 256),
                      math.sin(a * 2.0 * math.pi / 256))
                      for a in range(256)]


    def noise(self, x, y, per):
        def surflet(gridX, gridY):
            distX, distY = abs(x-gridX), abs(y-gridY)
            polyX = 1 - 6 * distX ** 5 + 15 * distX ** 4 + 10 * distX ** 3
            polyY = 1 - 6 * distY ** 5 + 15 * distY ** 4 + 10 * distY ** 3
            hashed = self.pseudorand[self.pseudorand[int(gridX)%per] + int(gridY%per)]
            grad = (x-gridX)*self.dirs[hashed][0] + (y-gridY)*self.dirs[hashed][1]
            return polyX * polyY * grad
        intX, intY = int(x), int(y)
        return (surflet(intX+0, intY+0) + surflet(intX+1, intY+0) +
                surflet(intX+0, intY+1) + surflet(intX+1, intY+1))


    def fBm(self, x, y, per, octs, perm, dirs):
        val = 0
        for o in range(octs):
            val += 0.5**o * self.noise(x*2**o, y*2**o, per*2**o)
        return val


    def gen_noise_map(self):
        size, freq, octs, data = self.size, 1/self.frequency, 5, []
        for y in range(size):
            for x in range(size):
                data.append(abs(int(self.fBm(x*freq, y*freq, int(size*freq), octs, self.pseudorand, self.dirs))))
        return data

x = perlin_map(64, 16)

print(x.gen_noise_map())