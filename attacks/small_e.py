from rsa import genereKeys, encrypt

def integerCubeRoot(n):
    """
    Calcule la racine cubique entière exacte d'un nombre n de n'importe quelle taille.
    Utilise la méthode de Newton sur des entiers pour éviter les limitations des nombres flottants.
    """
    if n < 0:
        return None
    if n == 0:
        return 0
    
    x = 1 << ((n.bit_length() + 2) // 3)
    while True:
        y = (2 * x + n // (x * x)) // 3
        if y >= x:
            return x
        x = y

def attackSmallE(c):
    """
    Exécute l'attaque par exposant faible (e=3) sur le texte chiffré c.
    Calcule la racine cubique exacte du chiffrement sans conversion en flottant.
    """
    return integerCubeRoot(c)


e = 3
message = 285

while True:
    key = genereKeys(bits=1024, e=e)
    n = key['public']
    
    if (message ** e) < n:
        break

c = encrypt(message, (e, n))
m = attackSmallE(c)

print(f"Original: {message} -> Ciphered: {c} -> Deciphered: {m}")
