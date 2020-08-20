######################################
# Name: Devon Knudsen
# Date: 17 April 2020
# Assingment: Rivets Arm His Lama Den
# Written in Python 3
######################################

from sys import stdin, stdout

# determines if a given number is prime
def isPrime(n):
    if(n % 2 == 0):
        return False
    
    for i in range(3, int(n ** 0.5 + 1), 2):
        if(n % i == 0):
            return False
        
    return True

# factors a number n into the product of two primes
def factor(n):
    for i in range(3, int(n ** 0.5 + 1), 2):
        if(n % i == 0 and isPrime(i) and isPrime(n / i)):
            return int(i), int(n / i)
    
    return None

# recursively returns the greatest common divisor of a and b
def gcd(a, b):
    if(b == 0):
        return a
    else:
        return gcd(b, a % b)
    
# generates all e's between 1 and z that are of the form 2 ** n + 1
def genEs(z):
    es = []
    for e in range(3, z + 1, 2):
        if(isPrime(e) and gcd(e, z) == 1 and isPowerOfTwoPlusOne(e)):
            es.append(e)
        
    return es

# checks if e is of the form 2 ** n + 1
# found a similar algorithm at: https://www.sanfoundry.com/python-program-find-whether-number-power-two/
def isPowerOfTwoPlusOne(e):
    possiblePowerOf2 = e - 1
    if(possiblePowerOf2 <= 0):
        return False
    elif(possiblePowerOf2 & (possiblePowerOf2 - 1) == 0):
        return True

# naively calculates the inverse modulo of e and z
def naiveInverse(e, z):
    for d in range(0, z):
        if((e * d) % z == 1):
            return d
    
    return None

# decrypts a ciphertext C with a private key K_priv
def decrypt(C, K_priv):
    return (C ** K_priv[0]) % K_priv[1]

# MAIN
# read in given n and cipher text
cipherTxt = stdin.read().rstrip("\n").split("\n")

# assign given n to variable n and ciphered text to variable C
n = eval(cipherTxt[0])
C = cipherTxt[1].split(",")

# calculate two prime factors of n
p, q = factor(n)

# calculate z
z = int(((p - 1)*(q - 1))/gcd(p - 1, q - 1))

print("p={}\tq={}".format(p, q))
print("n={}".format(n))
print("z={}".format(z))

# generate list of all possible e's
es = genEs(z)

# attempt decrypting the cipher text using each e in the list of e's 
for e in es:
    
    # calculate d (inverse modulo)
    d = naiveInverse(e, z)
    
    # set potential public and private keys
    K_pub = (e, n)
    K_priv = (d, n)
    
    print("--")
    print("Public key: {}".format(K_pub))
    print("Private key: {}".format(K_priv))
    
    # attempt to build decrypted string
    M = ""
    printSpace = True
    for char in C:
        m = decrypt(int(char), K_priv)
        # if char is outside of printable ascii characater range, invalid plaintext
        if(not(32 <= m <= 127) and not(chr(m) == "\n")):
            print("ERROR: invalid plaintext.")
            printSpace = False
            break
        
        # if within range printable ascii characater range, build string and write to screen
        M += chr(m)
        stdout.write(chr(m))
        stdout.flush()
        
    if(printSpace):
        print()

