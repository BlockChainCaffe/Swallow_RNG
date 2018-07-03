import random
import struct


values = [0]*256
for a in range(0,256):
    values[a]=a

f = open('random','wb')
for a in range(0,40000):
    random.shuffle(values)
    for i in range(0,256):
        B=struct.pack('B',values[i])
        f.write (B)
