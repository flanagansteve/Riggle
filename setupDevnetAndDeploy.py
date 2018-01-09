#!/usr/bin/python3
import os, subprocess, random, string
def instantiateNetwork():
    os.mkdir('devnet_info')
    #TODO: do we let user pick password, or use own random one?
    #      if user picks, then they may reuse a password which we won't store safely
    #      if randomly generated, user can't use password to reunlock as need be

    # generate random directory name, to prevent collisions
    devnet_directory = "./.ethereum/devnet"+''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    # generate random password, save to devnet_password.txt
    password_file = open('./devnet_info/devnet_password.txt', 'w')
    password_file.write(''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))
    password_file.close()
    pwd_file = open('./devnet_info/devnet_password.txt', 'r')
    devnet_pwd = pwd_file.readline()
    print('devnet account pwd is ' + devnet_pwd)
    pwd_file.close()

    # create account in geth with password from devnet_password, write to account1.txt
    # there are modules to run terminal commands w/arguments but they're not working right now. So
    # I'll write a temporary shell script, chmod it, and use that
    instantiate_geth_account = open('instantiate_geth_account.sh', 'w')
    instantiate_geth_account.write("#!/bin/bash\ngeth --datadir " + devnet_directory + " account new --password ./devnet_info/devnet_password.txt > ./devnet_info/account1.txt")
    instantiate_geth_account.close()
    subprocess.check_call(["sudo", "chmod", "+rwx", "./instantiate_geth_account.sh"])
    subprocess.check_call(["sudo", "./instantiate_geth_account.sh"])

    # get address from account1.txt
    devnet_address = open('./devnet_info/account1.txt', 'r').readline()
    devnet_address = devnet_address[devnet_address.index("{")+1:devnet_address.index("}")]
    print('devnet address is '+devnet_address)

    # write to genesis.json, with standard stuff + account address from account1.txt allocated iwth lots of eth
    print('writing genesis.json')
    genesis_json = open('./devnet_info/genesis.json', 'w')
    genesis_json.write("{\n\t\"config\": {" +
                       "\n\t\t\"chainId\": 15,\n\t\t\"homesteadBlock\": 0,\n\t\t\"eip155Block\": 0,\n\t\t\"eip158Block\": 0\n\t}," +
                       "\n\t\"difficulty\": \"200\",\n\t\"gasLimit\": \"2100000000000\",\n\t\"alloc\": {" +
                       "\n\t\t\"" + devnet_address + "\": { \"balance\": \"99999999999999999999999999999999999999\" }\n\t}\n}\n")
    genesis_json.close()

    # init geth network from this genesis, executed via shell script
    init_geth = open('init_geth.sh', 'w')
    init_geth.write("#!/bin/bash\ngeth --datadir "+devnet_directory+" init ./devnet_info/genesis.json")
    init_geth.close()
    subprocess.check_call(["sudo", "chmod", "+rwx", "./init_geth.sh"])
    subprocess.check_call(["sudo", "./init_geth.sh"])

    # start mining, also executed via shell script
    init_miner = open('init_miner.sh', 'w')
    init_miner.write("#!/bin/bash\n")
    # TODO: randomly pick port
    port_num = "35003"
    init_miner.write("sudo geth --verbosity 0 --datadir "+devnet_directory+" --mine -minerthreads 1 -etherbase 0")
    #init_miner.write("geth --port " + port_num + " --verbosity 0 --datadir "+devnet_directory+" --mine -minerthreads 1 -etherbase 0")
    init_miner.close()
    miner_script = open('init_miner.sh', 'r')
    print(miner_script.readline()+"\n"+miner_script.readline())
    miner_script.close()
    subprocess.check_call(["sudo", "chmod", "+rwx", "./init_miner.sh"])
    subprocess.Popen(["sudo", "./init_miner.sh"])
    print("network set up and miner running. open an ipc console in a new terminal to " + devnet_directory + "/geth.ipc, on port " + port_num + ", unlock your account " + devnet_address + " with password " + devnet_pwd + ", and deploy! need sudo")

    # TODO:
    # initialise console
    #print("ie, geth --port " + port_num + " attach ipc:" + devnet_directory + "/geth.ipc console")
    #init_console = open('init_console.sh', 'w')
    #init_console.write("#!/bin/bash\nsudo geth --port " + port_num + " attach ipc:" + devnet_directory + "/geth.ipc console")
    #init_console.close()
    #subprocess.check_call(["sudo", "chmod", "+rwx", "./init_console.sh"])
    #subprocess.check_call(["sudo", "./init_console.sh"])

# entering into console
# eth.accounts[0] = \"devnet_address\"
# eth.defaultAccount = eth.accounts[0]
# personal.unlockAccount(\"devnet_address\", \"devnet_password\")
# [possibly] prompt user for constructor parameters
# copy and paste parameter declarations
# copy and paste object def and instantiation
# show user console
# possibly: run automated interactions with contract

def deployContract(web3_source):
    pass

instantiateNetwork()
# deployContract(web3_source from other python path, console_path from instantiateNetwork))

# clean up
os.remove("devnet_info/account1.txt")
os.remove("devnet_info/devnet_password.txt")
os.remove("devnet_info/genesis.json")
os.rmdir('devnet_info')
os.remove("instantiate_geth_account.sh")
os.remove("init_geth.sh")
os.remove("init_miner.sh")
#os.remove("init_console.sh")
