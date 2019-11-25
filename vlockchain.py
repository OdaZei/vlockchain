import RelativeChain
import zChain

#create blockchain
new_balance=0.0
vlockchain = RelativeChain.BlockChain()
rwd=vlockchain.REWARD
my_addr=vlockchain.obtain_New_Address()
zc = zChain.CoinExpender()
def add_coins():
    if(len(vlockchain.chain) ==1):
        for i in range(int(rwd)):
            zc.create_coin(vlockchain.chain[0])
    else:
        for i in range(int(rwd)):
            zc.create_coin(vlockchain.chain[len(vlockchain.chain)-1])
for i in range(3):
    vlockchain.block_mining(my_addr)
    add_coins()
    


#THE BLOCKCHAIN FOR EACH NEW BLOCK GENERATES N COINS BEEING HIS IDENTIFIER THE BLOCK THEY BEEN GENERATED ON


    
print("This is your genesis block"+str(vlockchain.chain))
chain_lenght=len(zc.chain)
for i in range(chain_lenght):
    block=zc.chain[i].first_block
    new_balance +=vlockchain.check_Address_balance(my_addr,block)/rwd
    print("block id when it was generated:"+str(block.indicator)+"Coin number---"+str(i)+"---Address of the coin:"+str(zc.chain[i].public_key))


print("all the coins have been deployed to wallet address: "+str(my_addr)+"current balance:"+str(new_balance))


    
