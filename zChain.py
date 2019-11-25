import hashlib,os,binascii,base58,ecdsa

class ZCoin:

    def __init__(self,identity,first_block, public_key,spend):
        
        self.identity = identity #Coin identifier 
        self.first_block=first_block #This coins have been output as a reward for adding one block to the chain a 
        self.public_key=public_key #la private key sirve como instrumento de proteccion ante replicas , i para mandarlas
        self.spend = spend #este valor the permite gastar la moneda cambia con cada transaccion en la cual las monedas tengan lugar
    def __repr__(self):
        return "{} - {} - {} - {} ".format(self.identity,self.first_block,self.public_key,self.spend)
   
class CoinExpender():
    def __init__(self):
        self.chain = []

    def randNum(self):
        prk=os.urandom(32)
        return prk
    def ripemd160(self,x):
        d = hashlib.new('ripemd160')
        d.update(x)
        return d
        
    def getPrivKey(self,x):
        fullkey = '00' + binascii.hexlify(x).decode()
        sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
        
        return sha256a
    def getPubKey(self,x):
        sk = ecdsa.SigningKey.from_string(x, curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        publ_key = "04" + binascii.hexlify(vk.to_string()).decode()
        hash160 = self.ripemd160(hashlib.sha256(binascii.unhexlify(publ_key)).digest()).digest()
        publ_addr_a = b"\x99" + hash160
        checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
        publ_addr_b = base58.b58encode(publ_addr_a + checksum)
        return publ_addr_b.decode()
    
    def create_coin(self,first_block):
        rand=self.randNum()
        prk=self.getPrivKey(rand)
        pub_key = self.getPubKey(rand)
        
        zcoin =ZCoin(
            identity = len(self.chain),
            first_block =  first_block,
            public_key = pub_key,
            spend = int(0))
        self.chain.append(zcoin)
        return zcoin
            
        
    def spend_coin(self,identity):
        chain_lenght=len(self.chain)
        for i in range(chain_lenght):
            coins=self.chain[i].identity
            if(coins==identity):
                 return True
        

