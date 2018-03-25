from solidityToDeployable import *
from setupDevnetAndDeploy import *
#TODO: automatically install dependencies:
    # geth
    # Solc
    # py-solc
    # possibly tkinter?
        # sudo apt-get install python3-tk
    # possibly subprocess?
#TODO: set path variables for geth and solc
    # windows: setx or even just set
    # osx/linux: edit bash profile
init()
defineContractObject()
#defineContractObjectViaSolc()
instantiateContractObject(0)
if not isWindows():
    instantiateNetwork(getDeployableContractPath(), isWindows())
    deployContract(fileToString(getDeployableContractPath()), isWindows())
    cleanUp(isWindows())
else:
    print("Windows system detected. You will have to manually set up a development network")
    print("Please consult windowsSetup.md in this repository")
