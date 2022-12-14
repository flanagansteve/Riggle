Hello, and thanks for using Riggle! This product is currently in beta, so please, do not hesitate to open issues on this repository so we can continue to improve it. This project runs on Python3, and Python2 support is not guaranteed, so please upgrade to use.

# Dependencies

- [Geth](https://github.com/ethereum/go-ethereum/wiki/Building-Ethereum): The GoLang implementation of Ethereum. OSX users can download using "brew install geth"
- [Solc](https://github.com/ethereum/solidity/releases): the official Solidity compiler executable. Download the correct archive for your system, extract, and run. Alternatively, run:

    $ brew tap ethereum/ethereum

    $ brew install solidity

- [py-solc](https://github.com/pipermerriam/py-solc/): a library that helps convert your smart contract to byte-code. You can install via pip using "pip3 install py-solc"

- [TKinter](https://wiki.python.org/moin/TkInter): the python library that runs the GUI. TKinter should come with OSX and Windows' Python installations. Install TKinter on Linux via "sudo apt-get install python3-tk"

# Use

## Command Line Interface
To use Riggle, download this repository, and write up a contract in Solidity. In a terminal or command prompt, run:

    $ python3 riggle/main.py

Riggle will prompt you for the location of your contract source, convert it to web3 deploy text, and write this resulting text to a file called deployable_contractname.txt in your contract's project directory. Next, it will instantiate a private development network running the ethereum protocol, create a loaded account for you to use on it, start a miner for this network, and open a console from which you can interact with this network. All you'll have to do is unlock your account:

    (OSX/Linux)
    > personal.unlockAccount(eth.accounts[0], "password", 0)

    (Windows)
    > personal.unlockAccount(eth.coinbase, "password", 0)


set that account as the default account:

    (OSX/Linux)
    > eth.defaultAccount = eth.accounts[0]

    (Windows)
    > eth.defaultAccount = eth.coinbase

and paste in the web3 deploy text from the deployable_contractname.txt file! Once the contract mines you'll be able to interact with your contract.

To simply spin up a development network, without providing a contract to compile, just press enter when you are prompted for a file to compile.

## GUI

To run the gui, open a terminal/command prompt and run:

    $ python3 riggle/gui.py

The GUI comes with a menu bar with several options that are self-explanatory. Specifically, deploy contracts by clicking on the "Deploy" menu and selecting "Deploy to devnet." Ropsten and mainnet deployment are coming soon!

Keep your eyes out for new features:

- Automatic contract deployment, so that you can instantly get to testing your contract once the network console is presented to you
- Automated testing
- A full fledged GUI so that you can have a nice IDE to drive you towards becoming a smart contract pro.

I've attached a quick guide for setting up a private ethereum development network to test on, to help you get started. Happy coding! And again, please leave feedback so I can make this tool as useful as possible.

\- Steve from Sublimity Blockchain

I've released this software for free, to benefit the Solidity community, but tips and support are always appreciated: 0xDE1fa3159b2D8892Ef83648E639F1ee21Fc68F88
