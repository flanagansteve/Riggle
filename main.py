from solidityToDeployable import *
from setupDevnetAndDeploy import *
#TODO move off py-solc by making a command line call to solc directly
#TODO see exec todos in setupDevnetAndDeploy
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
defineContractObjects()
getConstructorParams()
instantiateNetwork(getDeployableContractPath(), isWindows())
if getDeployableContractPath() == "Only want devnet":
    deployContract("", isWindows())
else:
    deployContract(fileToString(getDeployableContractPath()), isWindows())
cleanUp(isWindows())
