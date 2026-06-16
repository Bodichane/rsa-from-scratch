import math
import random
import os

def isPrimeNumber(num):
    root = math.ceil(math.sqrt(num)) 
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


def addPadding(message, n):
    message_size = (message.bit_length() + 7) // 8
    message_bytes = message.to_bytes(message_size, 'big')
    n_size = (n.bit_length() + 7) // 8
    n_padding = n_size - len(message_bytes) - 4
    random_bytes = b''
    while len(random_bytes) < n_padding:
        b = os.urandom(1)
        if(b != b'\x00'):
            random_bytes += b

    padded_bytes = b'\x00\x02' + random_bytes + b'\x00' + message_bytes
    return int.from_bytes(padded_bytes, 'big')

def removingPadding(padded_int, n):
    padded_size = (n.bit_length() + 7) // 8
    padded_bytes = padded_int.to_bytes(padded_size, 'big')

    if(padded_bytes[0] == 0x00 and padded_bytes[1] == 0x02):
        separate = padded_bytes.index(b'\x00', 2)
        if(separate >= 2):
            message_bytes = padded_bytes[separate + 1:]
            return int.from_bytes(message_bytes, 'big')


def oracle(c, private_key):
    n = private_key[1]
    decrypted = decipher(c, private_key)
    padded_bytes = decrypted.to_bytes((n.bit_length() + 7) // 8, 'big')
    return padded_bytes[0] == 0x00 and padded_bytes[1] == 0x02


def find(c, e, n, private_key):
    s = 2
    while True:
        c_ = c * pow(s, e, n) % n

        if(oracle(c_, private_key)):
            return s
        else:
            s += 1


key = genereKeys()
padded = addPadding(42, key['private'][1])
c = cipher(padded, key['public'])
s = find(c, key['public'][0], key['public'][1], key['private'])
print(f"first valid s : {s}")


'''
key = genereKeys()
message = 42

# Cipher with padding
padded = addPadding(42, key['public'][1])
c = cipher(padded, key['public'])

# Decipher with removal padding
decipher_padded = decipher(c, key['private'])
m = removingPadding(decipher_padded, key['public'][1])

print(f"Original: {message} -> Ciphered: {c} -> Deciphired: {m}")
'''

'''
message = 42
e1, e2 = 65537, 17
key = genereKeys(16, e1)
c1 = cipher(message, (e1, key['public'][1]))
c2 = cipher(message, (e2, key['public'][1]))
m = attackCommonModulus(c1, c2, e1, e2, key['public'][1])
print(f"Message find: {m}")
'''

'''
key = genereKeys(16, e=3)
message = 285
private_key = attackSmallE
c = cipher(message, key['public'])
m = attackSmallE(c)
print(f"Original: {message} -> Ciphered: {c} -> Deciphered: {m}")
'''