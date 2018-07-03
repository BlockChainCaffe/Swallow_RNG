__author__ = 'marco.crotta'
import hashlib


###########################################################
# Class: nautilus
# this is one of the two parts of a swallow system
###########################################################


class nautilus(object):
    # In order to have a nautilus we need to have a starting seed
    # to intialize the cogs... and a number of cogs
    def __init__(self, seed, levels):

        # Vars
        # List of primes to be used as random cog steps
        primes =  [1,2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127]

        self.cogs = []              # array of long-int (the cogs)
        self.cogs_count = levels    # number of cogs in this nautilus
        self.cogs_maxpos = 128      # MD5 hash is 128 bit long
        self.cogs_pos = []          # position (0-127) of each cog
        self.cogs_hop = []          # (prime) number of bits each cog jumps each time

        # Initialize nautilus setting values for each cog and zeroing positions
        # md5(...(md5(sedd)) of seed are used as initial value of each cog
        # At each step seed is appended to avoid a predictable map md5(x) <-> md5(md5(x))
        rot = seed
        hop = 1

        for n in range(0, self.cogs_count):
            rot = hashlib.md5(rot+seed).hexdigest()
            self.cogs.append(long(rot, 16))
            self.cogs_pos.append(0)
            # Try to make random assignments of hops values for each cog
            # hop values are primes, so that all positions of the cog are used in turn
            seedmask=long(hashlib.md5(rot).hexdigest(),16)
            while (seedmask & hop) == 0:
                hop +=1
                seedmask = (seedmask >> 1)
            self.cogs_hop.append(primes[hop-1])
            hop +=1


    # Sping nautilus one position forward by
    # moving all needed cogs to move ONE step
    def spin(self):
        for n in range(0, self.cogs_count):
            # get mask value for 'n' left-most bits where n
            # is the prime hop number for this cog
            leftmost = (((2**self.cogs_hop[n])-1) << (128-self.cogs_hop[n]))
            # spin cog 'leftmost' one position left
            rem = self.cogs[n] & leftmost
            self.cogs[n] -= rem
            self.cogs[n] = self.cogs[n] << self.cogs_hop[n]
            rem = rem >> (128 - self.cogs_hop[n])
            self.cogs[n] = self.cogs[n] + rem
            # trak new position
            self.cogs_pos[n] += 1
            # spin next cog?
            if self.cogs_pos[n] < 128:
                # nope, exit for loop
                break
            else:
                # yes, set this pos to 0 and continue to next cog
                self.cogs_pos[n] = 0


    # prints out all values of the cogs of the nautilus in binary form
    def dumpbin(self):
        print self.cogs_hop
        for n in range(0, self.cogs_count):
            print n, ': ', bin(self.cogs[n])[2:].zfill(128)

    # Prints out all values of the cogs of the nautilus in hex form
    def dumphex(self):
        for n in range(0, self.cogs_count):
            print n, ': ', hex(self.cogs[n])[2:-1].zfill(32).upper()

    # Reads the resulting value of the cogs in the nautilus
    def readval(self):
        A = 0L
        for n in range(0, self.cogs_count):
            A ^= self.cogs[n]
        return A

    # Reads the resulting value of the cogs in the nautilus in binary form
    def readvalbin(self):
        A = self.readval()
        return bin(A)[2:].zfill(128)
