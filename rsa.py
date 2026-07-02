from math import ceil, sqrt
from random import getrandbits, randrange

def miller_rabin(num, k=40):
    """
    Test de primalité de Miller-Rabin.
    k est le nombre de rounds de vérification (40 rounds = certitude quasi absolue).
    """
    if num == 2 or num == 3:
        return True
    if num <= 1 or num % 2 == 0:
        return False

    d = num - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = randrange(2, num - 1)
        x = pow(a, d, num)  

        if x == 1 or x == num - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                break
        else:
            return False  

    return True  
 
def generePrime(bits):
    """
    Génère un nombre premier aléatoire de la taille spécifiée en bits.
    Utilise Miller-Rabin pour valider la primalité de manière efficace.
    """
    while True:
        num = getrandbits(bits) | 1
        num |= (1 << (bits - 1))
        
        if miller_rabin(num):
            return num 
    
def pgcd(a, b):
    """
    Calcule le Plus Grand Commun Diviseur (PGCD) de deux nombres.
    Version itérative (algorithme d'Euclide) pour éviter l'erreur RecursionError sur les grands entiers.
    """
    while b != 0:
        a, b = b, a % b
    return a

def inverseModulaire(e, phi):
    """
    Calcule l'inverse modulaire de e modulo phi tel que (e * d) % phi == 1.
    Utilise l'algorithme d'Euclide étendu de manière itérative.
    """
    r_prec, r_act = e, phi
    x_prec, x_act = 1, 0
    y_prec, y_act = 0, 1

    while r_act != 0:
        quotient = r_prec // r_act
        r_prec, r_act = r_act, r_prec - quotient * r_act
        x_prec, x_act = x_act, x_prec - quotient * x_act
        y_prec, y_act = y_act, y_prec - quotient * y_act

    return x_prec % phi
    
def genereKeys(bits=1024, e=65537):
    """
    Génère une paire de clés RSA (publique et privée) ainsi que les paramètres intermédiaires.
    Par défaut, génère des nombres premiers de 1024 bits pour un module n de 2048 bits.
    """
    while True:
        p = generePrime(bits)
        q = generePrime(bits)

        if p != q:
            n = p * q
            phi = (p - 1) * (q - 1)

            if pgcd(e, phi) == 1:
                d = inverseModulaire(e, phi)
                return { 'public': (e, n),
                        'private': (d, n),
                        'p': p,
                        'q': q,
                        'phi': phi}
        
def encrypt(message, public_key):
    """
    Chiffre un message entier à l'aide de la clé publique RSA.
    Utilise l'exponentiation modulaire rapide native de Python : (message^e) % n.
    """
    return pow(message, public_key[0], public_key[1])

def decrypt(cipher_message, private_key):
    """
    Déchiffre un message crypté à l'aide de la clé privée RSA.
    Utilise l'exponentiation modulaire rapide native de Python : (cipher_message^d) % n.
    """
    return pow(cipher_message, private_key[0], private_key[1])


key = genereKeys()
m = 42
c = encrypt(m, key['public'])
d = decrypt(c, key['private'])
print(f"Original: {m} -> Ciphered : {c} -> Decipher : {d}")
