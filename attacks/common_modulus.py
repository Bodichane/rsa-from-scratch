from rsa import inverseModulaire, genereKeys, encrypt, pgcd

def euclideEtendu(a, b):
    """
    Calcule le PGCD et les coefficients de Bézout de manière itérative.
    Évite l'erreur RecursionError sur des entiers de grande taille.
    """
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def attackCommonModulus(c1, c2, e1, e2, n):
    """
    Exécute l'attaque par module commun RSA en utilisant l'identité de Bézout.
    Retrouve le message d'origine chiffré sous deux exposants e1 et e2 différents.
    """
    g, a, b = euclideEtendu(e1, e2)
    
    if g != 1:
        return None

    if a < 0:
        inv_c1 = inverseModulaire(c1, n)
        part1 = pow(inv_c1, -a, n)
    else:
        part1 = pow(c1, a, n)

    if b < 0:
        inv_c2 = inverseModulaire(c2, n)
        part2 = pow(inv_c2, -b, n)
    else:
        part2 = pow(c2, b, n)

    return (part1 * part2) % n


message = 42
e1, e2 = 65537, 17

while True:
    key = genereKeys(bits=1024, e=e1)
    if pgcd(e2, key['phi']) == 1:
        break

n = key['public'][1]

c1 = encrypt(message, (e1, n))
c2 = encrypt(message, (e2, n))

m = attackCommonModulus(c1, c2, e1, e2, n)
print(f"Message find: {m}")
