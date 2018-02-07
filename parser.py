#!/usr/bin/env python
import json
import sys
import datetime

if len(sys.argv) != 2:
    print("Usage: python monero_resultparser.py log_XXX.json")
    sys.exit()
else:
    results_file = sys.argv[1]

print(results_file)

with open(results_file, 'r') as json_file:
    results = json.load(json_file)

def analyse_data(data):
    parsed_data = {}
    if data['pool_API_type'] == 'node-cryptonote-pool' and 'results' in data.keys():
        if 'stats' in data['results'].keys():
            parsed_data.update({'activity':1})
            mined_coins=0
            if 'balance' in data['results']['stats'].keys():
                mined_coins=float(data['results']['stats']['balance']) + float(data['results']['stats']['paid'])
                mined_coins = mined_coins / 1000000000000
            parsed_data.update({'mined_coins':mined_coins,'last_activity':data['results']['stats']['lastShare']})
            return parsed_data
        else:
            parsed_data.update({'activity':0})
            return parsed_data
    elif data['pool_API_type'] == 'nodejs-pool' and 'results' in data.keys():
        if data['results']['lastHash'] not in (0, None, "") :
            parsed_data.update({'activity':1})
            mined_coins=float(data['results']['amtPaid']) + float(data['results']['amtDue'])
            mined_coins = mined_coins / 1000000000000
            parsed_data.update({'mined_coins':mined_coins,'last_activity':data['results']['lastHash']})
            return parsed_data
        else:
            parsed_data.update({'activity':0})
            return parsed_data
    elif data['pool_API_type'] == 'nanopool' and 'results' in data.keys():
        if 'data' in data['results']['account'].keys() :
            parsed_data.update({'activity':1})
            balance=data['results']['account']['data']['userParams']['balance']
            last_activity=data['results']['account']['data']['shareRateHistory'][0]['hour']*3600
            payments = float(0)
            for payment in data['results']['payments']['data']:
                payments = float(payments) + float(payment['amount'])
            mined_coins = float(payments) + float(balance)
            parsed_data.update({'mined_coins':mined_coins,'last_activity':last_activity})
            return parsed_data
        else:
            parsed_data.update({'activity':0})
            return parsed_data
    else:
        parsed_data.update({'activity':0})
        return parsed_data

print("\n\t**********************************************")
print("\t***                Results                 ***")
print("\t**********************************************")
print("\t*            %s             *" % (results['date'].split('.')[0]))
print("\t**********************************************")

for wallet in results['results'].keys():
    print("###############################################################################################")
    print(wallet)
    print("###############################################################################################\n")
    for pool, pool_data in results['results'][wallet].items():
        data = analyse_data(pool_data)
        if data['activity'] == 1:
            print("*-----------------------------------------------------------------------------------------------*")
            print("| Activity found on %s" % (pool))
            print("| Last time seen: %s" % (datetime.datetime.fromtimestamp(int(data['last_activity']))))
            print("| Mined coins: %s" % (data['mined_coins']))
    print("*-----------------------------------------------------------------------------------------------*\n")
