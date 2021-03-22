import subprocess
import json
from constants import *


# from dotenv import load_dotenv

# Import web3 libraries
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account

#  Connect to web3
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# Enable PoA Ethereum transaction
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


# Need to adjust for PC and for errors i was getting

# command = 'php ../../../../Blockchain-Tools/hd-wallet-derive/hd-wallet-derive.php -g --mnemonic="busy gospel maid grocery mean solve usual blouse lumber tail agent crew" --cols=path,address,privkey,pubkey --format=json'


# p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
# (output, err) = p.communicate()
# p_status = p.wait()

# keys = json.loads(output)
# print(output)

test_mnemonic="busy gospel maid grocery mean solve usual blouse lumber tail agent crew"
mnemonic=test_mnemonic

def derive_wallets(mnemonic, coin, depth): 
    command = f'php ../../../../Blockchain-Tools/hd-wallet-derive/hd-wallet-derive.php -g --mnemonic="{mnemonic}" ----cols=all --coin={coin} --numderive={depth} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()

    # keys = 
    return json.loads(output)

eth_json=derive_wallets(test_mnemonic,ETH,3 )

coins={'ETH':derive_wallets(test_mnemonic,ETH,3), 'BTCTEST':derive_wallets(test_mnemonic,ETH,3)}
print(coins)


def priv_key_to_account(coin, priv_key):
    if coin==ETH:
        return Account.privateKeyToAccount(priv_key)
    if coin==BTCTEST:
        return PrivateKeyTestnet(priv_key)
    

def create_raw_tx(coin, account, recipient, amount):
    if coin==ETH:
        value = w3.toWei(amount, "ether") # convert ether to wei
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
        }
    if coin==BTCTEST:
        PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])

    
    
def send_tx(coin, account, recipient, amount):
    if coin==ETH:
        raw_tx = create_raw_tx(account, recipient, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()
    if coin==BTCTEST:
        raw_tx = create_raw_tx(coin, account, to, amount)
        signed_tx = account.sign_transaction(tx)
        return NetworkAPI.broadcast_tx_testnet(signed)

