from random import getrandbits, randrange

def miller_rabin(num, k=40):
    """
    Miller-Rabin primality test.
    k is the number of verification rounds (40 rounds = near-absolute certainty).
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
 
def generate_prime(bits):
    """
    Generate a random prime of the given bit size.
    Uses Miller-Rabin to validate primality efficiently.
    """
    while True:
        num = getrandbits(bits) | 1
        num |= (1 << (bits - 1))
        
        if miller_rabin(num):
            return num 
    
def gcd(a, b):
    """
    Compute the greatest common divisor (GCD) of two numbers.
    Iterative version (Euclid's algorithm) to avoid RecursionError on large integers.
    """
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    """
    Compute the modular inverse of e modulo phi such that (e * d) % phi == 1.
    Uses the iterative extended Euclidean algorithm.
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
    
def generate_keys(bits=1024, e=65537):
    """
    Generate an RSA key pair (public and private) along with the intermediate parameters.
    By default, generates 1024-bit primes for a 2048-bit modulus n.
    """
    while True:
        p = generate_prime(bits)
        q = generate_prime(bits)

        if p != q:
            n = p * q
            phi = (p - 1) * (q - 1)

            if gcd(e, phi) == 1:
                d = mod_inverse(e, phi)
                return { 'public': (e, n),
                        'private': (d, n),
                        'p': p,
                        'q': q,
                        'phi': phi}
        
def encrypt(message, public_key):
    """
    Encrypt an integer message with the RSA public key.
    Uses Python's fast built-in modular exponentiation: (message^e) % n.
    """
    return pow(message, public_key[0], public_key[1])

def decrypt(cipher_message, private_key):
    """
    Decrypt an encrypted message with the RSA private key.
    Uses Python's fast built-in modular exponentiation: (cipher_message^d) % n.
    """
    return pow(cipher_message, private_key[0], private_key[1])


if __name__ == "__main__":
    key = generate_keys()
    m = 42
    c = encrypt(m, key['public'])
    d = decrypt(c, key['private'])
    print(f"Original : {m}")
    print(f"Ciphertext: {c}")
    print(f"Decrypted : {d}")
    assert d == m, "Decryption does not recover the original message"
    print("OK: decrypt(encrypt(m)) == m")
