#!/usr/bin/python
## Primi esercizi sulle hash

import hashlib
import sys

#############################
# Prendiamo l'input (password)

input = sys.argv[1]
print input


def top_read (top):
	A=0L
	for n in range(0,len(top)):
		A ^= top[n]
	return A
			


#############################
# Creiamo la prima trottola

rot = input
top1 = []
for n in range(0,8):
	rot =  hashlib.md5(rot).hexdigest()
	top1.append(long(rot,16))

for n in range (0,8):
	print n,': ',top1[n]

#############################
# Creiamo la seconda trottola

rot = hashlib.sha1(input).hexdigest()
top2 = []
for n in range(0,8):
        rot =   hashlib.md5(rot).hexdigest()
        top2.append(long(rot,16))

for n in range (0,8):
        print n,': ',top2[n]


T1=top_read(top1)
T2=top_read(top2)

print T1," - ",T2
print T1^T2


