import requests
import json
from qr_crypto import generate_qr_keys, sign_qr_transaction, verify_qr_signature

PWR_CHAIN_RPC_URL = "https://bitcoinplus.pwrlabs.io/broadcast"  # Replace with actual PWR Chain RPC URL


class PWRChainIntegration:
    def __init__(self):
        self.rpc_url = PWR_CHAIN_RPC_URL

    def _rpc_call(self, method, params):
        payload = {
            "jsonrpc": "2.0",
            "id": 21000001,
            "method": method,
            "params": params
        }
        response = requests.post(self.rpc_url, json=payload)
        return response.json()

    def create_qr_transaction(self, from_address, to_address, amount, private_key):
        # Get the nonce for the from_address
        nonce = self._rpc_call("eth_getTransactionCount", [from_address, "latest"])["result"]

        # Prepare the transaction
        transaction = {
            "from": from_address,
            "to": to_address,
            "value": hex(int(amount * 10 ** 18)),  # Convert to Wei
            "gas": "0x5208",  # 21000 gas
            "gasPrice": self._rpc_call("eth_gasPrice", [])["result"],
            "nonce": nonce
        }

        # Sign the transaction with QR-BTF
        transaction_data = json.dumps(transaction)
        qr_signature = sign_qr_transaction(private_key, transaction_data)

        # Add the QR signature to the transaction
        transaction["qrSignature"] = qr_signature

        # Send the transaction
        tx_hash = self._rpc_call("eth_sendRawTransaction", [json.dumps(transaction)])["result"]
        return tx_hash

    def verify_qr_transaction(self, tx_hash):
        # Get the transaction details
        tx = self._rpc_call("eth_getTransactionByHash", [tx_hash])["result"]

        # Verify the QR signature
        transaction_data = json.dumps({k: v for k, v in tx.items() if k != "qrSignature"})
        return verify_qr_signature(tx["from"], transaction_data, tx["qrSignature"])


# Demo usage
if __name__ == "__main__":
    pwr_integration = PWRChainIntegration()

    # Generate QR keys
    private_key, public_key = generate_qr_keys()

    # Create a QR transaction
    from_address = "0x36271f87edecf9d5943720f043c3fb1e3905d7df"  # Replace with a valid address
    to_address = "0x36271f87edecf9d5943720f043c3fb1e3905d7df"  # Replace with a valid address
    amount = 1.0  # 1 PWR token
    tx_hash = pwr_integration.create_qr_transaction(from_address, to_address, amount, private_key)
    print(f"Transaction hash: {tx_hash}")

    # Verify the QR transaction
    is_valid = pwr_integration.verify_qr_transaction(tx_hash)
    print(f"Transaction is valid: {is_valid}")