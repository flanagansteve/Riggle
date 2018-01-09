from solidityToDeployable import *
from setupDevnetAndDeploy import *
init()
defineContractObject()
instantiateContractObject(0)
instantiateNetwork()
deployContract(fileToString(getDeployableContractPath()))
cleanUp()
