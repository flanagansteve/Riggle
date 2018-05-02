#Set up a private chain with a miner

## First, in the command prompt:

Set the password for your accounts:

    > echo password > password.txt

Create the account in a new chain called devnet:

    > geth --datadir ./.ethereum/devnet --password ./password.txt account new > account1.txt

Copy and paste the address for this new account:

    > notepad account1.txt

Create a genesis file of this form, putting your account from account1.txt in the alloc field, and save it as genesis.json:

    {
        "config": {
            "chainId": 15,
            "homesteadBlock": 0,
            "eip155Block": 0,
            "eip158Block": 0
        },
        "difficulty": "200",
        "gasLimit": "2100000000000",
        "alloc": {
            "YOUR ADDRESS HERE": { "balance": "99999999999999999999999999999999999999" }
        }
    }

Next, initialise the blockchain:

    > geth --datadir ./.ethereum/devnet init genesis.json

And set up a miner:

    > geth --datadir ./.ethereum/devnet --mine -minerthreads 1 -etherbase 0

In a new command prompt window, open a geth console attached to your custom chain:

    > geth attach ipc:./.ethereum/devnet/geth.ipc console

Now, in the geth console, set your loaded account as the default:

    > eth.defaultAccount = eth.accounts[0]

Unlock it:

    > personal.unlockAccount(eth.accounts[0], “password from password.txt”, 0)

and now you're ready to deploy a contract!

# Deploy a contract
If you've been using Riggle, the deployable contract text can be found in [myDappProjectDirectory]/deployable_contractname.txt.

Copy and paste the deployable text into the geth console, after unlocking your account (see above)

    > var contractNameContract = ... // this is the contract object definition
    > var param1 = ...; // set the constructor constructor parameters
    > var contractName = new contratNameContract({... // this instantiates the contract

Once you receive a "Contract mined successfully ..." message, you are ready to interact with the contract.

# Clean up
Making a private devnet will leave behind some old data. Remove it on windows via the following command prompt commands:

    > rmdir ./.ethereum/devnet
    > del account1.txt
