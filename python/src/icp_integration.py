import requests
import json
from qr_crypto import generate_qr_keys, sign_qr_transaction, verify_qr_signature

ICP_API_URL = "https://ic0.app"  # Replace with actual ICP API endpoint


class InternetComputerIntegration:
    def __init__(self):
        self.api_url = ICP_API_URL

    def _api_call(self, canister_id, method, args):
        payload = {
            "canister_id": canister_id,
            "method_name": method,
            "arg": json.dumps(args).encode().hex()
        }
        response = requests.post(f"{self.api_url}/api/v2/canister/{canister_id}/call", json=payload)
        return response.json()

    def deploy_qr_canister(self):
        # In a real implementation, you would deploy a Motoko or Rust canister
        # For this demo, we'll simulate canister deployment
        canister_id = "rrkah-fqaaa-aaaaa-aaaaq-cai"  # Example canister ID
        print(f"Deployed QR canister with ID: {canister_id}")
        return canister_id

    def store_qr_signature(self, canister_id, public_key, message, private_key):
        qr_signature = sign_qr_transaction(private_key, message)
        args = {
            "public_key": public_key,
            "message": message,
            "signature": qr_signature.hex()
        }
        result = self._api_call(canister_id, "store_signature", args)
        return result

    def verify_qr_signature(self, canister_id, public_key, message, signature):
        args = {
            "public_key": public_key,
            "message": message,
            "signature": signature
        }
        result = self._api_call(canister_id, "verify_signature", args)
        return result.get("result", False)


# Demo usage
if __name__ == "__main__":
    ic_integration = InternetComputerIntegration()

    # Deploy QR canister
    canister_id = ic_integration.deploy_qr_canister()

    # Generate QR keys
    private_key, public_key = generate_qr_keys()

    # Store a QR signature
    message = "Hello, Internet Computer!"
    store_result = ic_integration.store_qr_signature(canister_id, public_key, message, private_key)
    print(f"Store result: {store_result}")

    # Verify the QR signature
    signature = sign_qr_transaction(private_key, message)
    is_valid = ic_integration.verify_qr_signature(canister_id, public_key, message, signature.hex())
    print(f"Signature is valid: {is_valid}")