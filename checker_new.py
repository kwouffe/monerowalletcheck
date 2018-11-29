#!/usr/bin/env python
import requests
import json
import datetime
import sys
import os
import re
from concurrent.futures import ThreadPoolExecutor as PoolExecutor

#disable SSL warning
requests.packages.urllib3.disable_warnings()

# open pools and wallets JSON files
with open("pools.json", 'r') as pools_file:
        pools = json.load(pools_file)
pool_list=pools["pools"]

with open("wallets.json", 'r') as wallets_file:
        wallets = json.load(wallets_file)
wallet_list=wallets["wallets"]

# initiate time, log folder and results
now = datetime.datetime.now().replace(microsecond=0)

results={}


def checker(wallets,pools):
    #building list of request to be made -- wallet + pool

    for wallet in wallets:
        actions = []
        if not set(tags).intersection(wallet['tags']):
            continue
        for pool in pools:
            if wallet['coin'] == pool['coin']:
                action = {"wallet":wallet,"pool":pool}
                actions.append(action)
        if actions != []:
            print(wallet['wallet_addr'])
            results.update({wallet['wallet_addr']:{}})
            with PoolExecutor(max_workers=16) as executor:
                for _ in executor.map(process_wallet, actions):
                    pass
            ##
            #for action in actions:
            #    process_wallet(action)
            ##

def process_wallet(action):
    wallet = action['wallet']
    pool = action['pool']
    results[wallet['wallet_addr']].update({pool['pool_name']:{}})
    results[wallet['wallet_addr']][pool['pool_name']].update({"pool_API_type":pool['pool_API_type']})
    if pool['pool_API_type'] == 'node-cryptonote-pool':
        data=node_cryptonote_pool(pool, wallet)
        if data != None:
            results[wallet['wallet_addr']][pool['pool_name']].update({'results':data})
    elif pool['pool_API_type'] == 'nodejs-pool':
        data=nodejs_pool(pool, wallet)
        if data != None:
            results[wallet['wallet_addr']][pool['pool_name']].update({'results':data})
    elif pool['pool_API_type'] == 'nanopool':
        data=nanopool(pool, wallet)
        if data != None:
            results[wallet['wallet_addr']][pool['pool_name']].update({'results':data})
    elif pool['pool_API_type'] == 'dwarfpool':
        data=dwarfpool(wallet)
        if data != None:
            results[wallet['wallet_addr']][pool['pool_name']].update({'results':data})
    elif pool['pool_API_type'] == 'skypool':
        data=skypool(pool, wallet)
        if data != None:
            results[wallet['wallet_addr']][pool['pool_name']].update({'results':data})



def node_cryptonote_pool(pool, wallet):
    try:
        url = pool['pool_API_url'] + 'stats_address?address=' + wallet['wallet_addr']
        resp = requests.get(url, timeout=13, verify=False)
        output = json.loads(resp.text)
        return output
    except:
        return None

def nodejs_pool(pool, wallet):
    try:
        url = pool['pool_API_url'] + 'miner/' + wallet['wallet_addr'] + '/stats'
        resp = requests.get(url, timeout=13)
        output = json.loads(resp.text)
        return output
    except:
        return None

def nanopool(pool, wallet):
    try:
        url = pool['pool_API_url'] + 'load_account/' + wallet['wallet_addr']
        resp = requests.get(url, timeout=13)
        output_account = json.loads(resp.text)
        url = pool['pool_API_url'] + 'payments/' + wallet['wallet_addr']
        resp = requests.get(url, timeout=13)
        output_payments = json.loads(resp.text)
        data={"account":output_account,"payments":output_payments}
        return(data)
    except:
        return None

def dwarfpool(wallet):
    try:
        url = 'http://dwarfpool.com/xmr/address?wallet=' + wallet['wallet_addr']
        resp = requests.get(url, timeout=13)
        #print(resp.text)
        toto=re.findall("badge-money\".*XMR",resp.text)
        if toto != []:
            data={"balance":toto[0].split(">")[1].split(" ")[0],"paid":toto[1].split(">")[1].split(" ")[0]}
            return data
        else:
            data={"error": "not found"}
            return data
    except:
        return None

def skypool(pool, wallet):
    try:
        url = pool['pool_API_url'] + 'address_status?address=' + wallet['wallet_addr']
        resp = requests.get(url, timeout=13, verify=False)
        output = json.loads(resp.text)
        return output
    except:
        return None

# main
if len(sys.argv) == 1:
    print("Usage: python monerowalletcheck.py tags")
    print("example: python monerowalletcheck.py monero APT666")
    sys.exit()
else:
    tags = sys.argv[1:len(sys.argv)]

checker(wallet_list,pool_list)

output = {}
output.update({"date":str(datetime.datetime.now())})
output.update({"tags":tags})
output.update({"results":results})

logfile = "log_" + str(now) + ".json"
logfile=logfile.replace(" ","-")
logfile=logfile.replace(":","-")
with open(logfile, 'w') as log_output:
    log_output.write(json.dumps(output, indent=4))


print("\n\n\t**********************************************")
print("\t***                 Done                   ***")
print("\t**********************************************")

print("\n\t run $python parser.py %s to analyse output " % logfile)
