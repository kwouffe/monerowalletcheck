#!/usr/bin/env python
import requests
import json
import datetime
import sys
import os

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

# clearing term and printing header

print("\t**********************************************")
print("\t***      Monero Pools Wallet Checker       ***")
print("\t***      Emilien Le Jamtel - CERT-EU       ***")
print("\t**********************************************")



# functions for each pool type

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

def dwarfpool(pool, wallet):
    try:
        url = pool['pool_API_url'] + '?wallet=' + wallet['wallet_addr']
        resp = requests.get(url, timeout=13)
        output = json.loads(resp.text)
        if 'error' not in output.keys() :
            print("-_-_-_-_-_-_-_-_-_-_-_-_-")
            print(pool['pool_name'])
            print("-_-_-_-_-_-_-_-_-_-_-_-_-")
            print(output)
    except:
        print("%s is down ?" % (pool['pool_name']))
        print("_________")



# main

if len(sys.argv) == 1:
    print("Usage: python monerowalletcheck.py tags")
    print("example: python monerowalletcheck.py monero APT666")
    sys.exit()
else:
    tags = sys.argv[1:len(sys.argv)]


# for each wallet, connect to each pool and request statistics for the wallet address

print("\n\t\tProcessing wallets \o/")

for wallet in wallet_list:
    if not set(tags).intersection(wallet['tags']):
        continue
    print((wallet['wallet_addr']))
    result_wallet={}
    for pool in pool_list:
        result_wallet.update({pool['pool_name']:{}})
        result_wallet[pool['pool_name']].update({"pool_API_type":pool['pool_API_type']})
        if pool['pool_API_type'] == 'node-cryptonote-pool':
            data=node_cryptonote_pool(pool, wallet)
            if data != None:
                result_wallet[pool['pool_name']].update({'results':data})
            continue
        elif pool['pool_API_type'] == 'nodejs-pool':
            data=nodejs_pool(pool, wallet)
            if data != None:
                result_wallet[pool['pool_name']].update({'results':data})
            continue
        elif pool['pool_API_type'] == 'nanopool':
            data=nanopool(pool, wallet)
            if data != None:
                result_wallet[pool['pool_name']].update({'results':data})
            continue
        elif pool['pool_API_type'] == 'dwarfpool':
            dwarfpool(pool, wallet)
            continue
        else:
            continue
    results.update({wallet['wallet_addr']:result_wallet})

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
