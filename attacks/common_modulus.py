import sys
from pathlib import Path

# Allows running this script directly from the repository root:
#   python attacks/<script>.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rsa import inverseModulaire, genereKeys, encrypt, pgcd

def euclideEtendu(a, b):
    """
    Compute the GCD and Bézout coefficients iteratively.
    Avoids RecursionError on large integers.
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
    Run the RSA common-modulus attack using Bézout's identity.
    Recovers the original message encrypted under two different exponents e1 and e2.
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


if __name__ == "__main__":
    message = 42
    e1, e2 = 65537, 17

    # Both exponents must be invertible modulo phi(n) so that the two
    # encryptions are valid under the same modulus n.
    while True:
        key = genereKeys(bits=1024, e=e1)
        if pgcd(e2, key['phi']) == 1:
            break

    _, n = key['public']
    c1 = encrypt(message, (e1, n))
    c2 = encrypt(message, (e2, n))

    retrouve = attackCommonModulus(c1, c2, e1, e2, n)

    print(f"Message   : {message}")
    print(f"Recovered : {retrouve}")
    assert retrouve == message, "The attack did not recover the message"
    print("OK: message recovered without any private key")
