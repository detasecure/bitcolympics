import web3
from web3 import Web3
from qr_crypto import generate_qr_keys, sign_qr_transaction, verify_qr_signature

BEVM_RPC_URL = "https://bevm.example.com"  # Replace with actual BEVM RPC URL


class BEVMIntegration:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(BEVM_RPC_URL))

    def create_qr_transaction(self, from_address, to_address, amount, private_key):
        nonce = self.w3.eth.get_transaction_count(from_address)
        tx = {
            'nonce': nonce,
            'to': to_address,
            'value': self.w3.to_wei(amount, 'ether'),
            'gas': 21000,
            'gasPrice': self.w3.eth.gas_price,
            'chainId': self.w3.eth.chain_id
        }

        # Sign the transaction with QR-BTF
        tx_data = Web3.to_json(tx)
        qr_signature = sign_qr_transaction(private_key, tx_data)

        # Add QR signature to transaction data
        tx['qrSignature'] = qr_signature

        # Sign the transaction with Ethereum private key
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)

        # Send the transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.w3.to_hex(tx_hash)

    def verify_qr_transaction(self, tx_hash):
        tx = self.w3.eth.get_transaction(tx_hash)
        tx_data = {k: v for k, v in tx.items() if k != 'qrSignature'}
        return verify_qr_signature(tx['from'], Web3.to_json(tx_data), tx['qrSignature'])


# Demo usage
if __name__ == "__main__":
    bevm_integration = BEVMIntegration()

    # Generate QR keys (in real usage, you'd use the Ethereum private key)
    private_key, public_key = generate_qr_keys()

    # Create a QR transaction
    from_address = "0x1234..."  # Replace with a valid BEVM address
    to_address = "0x5678..."  # Replace with a valid BEVM address
    amount = 0.1  # 0.1 BEVM token
    tx_hash = bevm_integration.create_qr_transaction(from_address, to_address, amount, private_key)
    print(f"Transaction hash: {tx_hash}")

    # Verify the QR transaction
    is_valid = bevm_integration.verify_qr_transaction(tx_hash)
    print(f"Transaction is valid: {is_valid}")