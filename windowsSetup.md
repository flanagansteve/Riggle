#Set up a private chain with a miner

## First, in the command prompt:

    \> notepad password.txt //set general account pwd
    \> geth --datadir ./.ethereum/devnet --password ./password.txt account new > account1.txt
    \> notepad account1.txt //copy and paste address from notepad, will appear like this:
Address: {e832bbf754d08adc051cd3787474b39edc18bb95}
    \> notepad genesis.json //create genesis file if need be: https://github.com/ethereum/go-ethereum/wiki/Private-network [lower difficulty/increase funding at your preference]
    \> notepad genesis.json //paste address into 'alloc' field
    \> geth --datadir ./.ethereum/devnet init genesis.json
    \> geth --datadir ./.ethereum/devnet --mine -minerthreads 1 -etherbase 0

## In a new command prompt window:
    \> geth attach ipc:./.ethereum/devnet/geth.ipc console

## now, in the geth console you just opened:
    \> eth.defaultAccount = eth.accounts[0]
    \> personal.unlockAccount(eth.accounts[0], “password from password.txt”)

and now you're ready to deploy a contract!

# Deploy a contract
If you've been using Riggle, the deployable contract text can be found in [myDappProjectDirectory]/deployable_contractname.txt.

Copy and paste the deployable text into the geth console, after unlocking your account (see above)

    \> var contractNameContract = ... // this is the contract object definition
    \> var param1 = ...; // set the constructor constructor parameters
    \> var contractName = new contratNameContract({... // this instantiates the contract

Once you receive a "Contract mined successfully ..." message, you are ready to interact with the contract.

# Clean up
Making a private devnet will leave behind some old data. Remove it on windows via:
    \> rmdir ./.ethereum/devnet
    \> del account1.txt
