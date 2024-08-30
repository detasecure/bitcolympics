import hashlib
import time
import json
from qr_crypto import generate_qr_keys, sign_qr_transaction, verify_qr_signature

class SimpleBitcoinSimulator:
    def __init__(self):
        self.blockchain = []
        self.current_transactions = []

    def new_block(self, previous_hash):
        block = {
            'index': len(self.blockchain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'previous_hash': previous_hash or self.hash(self.blockchain[-1]),
        }
        self.current_transactions = []
        self.blockchain.append(block)
        return block

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def new_transaction(self, sender, recipient, amount, signature):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'signature': signature,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.blockchain[-1]

class QRBitcoinSimulator(SimpleBitcoinSimulator):
    def new_transaction(self, sender_public_key, recipient, amount, signature):
        transaction_data = json.dumps({
            'sender': sender_public_key,
            'recipient': recipient,
            'amount': amount,
        })
        if verify_qr_signature(sender_public_key, transaction_data, signature):
            return super().new_transaction(sender_public_key, recipient, amount, signature)
        else:
            raise ValueError("Invalid quantum-resistant signature")


# Test the simulator
if __name__ == "__main__":
    # simulator = SimpleBitcoinSimulator()
    # priv, pub = generate_qr_keys()
    # transaction_data = json.dumps({"sender": pub, "recipient": "recipient_address", "amount": 5})
    # signature = sign_qr_transaction(priv, transaction_data)
    # simulator.new_transaction(pub, "recipient_address", 5, signature)
    # simulator.new_block(None)
    # print(json.dumps(simulator.blockchain, indent=2))

    simulator = QRBitcoinSimulator()
    priv, pub = generate_qr_keys()
    transaction_data = json.dumps({"sender": pub, "recipient": "recipient_address", "amount": 5})
    signature = sign_qr_transaction(priv, transaction_data)
    simulator.new_transaction(pub, "recipient_address", 5, signature)
    simulator.new_block(None)
    print(json.dumps(simulator.blockchain, indent=2))
