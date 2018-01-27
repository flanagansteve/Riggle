Here's a quick guide to how I set up and tested Riggle on a windows machine that had never run any Solidity before. Hopefully it works for you too. I come from a Linux/OSX background, so there very well may be a better way to do this

1. Download a .zip of this git repo
2. Extract
3. Download solidity from the solidity-windows.zip file at https://github.com/ethereum/solidity/releases
4. Extract that to the same parent directory as Riggle
5. Install py-solc using:
	C:\Python34\Scripts\pip3.exe install py-solc
6. Run the solidityToDeployable.py file by using:
	C:\Python34\python.exe C:\<your extracted directory>\solidityToDeployable.py
7. Use as directed in readme

To manually set up a dev network:

1. [Install geth](https://github.com/ethereum/go-ethereum/wiki/Installation-instructions-for-Windows)
2. Set the path variable for geth:
    > ...
3. Instantiate the development account from a password.txt file:
    > ...
4. Create a genesis.json file that geth will use as the initial conditions for your network:
    > ... todo: write a script for this
5. Create the development network via geth, referencing the genesis file:
    > ...
6. Run a miner for this network:
    > ...
7. In a new command prompt window, attach a console to this network and begin interacting!
    > ...
