import subprocess
import json
import os
from dotenv import load_dotenv
from constants import *
from web3 import Web3
from eth_account import Account
from bit import wif_to_key, PrivateKeyTestnet
from bit.network import NetworkAPI

load_dotenv()

def derive_wallets(mnemonic, coin_list):
    
    wallets = {}

    for i in range(len(coin_list)):        
        
        # Get current coin
        coin = coin_list[i]        
       
        # Build command args
        cmd = 'php derive -g --mnemonic="' + mnemonic + '" --cols=address,index,path,privkey,pubkey,pubkeyhash,xprv,xpub --coin=' + coin + ' --numderive=10 --format=json'
    
        # Connect to hd-wallet process, pipe results
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        p_status = p.wait()

        # Get keys in json
        keys = json.loads(output)
        
        # Add coind specific wallets
        wallets[coin] = keys

    return wallets


def priv_key_to_account(coin, priv_key):
    
    if (coin == ETH):
        return Account.privateKeyToAccount(priv_key)
    elif (coin == BTCTEST):
        return PrivateKeyTestnet(priv_key)
    
    return None


def create_tx(coin, account, to, amount):
    
    if (coin == ETH):
        
        gasEstimate = w3.eth.estimateGas({ "from": account.address, "to": to, "value": amount})
            
        return {
            "from": account.address,
            "to": to,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address) 
        }

    elif (coin == BTCTEST):
        
        return PrivateKeyTestnet.prepare_transaction(
            account.address, 
            [(to, amount, BTC)])
    
    return None


def send_tx(coin, account, to, amount):
    
    raw_tx = create_tx(coin, account, to, amount)
    signed_tx = signed_tx = account.sign_transaction(raw_tx)
    
    if (coin == ETH):  
        w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        
    elif (coin == BTCTEST):
        NetworkAPI.broadcast_tx_testnet(signed_tx)
    
    return signed_tx


# Get mnemonic from env vars but use default value if not found
mnemonic = os.getenv('MNEMONIC_HW19', 'improve lion original smoke tail reveal boy ability weird lawsuit immune quality')

# Init w3
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Init coin list
coin_list = [BTC, BTCTEST, ETH]

# Init coins dictionary for fast lookup
coins = derive_wallets(mnemonic, coin_list)

# Bitcoin TestNet addresses
btc_test_from = coins[BTCTEST][0]['address']
btc_test_to = coins[BTCTEST][1]['address']

# Ethereum addresses
eth_from = coins[ETH][0]['address']
eth_to = coins[ETH][1]['address']

# Print instructions
print(f'****************************************')
print(f'Weclcome to HD Wallet Tool \n')
print(f'- version: 1.0.0 \n\n')
print(f'Bitcoin TestNet Addresses')
print(f'- from address: {btc_test_from}')
print(f'- to address: {btc_test_to}\n\n')
print(f'Ethereum Test Addresses')
print(f'- from address: {eth_from}')
print(f'- to address: {eth_to}\n\n')
print(f'****************************************')