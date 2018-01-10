from solidityToDeployable import *
from setupDevnetAndDeploy import *
init()
defineContractObject()
instantiateContractObject(0)
instantiateNetwork(isWindows())
deployContract(fileToString(getDeployableContractPath()), isWindows())
cleanUp(isWindows())
