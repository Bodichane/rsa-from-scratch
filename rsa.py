from math import ceil, sqrt
from random import getrandbits

def isPrimeNumber(num):
    root = ceil(sqrt(num)) 
    res = False

    if(num == 1):
        return False
    elif(num == 2):
        return True
    else:
        for iter in range(2, root + 1): 
            if(num % iter == 0):
                res = False
                break
            else:
                res = True
        return res
 
def generePrime(bits):
    while True:
        num = getrandbits(bits)

        if(isPrimeNumber(num)):
            return num 
    
def pgcd(a, b):
    if(b == 0):
        return a
    else:
        return pgcd(b, a % b)

def inverseModulaire(e, phi):
    r_prec, r_act = e, phi
    x_prec, x_act = 1, 0
    y_prec, y_act = 0, 1

    while r_act != 0:
        quotient = r_prec // r_act
        r_prec, r_act = r_act, r_prec - quotient * r_act
        x_prec, x_act = x_act, x_prec - quotient * x_act
        y_prec, y_act = y_act, y_prec - quotient * y_act

        return  x_prec % phi
    
def genereKeys(bits=16, e = 65537):
    while True:
        p = generePrime(bits)
        q = generePrime(bits)

        if( p != q):
            n = p * q
            phi = (p - 1) * (q - 1)

        if(pgcd(e, phi) == 1):
            d = inverseModulaire(e, phi)
            return { 'public': (e, n),
                     'private': (d, n),
                     'p': p,
                     'q': q,
                     'phi': phi}
        
def cipher(message, public_key):
    return pow(message, public_key[0], public_key[1])

def decipher(cipher_message, private_key):
    return pow(cipher_message, private_key[0], private_key[1])


key = genereKeys()
m = 42
c = cipher(m, key['public'])
d = decipher(c, key['private'])
print(f"Original: {m} -> Ciphered : {c} -> Decipher : {d}")