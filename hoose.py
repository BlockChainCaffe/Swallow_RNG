#!/usr/bin/python3

#
# The Hoose
# a test on hashes, PRNG and encryption
#


import hashlib
import sys, os
import argparse



####################################################################################################
###
###    Globals

Args = {}               # Parameters received from command line argiments



####################################################################################################
###
###    Functions
###


def parseArguments():
    global Args
    parser = argparse.ArgumentParser("the hoose might like some input")
    parser.add_argument("key", help="use this as encryption key/seed", type=str)
    parser.add_argument("plain", help="file to be encrypted", type=str, default=False, nargs='?')
    parser.add_argument("-o", "--output", help="write here", dest="output", type=str, required=False, default=False)
    parser.add_argument("-x", "--hex", help="output hex to stdout", dest="hex", action='store_const', const=True, default=False)
    parser.add_argument("-r", "--rounds", help="how many rounds to run", dest="rounds", type=int, required=False, default=0)
    parser.add_argument("-s", "--size", help="output size in bytes", dest="bytes", type=int, required=False, default=0)
    Args = parser.parse_args()

    ## Option 1 : encrypt/decrypt a file
    if Args.plain != False:
        if Args.output or Args.hex or Args.rounds or Args.bytes:
            print("you either generate or encrypt, pick your options accordingly")
            exit()
        if not os.path.isfile(Args.plain) or not os.access(Args.plain, os.R_OK):
            print("cannot access cleartext file", Args.plain)
            exit()
    ## Option 2 : generate some noise
    else:
        if Args.output and Args.hex :
            print("can't send output to file or stdout not booth, use tee for that")
            exit()
        if not (Args.output or Args.hex):
            print("you must have either output or hex")
            exit()

        if Args.rounds and Args.bytes :
            print("can't send both rounds and size")
            exit()
        if not (Args.rounds ^ Args.bytes) :
            print("you must have either rounds or size", Args.rounds ^ Args.bytes)
            exit()


def Generate():
    global Args
    h = hashlib.sha256(bytes(Args.key, 'utf-8')).digest()
    if Args.rounds:
        rounds = Args.rounds
        reminder = 0
    else:
        rounds = (Args.bytes // hashlib.sha256().digest_size)
        reminder = (Args.bytes % hashlib.sha256().digest_size)

    if Args.output:
        outputfile = open(Args.output,'wb')
    else:
        outputfile = sys.stdout

    while (rounds>0):
        h1 = h + bytes(Args.key, 'utf-8')
        h = hashlib.sha256(h1).digest()
        if Args.output:
            outputfile.write(h)
        else:
            outputfile.write(h.hex())
        rounds=rounds-1

    if (reminder > 0):
        h1 = h + bytes(Args.key, 'utf-8')
        h = hashlib.sha256(h1).digest()[:reminder]
        if Args.output:
            outputfile.write(h)
        else:
            outputfile.write(h.hex())

    outputfile.close()


def Operate():
    global Args

    outputfile = open(Args.plain+'.hoo','wb')
    h = hashlib.sha256(bytes(Args.key, 'utf-8')).digest()

    with open(Args.plain, 'rb') as plain:
        while(True) :
            h1 = h + bytes(Args.key, 'utf-8')
            h = hashlib.sha256(h1).digest()
            data = plain.read(hashlib.sha256().digest_size)
            
            h = h[:len(data)]
            enc = bytes([_a ^ _b for _a, _b in zip(h, data)])
            outputfile.write(enc)

            if len(data) < hashlib.sha256().digest_size:
                break
    outputfile.close()

def main():
    global Args

    if Args.plain:
        Operate()
    elif Args.hex or Args.output:
        Generate()


####################################################################################################
###
###    START
###


if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

if __name__ == "__main__": 
    # What does the user want?
    parseArguments()

main()

