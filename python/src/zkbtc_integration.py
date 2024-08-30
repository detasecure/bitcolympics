import requests
import json
from qr_crypto import generate_qr_keys, sign_qr_transaction, verify_qr_signature

ZKBTC_RPC_URL = "https://zkbtc.example.com/rpc"  # Replace with actual zkBTC RPC URL


class ZKBTCIntegration:
    def __init__(self):
        self.rpc_url = ZKBTC_RPC_URL

    def _rpc_call(self, method, params):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        response = requests.post(self.rpc_url, json=payload)
        return response.json()

    def create_qr_zk_transaction(self, from_address, to_address, amount, private_key):
        # Prepare the transaction
        transaction = {
            "from": from_address,
            "to": to_address,
            "amount": amount,
            "nonce": self._rpc_call("get_nonce", [from_address])["result"]
        }

        # Sign the transaction with QR-BTF
        transaction_data = json.dumps(transaction)
        qr_signature = sign_qr_transaction(private_key, transaction_data)

        # Create a zero-knowledge proof of the transaction
        zk_proof = self._rpc_call("create_zk_proof", [transaction, qr_signature])["result"]

        # Send the transaction with ZK proof
        tx_hash = self._rpc_call("send_zk_transaction", [zk_proof])["result"]
        return tx_hash

    def verify_qr_zk_transaction(self, tx_hash):
        # Get the transaction details and ZK proof
        tx_data = self._rpc_call("get_zk_transaction", [tx_hash])["result"]

        # Verify the ZK proof
        is_valid_zk = self._rpc_call("verify_zk_proof", [tx_data["zk_proof"]])["result"]

        # If ZK proof is valid, verify the QR signature
        if is_valid_zk:
            return verify_qr_signature(tx_data["from"], json.dumps(tx_data["transaction"]), tx_data["qr_signature"])
        return False


# Demo usage
if __name__ == "__main__":
    zkbtc_integration = ZKBTCIntegration()

    # Generate QR keys
    private_key, public_key = generate_qr_keys()

    # Create a QR-ZK transaction
    from_address = "zk1234..."  # Replace with a valid zkBTC address
    to_address = "zk5678..."  # Replace with a valid zkBTC address
    amount = 0.1  # 0.1 BTC
    tx_hash = zkbtc_integration.create_qr_zk_transaction(from_address, to_address, amount, private_key)
    print(f"Transaction hash: {tx_hash}")

    # Verify the QR-ZK transaction
    is_valid = zkbtc_integration.verify_qr_zk_transaction(tx_hash)
    print(f"Transaction is valid: {is_valid}")