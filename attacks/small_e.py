import sys
from pathlib import Path

# Allows running this script directly from the repository root:
#   python attacks/<script>.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rsa import genereKeys, encrypt

def integerCubeRoot(n):
    """
    Compute the exact integer cube root of a number n of any size.
    Uses Newton's method on integers to avoid floating-point limitations.
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
    Run the low-exponent attack (e=3) on ciphertext c.
    Computes the exact cube root of the ciphertext without floating-point conversion.
    """
    return integerCubeRoot(c)


if __name__ == "__main__":
    e = 3
    message = 285

    # Draw keys until m^e < n: this is the condition that makes the attack
    # possible (the modulus never wraps the ciphertext).
    while True:
        key = genereKeys(bits=1024, e=e)
        _, n = key['public']
        if (message ** e) < n:
            break

    c = encrypt(message, (e, n))
    retrouve = attackSmallE(c)

    print(f"Message    : {message}")
    print(f"Ciphertext : {c}")
    print(f"Recovered  : {retrouve}")
    assert retrouve == message, "The attack did not recover the message"
    print("OK: message recovered without factoring n")
