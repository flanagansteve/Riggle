#!/usr/bin/python3
import os, subprocess, random, string, time
# TODO: test windows support
    # TODO: does python need to open files using \ for windows? or does it still use /?

# TODO: randomly pick port num
port_num = "35003"
devnet_directory = ""
devnet_address = ""
devnet_pwd = ""
miner_pid = 0
def instantiateNetwork(deployable_path, windows=False):
    global devnet_directory, devnet_address, devnet_pwd, miner_pid
    os.mkdir('devnet_info')

    # generate random directory name, to prevent collisions
    if not windows:
        devnet_directory = "./.ethereum/devnet"+''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    else:
        devnet_directory = ".\.ethereum\devnet"+''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    # generate random password, save to devnet_password.txt
    if not windows:
        password_file = open('./devnet_info/devnet_password.txt', 'w')
    else:
        password_file = open('.\devnet_info\devnet_password.txt', 'w')
    password_file.write(''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))
    password_file.close()
    if not windows:
        pwd_file = open('./devnet_info/devnet_password.txt', 'r')
    else:
        pwd_file = open('.\devnet_info\devnet_password.txt', 'r')
    devnet_pwd = pwd_file.readline()
    pwd_file.close()

    # create account in geth with password from devnet_password, write to account1.txt
    instantiate_geth_account = open('instantiate_geth_account.sh', 'w')
    if not windows:
        instantiate_geth_account.write("#!/bin/bash\ngeth --datadir " + devnet_directory + " account new --password ./devnet_info/devnet_password.txt > ./devnet_info/account1.txt")
    else:
        # TODO: which way do these slashes go? especially on the shebang
        # TODO: does geth work the same way in the cmd prompt as terminal?
        instantiate_geth_account.write("#!/bin/bash\ngeth --datadir " + devnet_directory + " account new --password .\devnet_info\devnet_password.txt > .\devnet_info\\account1.txt")
    instantiate_geth_account.close()
    if not windows:
        subprocess.check_call(["chmod", "+rwx", "./instantiate_geth_account.sh"])
        subprocess.check_call(["./instantiate_geth_account.sh"])
    else:
        subprocess.check_call(["start", "instantiate_geth_account.sh"])

    # get address from account1.txt
    if not windows:
        devnet_address = open('./devnet_info/account1.txt', 'r').readline()
    else:
        devnet_address = open('.\devnet_info\account1.txt', 'r').readline()
    devnet_address = devnet_address[devnet_address.index("{")+1:devnet_address.index("}")]

    # write to genesis.json, with standard stuff + account address from account1.txt allocated iwth lots of eth
    if not windows:
        genesis_json = open('./devnet_info/genesis.json', 'w')
    else:
        genesis_json = open('.\devnet_info\genesis_json', 'w')
    genesis_json.write("{\n\t\"config\": {" +
                       "\n\t\t\"chainId\": 15,\n\t\t\"homesteadBlock\": 0,\n\t\t\"eip155Block\": 0,\n\t\t\"eip158Block\": 0\n\t}," +
                       "\n\t\"difficulty\": \"200\",\n\t\"gasLimit\": \"2100000000000\",\n\t\"alloc\": {" +
                       "\n\t\t\"" + devnet_address + "\": { \"balance\": \"99999999999999999999999999999999999999\" }\n\t}\n}\n")
    genesis_json.close()

    # init geth network from this genesis, executed via shell script
    init_geth = open('init_geth.sh', 'w')
    if not windows:
        init_geth.write("#!/bin/bash\ngeth --verbosity 0 --datadir "+devnet_directory+" init ./devnet_info/genesis.json")
        init_geth.close()
        subprocess.check_call(["chmod", "+rwx", "./init_geth.sh"])
        subprocess.check_call(["./init_geth.sh"])
    else:
        # TODO: does geth work the same way in the cmd prompt as terminal?
        # TODO: slashes for shebang?
        init_geth.write("#!/bin/bash\ngeth --verbosity 0 --datadir "+devnet_directory+" init .\devnet_info\genesis.json")
        init_geth.close()
        subprocess.check_call(["start", "init_geth.sh"])

    # TODO: support windows
    # start mining, also executed via shell script
    init_miner = open('init_miner.sh', 'w')
    init_miner.write("#!/bin/bash\ngeth --port " + port_num + " --verbosity 0 --datadir "+devnet_directory+" --mine -minerthreads 1 -etherbase 0 &")
    init_miner.close()
    subprocess.check_call(["chmod", "+rwx", "./init_miner.sh"])
    subprocess.check_call(["./init_miner.sh"])
    # TODO: fix message to point to correct file path for system (argh windows)
    print("Your development network is set up with a miner runnng and a loaded account for you to deploy from. Unlock your account " + devnet_address + " with password " + devnet_pwd + " and set it to eth.accounts[0], copy and paste the deployment text from " + deployable_path + " into the console, and begin interacting with your contract!")

def deployContract(web3_source, windows=False):
    # TODO: some way to check when miner is up, then launch this. Currently
    # just hard coding in a delay
    time.sleep(2.5)
    # TODO: unlock account
    #unlock_account = open('unlock_account.sh', 'w')
    #unlock_account.write("#!/bin/bash\ngeth --port " + port_num + " --datadir " + devnet_directory + " account --unlock " + devnet_address + " --password " + devnet_pwd)
    #unlock_account.close()
    #subprocess.check_call(["chmod", "+rwx", "./unlock_account.sh"])
    #subprocess.check_call(["./unlock_account.sh"])

    # TODO: does geth work the same way in the cmd prompt as terminal?
    # TODO: slashes for shebang?
    # initialise console
    init_console = open('init_console.sh', 'w')
    init_console.write("#!/bin/bash\ngeth --port " + port_num + " attach ipc:" + devnet_directory + "/geth.ipc console")
    init_console.close()
    subprocess.check_call(["chmod", "+rwx", "./init_console.sh"])
    subprocess.check_call(["./init_console.sh"])

    # TODO: somehow input web3 text into geth console.

def cleanUp(windows=False):
    # clean up
    if not windows:
        os.remove("devnet_info/account1.txt")
        os.remove("devnet_info/devnet_password.txt")
        os.remove("devnet_info/genesis.json")
    else:
        os.remove("devnet_info\\account1.txt")
        os.remove("devnet_info\devnet_password.txt")
        os.remove("devnet_info\genesis.json")
        os.rmdir('devnet_info')
    os.rmdir('devnet_info')
    os.remove("instantiate_geth_account.sh")
    os.remove("init_geth.sh")
    os.remove("init_miner.sh")
    os.remove("init_console.sh")
    if not windows:
        subprocess.check_call(["pkill", "geth"])
    else:
        # TODO: idk if this works like this
        subprocess.check_call(["pskill", "geth"])
    #os.remove("unlock_account.sh")
