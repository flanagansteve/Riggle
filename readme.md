---
title: Welcome!
---

Hello, and thanks for using Riggle! This product is currently in beta, so please, do not hesitate to open issues on this repository so we can continue to improve it.

You must have py-solc installed to use this. Run "pip install py-solc" to get it. Riggle was designed and tested to run on python3, but I haven't tested it on python2 so don't be afraid to try your luck there.

To use Riggle, download this repository, and write up a contract in Solidity. When you're ready to test and deploy your contract, run the Python program solidityToDeployable.py from the Riggle folder. The program will prompt you for the location of your contract and ideally write some deployable web3 text to your project directory. You can then copy and paste this deployable text into a geth console to interact with your contract, provided the account you asked Riggle to deploy is unlocked.

Coming soon: 

- 1. a tool to prop up a development network automatically for you, deploying your contract's web3 automatically so that you can go straight from development to testing 
- 2. automated testing 
- 3. a full fledged GUI so that you can have a nice IDE to drive you towards becoming a smart contract pro.

I've attached a quick guide for setting up a private ethereum development network to test on, to help you get started. Happy coding! And again, please leave feedback so I can make this tool as useful as possible.

\- Steve from Orion Blockchain Solutions

Tips: 0xDE1fa3159b2D8892Ef83648E639F1ee21Fc68F88
