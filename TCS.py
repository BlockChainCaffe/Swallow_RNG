import sys
import binascii
import class_swallow

'''
Generates a bunch of random bytes with the nautilus RNG and writes them to
a binary file for test purpouses)
'''

#passw1 = sys.argv[1]
passw1="input5"
sw=class_swallow.swallow(passw1,3)

f = open('random','wb')

sw.spin()
print sw.readvalhex ()
while 1 :
    f.write(binascii.a2b_hex(sw.readbytehex()))
f.close()
