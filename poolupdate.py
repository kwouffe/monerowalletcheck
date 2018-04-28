#!/usr/bin/env python
import requests
import json
import datetime
import sys
import os
import ui
from pyjsparser import PyJsParser

#disable SSL warning
requests.packages.urllib3.disable_warnings()

now = datetime.datetime.now().replace(microsecond=0)

results={}

print("\t**********************************************")
print("\t***      Monero Pools Update               ***")
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



def add_pool_ui(json_file):
    pool_list = open_pool_list(json_file)
    new_pool={}
    new_pool['pool_API_url'] = ''
    new_pool['pool_mining_urls'] = []
    new_pool['pool_name'] = ui.ask_string("Enter new pool name")
    pool_type_list = ["node-cryptonote-pool","nodejs-pool","other"]
    new_pool['pool_API_type'] = ui.ask_choice("API type ?", pool_type_list)
    new_pool['config_file'] = ui.ask_string("Configuration file URL (usually config.js OR global.js) ?")
    new_pool=get_config(new_pool)
    if new_pool['pool_API_url'] == '':
        new_pool['pool_API_url'] = ui.ask_string("Impossible to get API URL, please provide manually for next attempt")
        new_pool=get_config(new_pool)
    print("*** Output ***")
    print(json.dumps(new_pool, indent=4))
    yesno = ["no","yes"]
    accept = ui.ask_choice("Do you want to add to the pool list ?", yesno)
    if accept == "yes":
        pool_list.append(new_pool)
        output={}
        output["pools"] = pool_list
        with open(json_file, 'w') as pouet:
            pouet.write(json.dumps(output, indent=4))
            print("Done ...")
    else:
        print("OK nevermind ...")


def get_config(pool):
    if pool['pool_API_type'] == 'node-cryptonote-pool':
        try:
            response = requests.get(pool['config_file'], stream=True)
            if response.status_code == 200:
                config = response.text
                p = PyJsParser()
                config_json=(p.parse(config))
                for entry in config_json['body']:
                    if entry['type'] == 'VariableDeclaration' :
                        if entry['declarations'][0]['id']['name'] == "api":
                            pool['pool_API_url'] = entry['declarations'][0]['init']['value']
                        elif "poolHost" in entry['declarations'][0]['id']['name']:
                            if entry['declarations'][0]['init']['value'] not in pool['pool_mining_urls']:
                                pool['pool_mining_urls'].append(entry['declarations'][0]['init']['value'])
            return pool
        except:
            print("error getting the provided URL for config file")
            return pool
    elif pool['pool_API_type'] == 'nodejs-pool':
        try:
            response = requests.get(pool['config_file'], stream=True)
            if response.status_code == 200:
                config = response.text.splitlines()
                for line in config:
                    if 'api_url' in line:
                        pool['pool_API_url'] = line[line.index("api_url")+11:line.index(",")-1]
        except:
            print("error getting the provided URL for config file")
        try:
            poolports_url = pool['pool_API_url'] + "/pool/ports"
            response = requests.get(poolports_url)
            if response.status_code == 200:
                poolports = json.loads(response.text)
                for pplns in poolports['pplns']:
                    if pplns['host']['hostname'] not in pool['pool_mining_urls']:
                        pool['pool_mining_urls'].append(pplns['host']['hostname'])
                for pplns in poolports['global']:
                    if pplns['host']['hostname'] not in pool['pool_mining_urls']:
                        pool['pool_mining_urls'].append(pplns['host']['hostname'])
        except:
            print("error getting the list of poolHost via API")
        return pool
    else:
        return pool

def update_pool_list(json_file):
    pool_list = open_pool_list(json_file)
    updated_pool_list = []
    for pool in pool_list:
        new_pool = get_config(pool)
        updated_pool_list.append(new_pool)
    #print(json.dumps(updated_pool_list, indent=4))
    output={}
    output["pools"] = updated_pool_list
    with open(json_file, 'w') as pouet:
        pouet.write(json.dumps(output, indent=4))
        print("Done ...")
    #print(diff(pool_list,updated_pool_list))

def man():
    print("Usage: python poolupdate.py option file.json")
    print("Possible options:")
    print("\tupdate\t\tUpdate the full list (API and mining URLs)")
    print("\tadd\t\tAdd a pool to the list")

def open_pool_list(json_file):
    # open pools and wallets JSON files
    with open(json_file, 'r') as pools_file:
            pools = json.load(pools_file)
    return pools["pools"]

# main
def main():
    if len(sys.argv) != 3:
        man()
        sys.exit()
    elif sys.argv[1] not in ['update', 'add']:
        man()
        sys.exit()
    else:
        json_file = sys.argv[2]
    if sys.argv[1] == 'update':
        update_pool_list(json_file)
    else:
        add_pool_ui(json_file)


main()
