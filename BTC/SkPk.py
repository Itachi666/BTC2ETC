import rabinMiller
import hashlib
import random
import base58
import ecdsa


def hash(s='1.pdf'):
    filename = s
    m = hashlib.sha256()
    with open(filename, 'rb') as fp:
        while True:
            blk = fp.read(4096)  # 4KB per block
            if not blk: break
            m.update(blk)
    salt = random.randrange(2 ** (31), 2 ** 32)
    m.update(str(salt))

    h = m.hexdigest()
    h = bin_sha256(h)
    return h, salt


def getInverse(i, j):
    phiN = (i - 1) * (j - 1)
    k = phiN / 3

    if (phiN % 3 == 1):
        return phiN - k
    if (phiN % 3 == 2):
        return k
    if (phiN % 3 == 0):
        return 0


def bin_ripemd160(instr):
    res = hashlib.new("ripemd160")
    res.update(bytearray.fromhex(instr))
    return res.hexdigest()


def bin_sha256(instr):
    return hashlib.sha256(bytearray.fromhex(instr)).hexdigest()


def pkHash(pk):
    m = bin_sha256(pk)
    m = bin_ripemd160(m)

    k = bin_sha256('6f' + m)
    k = bin_sha256(k)

    m = '6f' + m + k[:8]
    if m[0] == '0' and m[1] == '0':
        m = '1' + base58.b58encode_int(int(m, 16))
    else:
        m = base58.b58encode_int(int(m, 16))
    return m


def privateKeyToPublicKey(s):
    sk = ecdsa.SigningKey.from_string(s.decode('hex'), curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    return ('\04' + sk.verifying_key.to_string()).encode('hex')


def compressionPk(pk):
    pk_x = pk[2:66]
    pk_y = pk[66:130]
    if int(pk_y, 16) % 2 == 0:
        return '02' + pk_x
    else:
        return '03' + pk_x


def getWIF(k):
    k = 'ef' + k
    m = bin_sha256(bin_sha256(k))
    k = k + m[:8]
    k = base58.b58encode_int(int(k, 16))
    return k


def getprint(i, j, n, h, salt, sk, Wifsk, pk, compk, address):
    print 'p=', hex(i)[2:len(hex(i)) - 1]
    print 'q=', hex(j)[2:len(hex(j)) - 1]
    print 'n=', hex(n)[2:len(hex(n)) - 1]
    print 'h=', h
    print 'Salt=', hex(salt)[2:len(hex(salt)) - 1]
    print 'Sk=', hex(sk)[2:len(hex(sk)) - 1]
    print 'Wifsk=', Wifsk
    print 'Pk=', pk
    print 'ComPk=', compk
    print 'Address=', address


def checking(address, sk):
    if len(sk) != 52:
        return False
    k = base58.b58decode_int(sk)
    k = hex(k)[4:len(hex(k)) - 11]
    pk = privateKeyToPublicKey(k)
    com_pk = compressionPk(pk)
    final_pk = pkHash(com_pk)
    if address == final_pk:
        return True
    else:
        return False

def fromsk2compk(sk):
    k = base58.b58decode_int(sk)
    k = hex(k)[4:len(hex(k)) - 11]
    pk = privateKeyToPublicKey(k)
    com_pk = compressionPk(pk)
    return com_pk

def generate_pq():
    while True:
        i = rabinMiller.generateLargePrime()
        j = rabinMiller.generateLargePrime()
        inverse3 = getInverse(i, j)
        if (inverse3 != 0):
            break

    return i, j, inverse3


def main():
    x = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    p = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
    h, salt = hash('C:/Users/Niujx/Documents/GitHub/Imtest/1.pdf')

    i, j, inverse3 = generate_pq()
    n = i * j

    sk = pow(int(h, 16), inverse3, n) % q
    # sk = int('1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD', 16)
    Wifsk = getWIF(hex(sk)[2:len(hex(sk)) - 1] + '01')
    pk = privateKeyToPublicKey(hex(sk)[2:len(hex(sk)) - 1])
    com_pk = compressionPk(pk)
    final_pk = pkHash(com_pk)

    getprint(i, j, n, h, salt, sk, Wifsk, pk, com_pk, final_pk)
    return i, j, n, h, salt, sk, Wifsk, pk, com_pk, final_pk


def getall(i, j, inverse3, path):
    x = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    p = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
    h, salt = hash(path)

    n = i * j

    sk = pow(int(h, 16), inverse3, n) % q
    # sk = int('1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD', 16)
    Wifsk = getWIF(hex(sk)[2:len(hex(sk)) - 1] + '01')
    pk = privateKeyToPublicKey(hex(sk)[2:len(hex(sk)) - 1])
    com_pk = compressionPk(pk)
    final_pk = pkHash(com_pk)

    return i, j, n, h, salt, sk, Wifsk, pk, com_pk, final_pk


