#How to create a private development network in geth
#in terminal:

#$ vim password.txt //set general account pwd
#$ geth --datadir ./.ethereum/devnet --password ./password.txt account new > account1.txt
#$ geth --datadir ./.ethereum/devnet --password ./password.txt account new > account2.txt
#$ cat account1.txt
#Address: {e832bbf754d08adc051cd3787474b39edc18bb95}
#$ cat account2.txt
#Address: {67e5026cf6349e0ed7275ce0d83b9928dfbffc9f}
#$ vim genesis.json //create genesis file if need be: https://github.com/ethereum/go-ethereum/wiki/Private-network [lower difficulty/increase funding at your preference]
#$ vim genesis.json //copy paste address into alloc field
#$ vim genesis.json //copy paste address into alloc field
#$ geth --datadir ./.ethereum/devnet init genesis.json
#$ geth --datadir ./.ethereum/devnet --mine -minerthreads 1 -etherbase 0

#new terminal window:
#$ geth attach ipc:./.ethereum/devnet/geth.ipc console

#in geth console:
#// if you’d like to deploy and interact from account 0, do below, otherwise customise as you please
#> eth.accounts[0] = “0x..." //account from account1.txt
#> personal.unlockAccount(eth.accounts[0], “password from password.txt”)
#> var namedContract =  //object definition
#> var contract = ... //contract instantiation
#	from: web3.eth.accounts[0]
#wait for “Contract mined successfully”
#> eth.defaultAccount = eth.accounts[0]

#and you’re ready to interact with your contract!

#How to wipe an old development network in geth
#in terminal:
#$ rm -r ./.ethereum/devnet
#$ rm account1.txt
#$ rm account2.txt
import subprocess

p = subprocess.Popen(["echo", "hello world > success.txt"], stdout=subprocess.PIPE)

print(p.communicate())
