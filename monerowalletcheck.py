#!/usr/bin/env python
import requests
import json
import re
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

log_directory = "log_" + str(now)

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

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
        if 'stats' in output.keys():
            mined_coins=float(output['stats']['balance']) + float(output['stats']['paid'])
            mined_coins = mined_coins / 1000000000000
            data={"last_activity":output['stats']['lastShare'],"hashrate":output['stats']['hashrate'],"mined_coins":mined_coins}
            logfile = log_wallet + "/" + pool['pool_name'] + ".json"
            with open(logfile, 'w') as log:
                log.write(json.dumps(output, indent=4))
            return data
    except:
        return None

def nodejs_pool(pool, wallet):
    try:
        url = pool['pool_API_url'] + 'miner/' + wallet['wallet_addr'] + '/stats'
        resp = requests.get(url, timeout=13)
        output = json.loads(resp.text)
        if output['lastHash'] not in (0, None, "") :
            mined_coins=float(output['amtPaid']) + float(output['amtDue'])
            mined_coins = mined_coins / 1000000000000
            data={"last_activity":output['lastHash'],"mined_coins":mined_coins}
            logfile = log_wallet + "/" + pool['pool_name'] + ".json"
            with open(logfile, 'w') as log:
                log.write(json.dumps(output, indent=4))
            return data
    except:
        return None

def nanopool(pool, wallet):
    try:
        url = pool['pool_API_url'] + 'load_account/' + wallet['wallet_addr']
        resp = requests.get(url, timeout=13)
        output_account = json.loads(resp.text)
        if 'data' in output_account.keys() :
            balance=output_account['data']['userParams']['balance']
            last_activity=output_account['data']['shareRateHistory'][0]['hour']*3600
            url = pool['pool_API_url'] + 'payments/' + wallet['wallet_addr']
            resp = requests.get(url, timeout=13)
            output_payments = json.loads(resp.text)
            payments = float(0)
            for payment in output_payments['data']:
                payments = float(payments) + float(payment['amount'])
            mined_coins = float(payments) + float(balance)
            data={"last_activity":last_activity,"mined_coins":mined_coins}
            logfile_account = log_wallet + "/" + pool['pool_name'] + ".account.json"
            with open(logfile_account, 'w') as log_acc:
                log_acc.write(json.dumps(output_account, indent=4))
            logfile_payments = log_wallet + "/" + pool['pool_name'] + ".payments.json"
            with open(logfile_payments, 'w') as log_pay:
                log_pay.write(json.dumps(output_payments, indent=4))
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
    log_wallet = log_directory + "/" + wallet['wallet_addr']
    if not os.path.exists(log_wallet):
        os.makedirs(log_wallet)
    result_wallet={}
    for pool in pool_list:
        if pool['pool_API_type'] == 'node-cryptonote-pool':
            data=node_cryptonote_pool(pool, wallet)
            if data != None:
                result_wallet.update({pool['pool_name']:data})
            continue
        elif pool['pool_API_type'] == 'nodejs-pool':
            data=nodejs_pool(pool, wallet)
            if data != None:
                result_wallet.update({pool['pool_name']:data})
            continue
        elif pool['pool_API_type'] == 'nanopool':
            data=nanopool(pool, wallet)
            if data != None:
                result_wallet.update({pool['pool_name']:data})
            continue
        elif pool['pool_API_type'] == 'dwarfpool':
            dwarfpool(pool, wallet)
            continue
        else:
            continue
    results[wallet['wallet_addr']]=result_wallet

print("\n\t**********************************************")
print("\t***                Results                 ***")
print("\t**********************************************")
print("\t*            %s             *" % (now))
print("\t**********************************************")

for wallet in results.keys():
    print("###############################################################################################")
    print(wallet)
    print("###############################################################################################\n")
    for key, value in results[wallet].items():
        print("*-----------------------------------------------------------------------------------------------*")
        print("| Activity found on %s" % (key))
        print("| Last time seen: %s" % (datetime.datetime.fromtimestamp(int(value['last_activity']))))
        print("| Mined coins: %s" % (value['mined_coins']))
    print("*-----------------------------------------------------------------------------------------------*\n")
