# Monero Pools Wallet Checker
Monero Wallet address checker against popular pools.

# description
Python scripts to test if a Monero Wallet Address has been used to mine on popular pools.
Now split into 2 scripts:
 - checker.py for grabbing data and generating json output_account
 - parser.py to analyse the output of checker.py

list of address are stored in `wallets.json` and list of pools are stored in `pools.json`

# Installation
run it and read errors for missing modules

# Example
From https://www.proofpoint.com/us/threat-insight/post/smominru-monero-mining-botnet-making-millions-operators we take the wallet adresses used by Smominru mining botnet and add them in the wallets.json file, with the same tag (Smominru):

 * 45bbP2muiJHD8Fd5tZyPAfC2RsajyEcsRVVMZ7Tm5qJjdTMprexz6yQ5DVQ1BbmjkMYm9nMid2QSbiGLvvfau7At5V18FzQ
 * 47Tscy1QuJn1fxHiBRjWFtgHmvqkW71YZCQL33LeunfH4rsGEHx5UGTPdfXNJtMMATMz8bmaykGVuDFGWP3KyufBSdzxBb2
 * 43Lm9q14s7GhMLpUsiXY3MH6G67Sn81B5DqmN46u8WnBXNvJmC6FwH3ZMwAmkEB1nHSrujgthFPQeQCFPCwwE7m7TpspYBd

`$ python checker.py Smominru
	**********************************************
	***      Monero Pools Wallet Checker       ***
	***      Emilien Le Jamtel - CERT-EU       ***
	**********************************************

		Processing wallets \o/
45bbP2muiJHD8Fd5tZyPAfC2RsajyEcsRVVMZ7Tm5qJjdTMprexz6yQ5DVQ1BbmjkMYm9nMid2QSbiGLvvfau7At5V18FzQ
47Tscy1QuJn1fxHiBRjWFtgHmvqkW71YZCQL33LeunfH4rsGEHx5UGTPdfXNJtMMATMz8bmaykGVuDFGWP3KyufBSdzxBb2
43Lm9q14s7GhMLpUsiXY3MH6G67Sn81B5DqmN46u8WnBXNvJmC6FwH3ZMwAmkEB1nHSrujgthFPQeQCFPCwwE7m7TpspYBd


	**********************************************
	***                 Done                   ***
	**********************************************

	 run $python parser.py log_2018-02-07-11-44-42.json to analyse output

   $ python parser.py log_2018-02-07-11-44-42.json
   log_2018-02-07-11-44-42.json

   	**********************************************
   	***                Results                 ***
   	**********************************************
   	*            2018-02-07 11:45:52             *
   	**********************************************
   ###############################################################################################
   45bbP2muiJHD8Fd5tZyPAfC2RsajyEcsRVVMZ7Tm5qJjdTMprexz6yQ5DVQ1BbmjkMYm9nMid2QSbiGLvvfau7At5V18FzQ
   ###############################################################################################

   *-----------------------------------------------------------------------------------------------*
   | Activity found on moneroocean.stream
   | Last time seen: 2018-01-24 18:06:36
   | Mined coins: 0.0
   *-----------------------------------------------------------------------------------------------*
   | Activity found on xmrpool.eu
   | Last time seen: 2017-10-18 11:09:16
   | Mined coins: 0
   *-----------------------------------------------------------------------------------------------*

   ###############################################################################################
   47Tscy1QuJn1fxHiBRjWFtgHmvqkW71YZCQL33LeunfH4rsGEHx5UGTPdfXNJtMMATMz8bmaykGVuDFGWP3KyufBSdzxBb2
   ###############################################################################################

   *-----------------------------------------------------------------------------------------------*
   | Activity found on monero.crypto-pool.fr
   | Last time seen: 2018-02-07 11:33:30
   | Mined coins: 569.132981357243
   *-----------------------------------------------------------------------------------------------*
   | Activity found on minexmr.com
   | Last time seen: 2018-02-07 11:44:33
   | Mined coins: 2011.34155733054
   *-----------------------------------------------------------------------------------------------*

   ###############################################################################################
   43Lm9q14s7GhMLpUsiXY3MH6G67Sn81B5DqmN46u8WnBXNvJmC6FwH3ZMwAmkEB1nHSrujgthFPQeQCFPCwwE7m7TpspYBd
   ###############################################################################################

   *-----------------------------------------------------------------------------------------------*
   | Activity found on supportXMR.com
   | Last time seen: 2018-02-07 11:45:25
   | Mined coins: 18.701311547858
   *-----------------------------------------------------------------------------------------------*


`
