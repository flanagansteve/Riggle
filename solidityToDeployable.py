#!/usr/bin/python3
import sys
try:
    from solc import compile_source, compile_files, compile_standard
except:
    print("Install py-solc to use this tool. You can do so with: \"pip3 install py-solc\"")
    sys.exit()
# this is a tool to convert your Solidity smart contract source
# code to a deployable web3 format. you can copy and paste the output
# into a geth console and then interact with your contract from there

# installation requirements: python3, geth, py-solc

# Steve Flanagan of Orion Blockchain Solutions made this, and you can send tips his way at:
# 0xDE1fa3159b2D8892Ef83648E639F1ee21Fc68F88

# have fun!
# TODO: potentially handle .sol's with more than one contract
# and compile separate web3 deploys.
# TODO: handle structs?
# TODO: handle multi-line function headers

contract_source = None
contract_name = None
deployable_path = None
contract = None
deployable_contract = None
windows = None
constructor_parameters = list()

def init():
    global contract_source, contract, deployable_path, deployable_contract, windows, contract_name
    contract_source = input("Where's the solidity source for this contract?\n")
    contract = None
    while(contract is None):
        try:
            contract = open(contract_source, 'r')
        except FileNotFoundError:
            contract_source = input("File Not Found\nInput file location as:\nproject_directory/Contract.sol\nor\nproject_directory/contracts/Contract.sol,\npresuming you're working from the directory above your project\n")
    try:
        # osx and linux
        windows = False
        contract_name = contract_source[contract_source.rindex('/')+1:contract_source.index('.sol')]
    except ValueError:
        # windows
        windows = True
        contract_name = contract_source[contract_source.rindex('\\')+1:contract_source.index('.sol')]

    if "/contracts/" in contract_source or "\\contracts\\" in contract_source:
        # TODO: fix this
        # if in a contracts-only directory, we will save this one directory up,
        # ie the broader project directory
        print("In a contract directory, writing output in project directory: ")
        project_directory = contract_source[:contract_source.index(contract_name+".sol")]
        if windows:
            project_directory = project_directory[:project_directory.rindex("\\")]
            project_directory = project_directory[:project_directory.rindex("\\")+1]
        else:
            project_directory = project_directory[:project_directory.rindex("/")]
            project_directory = project_directory[:project_directory.rindex("/")+1]
        print(project_directory)
        deployable_path = project_directory + "deployable_"+contract_name.lower()+'.txt'
    else:
        # if not in a contract directory (ie, using truffle), I presume we
        # should put deployable contracts in same directory as provided source
        print("Putting output in same directory as provided source contract: "
            + contract_source[:contract_source.index(contract_name+".sol")])
        deployable_path = contract_source[:contract_source.index(contract_name+".sol")] + "deployable_"+contract_name.lower()+'.txt'
    deployable_contract = open(deployable_path, 'w')

# create the contract object, including its functions and held values
def defineContractObject():
    global constructor_parameters
    search_for_con_params = open(contract_source, 'r')
    for line in search_for_con_params:
        if "function" in line and "//" not in line[:line.index("function")]:
            if " " + contract_name + "(" in line:
                # is constructor so grab parameters
                parameters = line[line.index("(")+1:line.index(")")]
                if len(parameters) > 0:
                    for input in parameters.split(","):
                        input_info = input.split()
                        deployable_contract.write("var " + input_info[1] + " = /* insert " + input_info[0] + " here */;\n")
                        constructor_parameters.append(input_info)
    search_for_con_params.close()
    deployable_contract.write("var " + contract_name.lower() + "Contract = web3.eth.contract([")
    for line in contract:
        # get function info from header
        try:
            if "function" in line and "//" not in line[:line.index("function")]:
                deployable_contract.write("{\"constant\":")
                if "constant" in line:
                    deployable_contract.write("true,")
                else:
                    deployable_contract.write("false,")

                deployable_contract.write("\"inputs\":[")
                parameters = line[line.index("(")+1:line.index(")")]
                inputWeb3 = ""
                if len(parameters) > 0:
                    for input in parameters.split(","):
                        input_info = input.split()
                        if input_info[0] == "uint":
                            input_info[0] = "uint256"
                        inputWeb3 += "{\"name\":\"" + input_info[1] + "\",\"type\":\""+input_info[0]+"\"}, "
                    inputWeb3 = inputWeb3[:inputWeb3.rindex(",")]
                deployable_contract.write(inputWeb3)
                deployable_contract.write("],")

                deployable_contract.write("\"name\":\"" + line[line.index("function ")+len("function "):line.index("(")] + "\",")

                deployable_contract.write("\"outputs\":[")
                outputWeb3 = ""
                if "returns(" in line:
                    output_declaration = line[line.index("returns(") + len("returns("):]
                    output_declaration = output_declaration[:output_declaration.index(")")]
                    for output in output_declaration.split(","):
                        output_info = output.split()
                        if output_info[0] == "uint":
                            output_info[0] = "uint256"
                        if len(output_info) == 2:
                            outputWeb3 += "{\"name\":\"" + output_info[1] + "\",\"type\":\""+output_info[0]+"\"}, "
                        else:
                            outputWeb3 += "{\"name\":\"\",\"type\":\""+output_info[0]+"\"}, "
                    outputWeb3 = outputWeb3[:outputWeb3.rindex(",")]
                    deployable_contract.write(outputWeb3)
                elif "returns (" in line:
                    output_declaration = line[line.index("returns (") + len("returns ("):]
                    output_declaration = output_declaration[:output_declaration.index(")")]
                    outputWeb3 = ""
                    for output in output_declaration.split(","):
                        print(output_info)
                        output_info = output.split()
                        if output_info[0] == "uint":
                            output_info[0] = "uint256"
                        if len(output_info) == 2:
                            outputWeb3 += "{\"name\":\"" + output_info[1] + "\",\"type\":\""+output_info[0]+"\"}, "
                        else:
                            outputWeb3 += "{\"name\":\"\",\"type\":\""+output_info[0]+"\"}, "
                    outputWeb3 = outputWeb3[:outputWeb3.rindex(",")]
                    deployable_contract.write(outputWeb3)
                deployable_contract.write("],")

                deployable_contract.write("\"payable\":")
                if " payable " in line:
                    deployable_contract.write("true,")
                else:
                    deployable_contract.write("false,")

                deployable_contract.write("\"stateMutability\":")
                # finds stateMutability from header. relies on the dev to declare stateMutability
                if "pure" in line:
                    deployable_contract.write("\""+ "pure" + "\",")
                if "view" in line:
                    deployable_contract.write("\""+ "view" + "\",")
                else:
                    if " payable " in line:
                        deployable_contract.write("\""+ "payable" + "\",")
                    else:
                        deployable_contract.write("\""+ "nonpayable" + "\",")

                # better way to get stateMutability:
                # if function changes some state:
                #    either payable or nonpayable? idk
                # else if function reads into storage (ie, get() in storage):
                #    view [no gas usage, calculated in node with cached vals]
                # else if function only uses given inputs and internal vals (ie, a function that takes in two nums returns sum):
                #    pure [ie, no gas usage, calculated in node]

                deployable_contract.write("\"type\":\"function\"")
                deployable_contract.write("},")
            # TODO: does the web3 deploy need to know about held values? if so,
            # find some way to determine whether this line is declaring
            # a held value. maybe by whitespace
            # TODO: what else might the network need to know about this contract?
        except ValueError as e:
            print(e, line)

    deployable_contract.write("\b])\n")
    contract.close()
def instantiateContractObject(account_sender_index: int):
    deployable_contract.write("var "+contract_name.lower()+" = "+contract_name.lower()+"Contract.new(\n")
    for constructor_param in constructor_parameters:
        deployable_contract.write("\t" + constructor_param[1] + ",\n")
    deployable_contract.write("\t{\n")
    deployable_contract.write("\t\tfrom: web3.eth.accounts["+str(account_sender_index)+"],\n")
    source = fileToString(contract_source)
    deployable_contract.write("\t\tdata: \'0x" + getContractBytecode(source) + "\',\n")
    # TODO: how do I calculate how much gas? remix seems to always use 470000
    deployable_contract.write("\t\tgas: \'470000\'\n")
    deployable_contract.write("\t}, function(e, contract){\n")
    deployable_contract.write("\t\tconsole.log(e, contract);\n")
    deployable_contract.write("\t\tif (typeof contract.address != 'undefined') {\n")
    deployable_contract.write("\t\t\tconsole.log(\'Contract successfully mined. address: \' + contract.address + \' transactionHash: \' + contract.transactionHash);\n\t\t}\n")
    deployable_contract.write("\t})\n")
    deployable_contract.close()

def fileToString(file_path):
    output = ""
    for line in open(file_path, "r"):
        output+=(line+"\n")
    return output

def getContractBytecode(contract_source_string):
    try:
        py_solc_result = compile_source(contract_source_string)
    except FileNotFoundError:
        print("Solc not installed. Please search online and install Solc to use this tool and to develop in Solidity")
        sys.exit()
    output = py_solc_result['<stdin>:'+contract_name]
    bytecode = output['bin']
    return bytecode

def getDeployableContractPath():
    return deployable_path

def isWindows():
    return windows
# TODO: should we get the Application Binary Interface from py-solc as well rather than generating our own?
