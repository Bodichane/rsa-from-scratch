import os
from rsa import cipher, decipher, genereKeys

def addPadding(message, n):
    message_size = (message.bit_length() + 7) // 8
    message_bytes = message.to_bytes(message_size, 'big')
    n_size = (n.bit_length() + 7) // 8
    n_padding = n_size - len(message_bytes) - 4
    random_bytes = b''
    while len(random_bytes) < n_padding:
        b = os.urandom(1)
        if(b != b'\x00'):
            random_bytes += b

    padded_bytes = b'\x00\x02' + random_bytes + b'\x00' + message_bytes
    return int.from_bytes(padded_bytes, 'big')

def removingPadding(padded_int, n):
    padded_size = (n.bit_length() + 7) // 8
    padded_bytes = padded_int.to_bytes(padded_size, 'big')

    if(padded_bytes[0] == 0x00 and padded_bytes[1] == 0x02):
        separate = padded_bytes.index(b'\x00', 2)
        if(separate >= 2):
            message_bytes = padded_bytes[separate + 1:]
            return int.from_bytes(message_bytes, 'big')

def oracle(c, private_key):
    n = private_key[1]
    decrypted = decipher(c, private_key)
    padded_bytes = decrypted.to_bytes((n.bit_length() + 7) // 8, 'big')
    return padded_bytes[0] == 0x00 and padded_bytes[1] == 0x02

def find(c, e, n, private_key):
    s = 2
    while True:
        c_ = c * pow(s, e, n) % n

        if(oracle(c_, private_key)):
            return s
        else:
            s += 1


key = genereKeys()
padded = addPadding(42, key['public'][1])
c = cipher(padded, key['public'])
s = find(c, key['public'][0], key['public'][1], key['private'])
print(f"First valid s : {s}")
