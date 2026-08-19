import sys
from pathlib import Path

# Permet de lancer ce script directement depuis la racine du dépôt :
#   python attacks/<script>.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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


if __name__ == "__main__":
    e = 3
    message = 285

    # On tire une clé jusqu'à obtenir m^e < n : c'est la condition qui rend
    # l'attaque possible (le modulo ne « replie » jamais le chiffré).
    while True:
        key = genereKeys(bits=1024, e=e)
        _, n = key['public']
        if (message ** e) < n:
            break

    c = encrypt(message, (e, n))
    retrouve = attackSmallE(c)

    print(f"Message   : {message}")
    print(f"Chiffré   : {c}")
    print(f"Retrouvé  : {retrouve}")
    assert retrouve == message, "L'attaque n'a pas retrouvé le message"
    print("OK : message retrouvé sans factoriser n")
