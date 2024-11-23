from web3 import Web3
from eth_account import Account
import hashlib
from typing import Dict
import json

class BlockchainVerifier:
    def __init__(self, ethereum_url: str):
        self.w3 = Web3(Web3.HTTPProvider(ethereum_url))
        self.contract_address = "YOUR_SMART_CONTRACT_ADDRESS"
        self.private_key = "YOUR_PRIVATE_KEY"
        
    def verify_alert(self, alert_data: Dict) -> str:
        """Store alert hash in blockchain for immutable verification"""
        # Create alert hash
        alert_hash = hashlib.sha256(
            json.dumps(alert_data, sort_keys=True).encode()
        ).hexdigest()
        
        # Create transaction
        nonce = self.w3.eth.get_transaction_count(self.w3.eth.account.address)
        
        transaction = {
            'nonce': nonce,
            'gasPrice': self.w3.eth.gas_price,
            'gas': 100000,
            'to': self.contract_address,
            'value': 0,
            'data': self.w3.to_hex(text=alert_hash)
        }
        
        # Sign and send transaction
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, self.private_key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        return self.w3.to_hex(tx_hash) 