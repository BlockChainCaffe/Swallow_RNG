# Swallow RNG

Swallow (meaning the bird) is a pseudo RNG written in python for educatinal and test purpouses only.
The underlying idea is to use random data geneated by swallow to crypt data using a simple xor function, thus using simmecric algorithm.

The RNG is tought to resist a known-plaintext attack, so to make it unpractical or impossible to derive the seed/password even if code, plaintext, and cyphertext are provided. Hash functions are heavilly used all orver, still the code tryes to be resist an attacker with a full rainbow table available, that can revert hash functions.

# Please note:

Swallow is not tested nor guaranted to fit any specific purpouses. Althought it was written with cryptographyc applications in mind, no assumption can be made on it's performace, trutablity etc.
