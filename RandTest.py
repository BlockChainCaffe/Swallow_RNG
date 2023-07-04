import sys
import math
import struct

'''
Simple test for the randomness of a BINARY file.
Reads a file named "random" in binary mode. Read bytes, does some stats
- byte value that apperars less time
- byte value that appears more ofthen
- entropy
- all the values
'''

## List of values : position N ->number of times N is present in the file
values = [0]*256

min=0
max=0
tot=0

f = open('random','rb')
while 1==1 :
    n = f.read(1)
    print(">",n)
    if ( len(n) != 1 ):
        break
    i = struct.unpack('B',n)[0]
    values[i] += 1
    if ( max < values[i]):
        max = values[i]
    tot=tot+1
f.close()

## Find min
min=max
for i in range (0,256):
    if (values[i] < min):
        min = values[i]

# Results
print("----")
print('Value ', values.index(max), 'appeared', max, 'times')
print('Value ', values.index(min), 'appeared', min, 'times')

ent = 0.0
for v in values:
    if v > 0:
        freq = float(v) / tot
        ent = ent + freq * math.log(freq, 2)
ent = -ent
print('Entropy ', ent,'/8')

print
print(values)
