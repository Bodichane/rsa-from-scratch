from os import urandom

import sys
from pathlib import Path

# Allows running this script directly from the repository root:
#   python attacks/<script>.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rsa import encrypt, decrypt, genereKeys

def addPadding(message, n):
    """
    Add PKCS#1 v1.5-compliant padding to an integer message.
    Ensures the final byte string is exactly the same size as the modulus n.
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
    Strip PKCS#1 v1.5 padding from a decrypted integer to recover the original message.
    Checks for the 0x00 and 0x02 markers.
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
    Simulate an RSA padding oracle.
    Returns True if the decrypted message follows the PKCS#1 v1.5 structure, False otherwise.
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
    First phase of the Bleichenbacher attack.
    Searches for the first valid multiplier s above the initial mathematical bound.
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

    # Bleichenbacher phase 1: find the first multiplier s such that
    # c * s^e mod n is still accepted by the padding oracle.
    s = find(c, key['public'][0], n, key['private'])

    print(f"Message          : {message}")
    print(f"First valid s    : {s}")

    # Check that the padding round-trips correctly.
    assert removingPadding(decrypt(c, key['private']), n) == message, \
        "PKCS#1 padding does not round-trip"
    print("OK: PKCS#1 v1.5 padding valid and oracle working")
