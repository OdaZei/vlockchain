import hashlib , os,binascii,base58,ecdsa

filepath="txt.txt"
def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d
def randomNumber():
     prk=os.urandom(32)
     return prk
def getPrivKey(x):
    fullkey = '00' + binascii.hexlify(x).decode()
    sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
    sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
    WIF = base58.b58encode(binascii.unhexlify(fullkey+sha256b[:8]))
    return WIF.decode()
def getPubKey(x):
    sk = ecdsa.SigningKey.from_string(x, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    publ_key = "04" + binascii.hexlify(vk.to_string()).decode()
    hash160 = ripemd160(hashlib.sha256(binascii.unhexlify(publ_key)).digest()).digest()
    publ_addr_a = b"\x99" + hash160
    checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
    publ_addr_b = base58.b58encode(publ_addr_a + checksum)
    return publ_addr_b.decode()

def CreateWallet():
    x=randomNumber()
    c=getPrivKey(x)
    v=getPubKey(x)
    with open(filepath,"a") as fp:
        fp.write(str(c)+"    "+str(v))
    return v 



