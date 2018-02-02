# Monero Pools Wallet Checker
Monero Wallet address checker against popular pools

# description
Python script to test if a Monero Wallet Address has been used to mine on popular pools_file.
list of address are stored in `wallets.json` and list of pools are stored in `pools.json`

# Installation
Just read the code

# Example
From https://www.proofpoint.com/us/threat-insight/post/smominru-monero-mining-botnet-making-millions-operators we take the wallet adresses used by Smominru mining botnet and add them in the wallets.json file, with the same tag (Smominru):

 * 45bbP2muiJHD8Fd5tZyPAfC2RsajyEcsRVVMZ7Tm5qJjdTMprexz6yQ5DVQ1BbmjkMYm9nMid2QSbiGLvvfau7At5V18FzQ
 * 47Tscy1QuJn1fxHiBRjWFtgHmvqkW71YZCQL33LeunfH4rsGEHx5UGTPdfXNJtMMATMz8bmaykGVuDFGWP3KyufBSdzxBb2
 * 43Lm9q14s7GhMLpUsiXY3MH6G67Sn81B5DqmN46u8WnBXNvJmC6FwH3ZMwAmkEB1nHSrujgthFPQeQCFPCwwE7m7TpspYBd

```
$ python monerowalletcheck.py Smominru
	**********************************************
	***      Monero Pools Wallet Checker       ***
	***      Emilien Le Jamtel - CERT-EU       ***
	**********************************************

		Processing wallets \o/
45bbP2muiJHD8Fd5tZyPAfC2RsajyEcsRVVMZ7Tm5qJjdTMprexz6yQ5DVQ1BbmjkMYm9nMid2QSbiGLvvfau7At5V18FzQ
47Tscy1QuJn1fxHiBRjWFtgHmvqkW71YZCQL33LeunfH4rsGEHx5UGTPdfXNJtMMATMz8bmaykGVuDFGWP3KyufBSdzxBb2
43Lm9q14s7GhMLpUsiXY3MH6G67Sn81B5DqmN46u8WnBXNvJmC6FwH3ZMwAmkEB1nHSrujgthFPQeQCFPCwwE7m7TpspYBd

	**********************************************
	***                Results                 ***
	**********************************************
	*            2018-02-02 23:38:56             *
	**********************************************
###############################################################################################
45bbP2muiJHD8Fd5tZyPAfC2RsajyEcsRVVMZ7Tm5qJjdTMprexz6yQ5DVQ1BbmjkMYm9nMid2QSbiGLvvfau7At5V18FzQ
###############################################################################################

*-----------------------------------------------------------------------------------------------*
| Activity found on moneroocean.stream
| Last time seen: 2018-01-24 18:06:36
| Mined coins: 0.0
*-----------------------------------------------------------------------------------------------*

###############################################################################################
47Tscy1QuJn1fxHiBRjWFtgHmvqkW71YZCQL33LeunfH4rsGEHx5UGTPdfXNJtMMATMz8bmaykGVuDFGWP3KyufBSdzxBb2
###############################################################################################

*-----------------------------------------------------------------------------------------------*
| Activity found on minexmr.com
| Last time seen: 2018-02-02 23:37:41
| Mined coins: 2011.324836691644
*-----------------------------------------------------------------------------------------------*

###############################################################################################
43Lm9q14s7GhMLpUsiXY3MH6G67Sn81B5DqmN46u8WnBXNvJmC6FwH3ZMwAmkEB1nHSrujgthFPQeQCFPCwwE7m7TpspYBd
###############################################################################################

*-----------------------------------------------------------------------------------------------*
```

All API requests are saved in a log folder.
