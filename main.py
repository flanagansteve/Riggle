from solidityToDeployable import *
from setupDevnetAndDeploy import *
init()
defineContractObject()
instantiateContractObject(0)
instantiateNetwork(getDeployableContractPath(), isWindows())
deployContract(fileToString(getDeployableContractPath()), isWindows())
cleanUp(isWindows())
