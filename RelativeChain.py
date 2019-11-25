import hashlib
import json
import time
import wallet
isRunning=False
mineCoin = 1000000
supply = 200000000
DIFICULTY=40000000
REWARD = (supply/DIFICULTY)
#the time it takes for uploading a new block
nTime=2

class Block:

    def __init__(self, indicator, proof_no, prev_hash, data, timestamp=None):
        self.indicator = indicator
        self.proof_no = proof_no
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time()

    @property
    def calculate_hash(self):
        block_of_string = "{}{}{}{}{}".format(self.indicator, self.proof_no,
                                              self.prev_hash, self.data,
                                              self.timestamp)

        return hashlib.sha256(block_of_string.encode()).hexdigest()

    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self.indicator, self.proof_no,
                                               self.prev_hash, self.data,
                                               self.timestamp)


class BlockChain:

    def __init__(self):
        self.chain = []
        self.current_data = []
        self.nodes = set()
        self.construct_genesis()
        self.REWARD=REWARD
    def construct_genesis(self):
        self.construct_block(proof_no=0, prev_hash=0)


    def construct_block(self, proof_no, prev_hash):
        block = Block(
            indicator=len(self.chain),
            proof_no=proof_no,
            prev_hash=prev_hash,
            data=self.current_data)
        self.current_data = []

        self.chain.append(block)
        return block

    @staticmethod
    def check_validity(block, prev_block):
        if((prev_block.indicator + 1) != block.indicator):
            return False

        elif (prev_block.calculate_hash != block.prev_hash):
            return False

        elif not (BlockChain.verifying_proof(block.proof_no,
                                            prev_block.proof_no)):
            return False

        elif (block.timestamp <= prev_block.timestamp):
            return False

        return True

    def new_data(self, sender, recipient, quantity):
        self.current_data.append({
            'sender': sender,
            'recipient': recipient,
            'quantity': quantity
        })
        return True

    @staticmethod
    def proof_of_work(last_proof):
        '''this simple algorithm identifies a number f' such that hash(ff') contain 4 leading zeroes
         f is the previous f'
         f' is the new proof
        '''
        proof_no = 0
        while BlockChain.verifying_proof(proof_no, last_proof) is False:
            proof_no += 1

        return proof_no

    @staticmethod
    def verifying_proof(last_proof, proof):
        #verifying the proof: does hash(last_proof, proof) contain 4 leading zeroes?

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @property
    def latest_block(self):
        return self.chain[-1]

    def block_mining(self, details_miner):

        self.new_data(
            sender="0",  #it implies that this node has created a new block
            recipient=details_miner,
            quantity=
            REWARD,  #creating a new block (or identifying the proof number) is awarded with 5Z coins
        )

        last_block = self.latest_block

        last_proof_no = last_block.proof_no
        proof_no = self.proof_of_work(last_proof_no)

        last_hash = last_block.calculate_hash
        block = self.construct_block(proof_no, last_hash)

        return vars(block)
   
    def create_node(self, address):
        self.nodes.add(address)
        return True
    
    def obtain_block_object(block_data):
        #obtains block object from the block data

        return Block(
            block_data['indicator'],
            block_data['proof_no'],
            block_data['prev_hash'],
            block_data['data'],
            timestamp=block_data['timestamp'])

    def check_Address_balance(self,address,block):
        d=(block.data)
        t=d[0]
        w=0.0
        w=t.get("recipient")
        if(address==w):
            return t.get("quantity")
        return w
   
    def obtain_New_Address(self):
        t= str(wallet.CreateWallet())
        return t
 



