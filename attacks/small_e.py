from rsa import genereKeys, cipher

def attackSmallE(c):
    return int(round(c ** (1/3)))


key = genereKeys(16, e=3)
message = 285
c = cipher(message, key['public'])
m = attackSmallE(c)
print(f"Original: {message} -> Ciphered: {c} -> Deciphered: {m}")
