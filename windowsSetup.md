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
