__author__ = 'marco.crotta'
import hashlib
import class_nautilus


###########################################################
# Class: swallow
# this is the coupling of two nautilus
###########################################################


class swallow(object):
    # A Swallow is the combination of two nautilus object
    # The swallow manipulates the nautilus, get rands from them
    # and uses only part of that data to compose new rands

    def __init__(self, seed, levels):
        # derive two new seeds (passwords) from the given one
        self.seed_right = ""
        self.seed_left = ""
        self.split_seed(seed)

        # two nautilus are needed
        self.nautilus_right = class_nautilus.nautilus(self.seed_right, levels)
        self.nautilus_left = class_nautilus.nautilus(self.seed_left, levels)

        # store local values for reading blocks or bytes
        self.value = 0
        self.bytereadpos = 0

    # Functions ############################################################

    # derive two new seeds (passwords) from the given one
    def split_seed(self, seed):
        self.seed_right = hashlib.sha512(seed).hexdigest()
        self.seed_left = hashlib.sha512(self.seed_right+seed).hexdigest()


    def spin(self):
        #reset byte pointer since this block will get new values
        self.bytereadpos = 0
        self.nautilus_right.spin()
        self.nautilus_left.spin()

    # Reads the resulting value of the cogs in the swallow
    def readval(self):
        R = self.nautilus_right.readval();
        L = self.nautilus_left.readval();
        # make a mask so to extract only 64 less significant bits of each nautilus result
        mask = ((2 ** 64) - 1)
        R = R & mask
        L = L & mask
        # value is the concat of the two 64bit from each nautilus
        self.value = (L << 64) + R
        return long(self.value)

    # Reads the resulting value of the cogs in the swallow in hex form
    def readvalhex(self):
        V = self.readval()
        return hex(V)[2:-1].zfill(32).upper()

    # Reads the resulting value of the cogs in the swallow in binary form
    def readvalbin(self):
        V = self.readval()
        return bin(V)[2:].zfill(128)

    # Reads a single (next) byte from the value.
    # Spins the swallow if needed
    def readbyte(self):
        if (self.bytereadpos >= (128 / 8)):
            self.spin()
            self.readval()
        hexx = hex(self.value)[2:-1].zfill(32).upper()
        byte = 255 << (self.bytereadpos * 8)
        B = (self.value & byte) >> (self.bytereadpos * 8)
        self.bytereadpos += 1
        return B

    def readbytehex(self):
        B = self.readbyte()
        return hex(B)[2:-1].zfill(2).upper()
