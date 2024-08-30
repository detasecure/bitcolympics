import requests
import json
from qr_crypto import generate_qr_keys, sign_qr_transaction, verify_qr_signature

PARTICLE_API_URL = "https://api.particle.network"  # Replace with actual Particle Network API URL
PARTICLE_PROJECT_ID = "your_project_id"
PARTICLE_PROJECT_SECRET = "your_project_secret"


class ParticleNetworkIntegration:
    def __init__(self):
        self.api_url = PARTICLE_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "X-Project-Id": PARTICLE_PROJECT_ID,
            "X-Project-Secret": PARTICLE_PROJECT_SECRET
        }

    def _api_call(self, endpoint, method, data):
        url = f"{self.api_url}/{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data)
        return response.json()

    def create_wallet(self):
        data = {
            "chain_name": "solana",  # or "ethereum", depending on your use case
            "wallet_type": "mnemonic"
        }
        result = self._api_call("wallet/create", "POST", data)
        return result['wallet_address'], result['private_key']

    def send_qr_transaction(self, from_address, to_address, amount, private_key):
        # Prepare transaction data
        tx_data = {
            "from": from_address,
            "to": to_address,
            "amount": str(amount),
            "chain_name": "solana"  # or "ethereum", depending on your use case
        }

        # Sign transaction with QR-BTF
        qr_signature = sign_qr_transaction(private_key, json.dumps(tx_data))

        # Add QR signature to transaction data
        tx_data["qr_signature"] = qr_signature.hex()

        # Send transaction through Particle Network
        result = self._api_call("transaction/send", "POST", tx_data)
        return result['tx_hash']

    def verify_qr_transaction(self, tx_hash):
        # Get transaction details
        tx_data = self._api_call(f"transaction/{tx_hash}", "GET", {})

        # Extract QR signature and verify
        qr_signature = bytes.fromhex(tx_data['qr_signature'])
        tx_data_without_signature = {k: v for k, v in tx_data.items() if k != 'qr_signature'}
        return verify_qr_signature(tx_data['from'], json.dumps(tx_data_without_signature), qr_signature)


# Demo usage
if __name__ == "__main__":
    particle_integration = ParticleNetworkIntegration()

    # Create a wallet
    address, private_key = particle_integration.create_wallet()
    print(f"Created wallet with address: {address}")

    # Generate QR keys (in a real scenario, you might use the wallet's private key)
    qr_private_key, qr_public_key = generate_qr_keys()

    # Send a QR transaction
    to_address = "FakEbT4CkhuVmAYKu2TX5EK5EbXnEzLkVxXQ6my56UZC"  # Replace with a valid address
    amount = 0.01
    tx_hash = particle_integration.send_qr_transaction(address, to_address, amount, qr_private_key)
    print(f"Transaction hash: {tx_hash}")

    # Verify the QR transaction
    is_valid = particle_integration.verify_qr_transaction(tx_hash)
    print(f"Transaction is valid: {is_valid}")