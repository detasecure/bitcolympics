import web3
from web3 import Web3
from qr_crypto import generate_qr_keys, sign_qr_transaction, verify_qr_signature

RSK_RPC_URL = "https://public-node.rsk.co"  # Rootstock public node


class RootstockIntegration:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(RSK_RPC_URL))

    def deploy_qr_contract(self, from_address, private_key):
        # Simple smart contract that stores and verifies QR signatures
        contract_source = '''
        pragma solidity ^0.8.0;

        contract QRVerifier {
            mapping(address => bytes) public qrSignatures;

            function storeSignature(bytes memory signature) public {
                qrSignatures[msg.sender] = signature;
            }

            function verifySignature(address signer, bytes memory message, bytes memory signature) public view returns (bool) {
                // In a real implementation, this would call a precompile for QR verification
                // For demo purposes, we'll just check if the stored signature matches
                return keccak256(qrSignatures[signer]) == keccak256(signature);
            }
        }
        '''

        # Compile and deploy the contract (simplified for demo)
        contract_interface = self.w3.eth.contract(abi=[], bytecode=contract_source)
        tx_hash = contract_interface.constructor().transact({'from': from_address})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt.contractAddress

    def store_qr_signature(self, contract_address, from_address, private_key, message):
        contract = self.w3.eth.contract(address=contract_address, abi=[])
        qr_signature = sign_qr_transaction(private_key, message)
        tx_hash = contract.functions.storeSignature(qr_signature).transact({'from': from_address})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return qr_signature

    def verify_qr_signature(self, contract_address, signer, message, signature):
        contract = self.w3.eth.contract(address=contract_address, abi=[])
        return contract.functions.verifySignature(signer, message.encode(), signature).call()


# Demo usage
if __name__ == "__main__":
    rsk_integration = RootstockIntegration()

    # Generate QR keys (in real usage, you'd use the RSK private key)
    private_key, public_key = generate_qr_keys()
    from_address = "0x1234..."  # Replace with a valid RSK address

    # Deploy the QR verifier contract
    contract_address = rsk_integration.deploy_qr_contract(from_address, private_key)
    print(f"Contract deployed at: {contract_address}")

    # Store a QR signature
    message = "Hello, Rootstock!"
    stored_signature = rsk_integration.store_qr_signature(contract_address, from_address, private_key, message)
    print(f"Stored signature: {stored_signature.hex()}")

    # Verify the QR signature
    is_valid = rsk_integration.verify_qr_signature(contract_address, from_address, message, stored_signature)
    print(f"Signature is valid: {is_valid}")