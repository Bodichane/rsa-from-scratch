from rsa import inverseModulaire, genereKeys, cipher

def euclideEtendu(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = euclideEtendu(b, a % b)
    return g, y, x - (a // b) * y

def attackCommonModulus(c1, c2, e1, e2, n):
    g, a, b = euclideEtendu(e1, e2)

    if(a < 0):
        part1 = pow(inverseModulaire(c1, n), -a, n)
    else:
        part1 = pow(c1, a, n)

    if(b < 0):
        part2 = pow(inverseModulaire(c2, n), -b, n)
    else:
        part2 = pow(c2, b, n) 
    
    return part1 * part2 % n


message = 42
e1, e2 = 65537, 17
key = genereKeys(16, e1)
c1 = cipher(message, (e1, key['public'][1]))
c2 = cipher(message, (e2, key['public'][1]))
m = attackCommonModulus(c1, c2, e1, e2, key['public'][1])
print(f"Message find: {m}")
