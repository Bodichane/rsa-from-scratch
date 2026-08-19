# RSA From Scratch

## Description
This project is an implementation of the RSA algorithm from scratch, without any
cryptographic libraries. It also implements a few attacks to try to break this
encryption scheme.

## Mathematical concepts

### GCD
Used to check that Euler's totient $\phi(n)$ and the encryption exponent $e$ are
coprime.

### Modular inverse
Since $e$ is coprime with $\phi(n)$, the Bézout theorem guarantees the existence
of two integers $d$ and $k$ such that:
$$ed = 1 + k\phi(n)$$
<br>This means $ed \equiv 1 \pmod{\phi(n)}$, which proves that $e$ is invertible
modulo $\phi(n)$. This property allows computing the decryption exponent:
`d = mod_inverse(e, phi)`.

### Euler's totient $\phi(n)$
An integer $p > 1$ is prime if and only if all numbers from $1$ to $p - 1$ are
coprime with $p$. We then have $\phi(p) = p - 1$. In the RSA case, for two primes
$p$ and $q$, we get:
$$\phi(n) = (p - 1)(q - 1)$$
<br>This value is essential to generate the system's private key.

### Modular exponentiation
Modular exponentiation computes the integer $c$ such that:
$$c \equiv m^e \pmod n$$
<br>This formula encrypts the message $m$ efficiently using the exponent $e$ and
the modulus $n$.

---

## Implemented attacks

### Low-exponent attack (Small $e$)
This attack can be exploited when the encryption exponent is very small
(typically $e = 3$). If the message $m$ is short, we may end up with $m^3 < n$.
Encryption then becomes a simple power:
$$c \equiv m^3 \pmod n \implies c = m^3$$
<br>It is then enough to compute the ordinary cube root of $c$ over the integers
to recover the plaintext, without factoring $n$.

### Common-modulus attack
This attack is possible when two users share the same modulus $n$ but have
different encryption exponents $e_1$ and $e_2$ to encrypt the same message $m$.
We have:
$$c_1 \equiv m^{e_1} \pmod n \quad \text{and} \quad c_2 \equiv m^{e_2} \pmod n$$
<br>If $\gcd(e_1, e_2) = 1$, the Bézout theorem guarantees that there exist two
integers $a$ and $b$ such that:
$$a \cdot e_1 + b \cdot e_2 = 1$$
<br>Using the extended Euclidean algorithm, we compute $a$ and $b$ (one of them
being negative, we use the modular inverse). We then recover the original message
as:
$$(c_1)^a \cdot (c_2)^b \equiv (m^{e_1})^a \cdot (m^{e_2})^b \equiv m^{a \cdot e_1 + b \cdot e_2} \equiv m^1 \equiv m \pmod n$$
<br>The message is thus intercepted without knowing the private keys.

### Bleichenbacher attack (PKCS#1 padding oracle)
This side-channel attack relies on a server acting as a padding oracle. The
server returns information (or a different error) depending on whether the
padding of the decrypted message is valid (`True`) or invalid (`False`).
The goal is to recover the message by carefully choosing successive integers $s$
and sending the modified ciphertext to the server:
$$c' \equiv c \cdot s^e \pmod n$$
<br>By analyzing the oracle's responses for different choices of $s$, we
progressively narrow the interval of possible values for the message until it is
fully isolated.

---

## Installation and usage

### Prerequisites
This project is developed in **Python 3**. No third-party library is required
since all functions (RSA and attacks) are coded from scratch.

### 1. Clone the project
```bash
git clone https://github.com/Bodichane/rsa-from-scratch
cd rsa-from-scratch
```

### 2. Run RSA encryption/decryption
To generate keys, encrypt and decrypt a demonstration message:
```bash
python rsa.py
```

### 3. Run the attack simulations
Each attack has its own demonstration script proving its feasibility:

* **Small $e$ attack**:
  ```bash
  python attacks/small_e.py
  ```
* **Common-modulus attack**:
  ```bash
  python attacks/common_modulus.py
  ```
* **Bleichenbacher attack**:
  ```bash
  python attacks/bleichenbacher.py
  ```

### Expected run times

All keys are generated at 2048 bits (two 1024-bit primes), without any
third-party library: key generation dominates the compute time. Measured on an
ordinary desktop machine:

| Script | Typical time | Output |
|---|---|---|
| `rsa.py` | ~10 s | checks that `decrypt(encrypt(m)) == m` |
| `attacks/small_e.py` | ~40 s | recovers the message without factoring `n` |
| `attacks/common_modulus.py` | ~5 s | recovers the message without any private key |
| `attacks/bleichenbacher.py` | ~30 s | finds the first `s` accepted by the oracle |

Each script ends with an assertion: an exit code of 0 means the attack actually
succeeded, not merely that the script ran.

## Project structure
* `rsa.py`: core mathematical primitives (Miller-Rabin, GCD, modular inverse,
  modular exponentiation) and RSA logic. Importable with no side effects — the
  demonstration is under `if __name__ == "__main__"`.
* `attacks/small_e.py`: low-exponent attack (`e = 3`).
* `attacks/common_modulus.py`: common-modulus attack.
* `attacks/bleichenbacher.py`: PKCS#1 v1.5 padding and padding oracle.

## Reflection
This project helped me understand the fundamentals of RSA encryption, from its
conceptual logic down to the mathematical functions behind it.

I ran into difficulties, particularly implementing the `mod_inverse()` and
`addPadding()` functions. While developing them, I learned to use new native
Python methods (such as `bit_length()`, `to_bytes()`, `from_bytes()`, etc.). By
the end of this project, I am now able to explain how RSA works as well as the
attacks it is vulnerable to.

## References and useful links
* [RSA encryption — Wikipedia](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
* [Euler's totient function — Wikipedia](https://en.wikipedia.org/wiki/Euler%27s_totient_function)
* [Bézout's identity — Wikipedia](https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity)
* [PKCS #1 — Wikipedia](https://en.wikipedia.org/wiki/PKCS_1)
* [RFC 8017 — PKCS #1 v2.2](https://www.rfc-editor.org/rfc/rfc8017)
* [Miller-Rabin primality test — Wikipedia](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test)
* Bleichenbacher, D. (1998). *Chosen Ciphertext Attacks Against Protocols Based on the RSA Encryption Standard PKCS #1*, CRYPTO ’98.
