import math
import random

def isPrimeNumber(num):
    racine = math.ceil(math.sqrt(num)) 
    res = False

    if(num == 1):
        return False
    elif(num == 2):
        return True
    else:
        for iter in range(2, racine + 1): 
            if(num % iter == 0):
                res = False
                break
            else:
                res = True
        return res


def generePrime(bits):
    while True:
        num = random.getrandbits(bits)

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
    else:
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


def attackSmallE(c):
    return int(round(c ** (1/3)))


def euclideEtendu(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = euclideEtendu(b, a % b)
    return g, y, x - (a // b) * y


def attackCommonModulus(c1, c2, e1, e2, n):
    g, a, b = euclideEtendu(e1, e2)

    if(a < 0):
        part1 = pow(inverseModulaire(c1, n), -a, n)
    else:
        part1 = pow(c1, a, n)

    if(b < 0):
        part2 = pow(inverseModulaire(c2, n), -b, n)
    else:
        part2 = pow(c2, b, n) 
    
    return part1 * part2 % n


message = 42
e1, e2 = 65537, 17
key = genereKeys(16, e1)
c1 = cipher(message, (e1, key['public'][1]))
c2 = cipher(message, (e2, key['public'][1]))
m = attackCommonModulus(c1, c2, e1, e2, key['public'][1])
print(f"Message trouve: {m}")


'''
key = genereKeys(16, e=3)
message = 285
private_key = attackSmallE
c = cipher(message, key['public'])
m = attackSmallE(c)
print(f"Original: {message} -> Ciphered: {c} -> Deciphered: {m}")
'''