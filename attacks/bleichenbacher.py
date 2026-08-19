from os import urandom

import sys
from pathlib import Path

# Permet de lancer ce script directement depuis la racine du dépôt :
#   python attacks/<script>.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rsa import encrypt, decrypt, genereKeys

def addPadding(message, n):
    """
    Ajoute un padding conforme aux spécifications PKCS#1 v1.5 à un message entier.
    Garantit que la chaîne d'octets finale fait exactement la même taille que le module n.
    """
    n_size = (n.bit_length() + 7) // 8
    message_size = (message.bit_length() + 7) // 8
    message_bytes = message.to_bytes(message_size, 'big')
    
    n_padding = n_size - len(message_bytes) - 3
    random_bytes = b''
    while len(random_bytes) < n_padding:
        b = urandom(1)
        if b != b'\x00':
            random_bytes += b

    padded_bytes = b'\x00\x02' + random_bytes + b'\x00' + message_bytes
    return int.from_bytes(padded_bytes, 'big')

def removingPadding(padded_int, n):
    """
    Supprime le padding PKCS#1 v1.5 d'un entier déchiffré pour retrouver le message initial.
    Vérifie la présence des marqueurs 0x00 et 0x02.
    """
    padded_size = (n.bit_length() + 7) // 8
    padded_bytes = padded_int.to_bytes(padded_size, 'big')

    if padded_bytes[0] == 0x00 and padded_bytes[1] == 0x02:
        separate = padded_bytes.index(b'\x00', 2)
        if separate >= 2:
            message_bytes = padded_bytes[separate + 1:]
            return int.from_bytes(message_bytes, 'big')
    return None

def oracle(c, private_key):
    """
    Simule un oracle de padding RSA.
    Retourne True si le message déchiffré respecte la structure PKCS#1 v1.5, False sinon.
    """
    n = private_key[1]
    n_size = (n.bit_length() + 7) // 8
    decrypted = decrypt(c, private_key)
    
    try:
        padded_bytes = decrypted.to_bytes(n_size, 'big')
        return padded_bytes[0] == 0x00 and padded_bytes[1] == 0x02
    except (OverflowError, ValueError):
        return False

def find(c, e, n, private_key):
    """
    Première phase de l'attaque de Bleichenbacher.
    Recherche le premier multiplicateur s valide supérieur à la borne mathématique initiale.
    """
    n_size = (n.bit_length() + 7) // 8
    B = 1 << (8 * (n_size - 2))
    s = (n + 3 * B - 1) // (3 * B)
    
    while True:
        c_ = (c * pow(s, e, n)) % n

        if oracle(c_, private_key):
            return s
        s += 1


if __name__ == "__main__":
    message = 42
    key = genereKeys()
    _, n = key['public']

    padded = addPadding(message, n)
    c = encrypt(padded, key['public'])

    # Phase 1 de Bleichenbacher : trouver le premier multiplicateur s tel que
    # c * s^e mod n soit encore accepté par l'oracle de padding.
    s = find(c, key['public'][0], n, key['private'])

    print(f"Message        : {message}")
    print(f"Premier s valide : {s}")

    # Vérifie que le padding fait bien l'aller-retour.
    assert removingPadding(decrypt(c, key['private']), n) == message, \
        "Le padding PKCS#1 ne fait pas l'aller-retour"
    print("OK : padding PKCS#1 v1.5 valide et oracle fonctionnel")
