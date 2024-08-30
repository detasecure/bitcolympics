from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import binascii

def generate_qr_keys():
    key = ECC.generate(curve='P-256')
    private_key = key.export_key(format='PEM')
    public_key = key.public_key().export_key(format='PEM')
    return private_key, public_key

def sign_qr_transaction(private_key, transaction_data):
    key = ECC.import_key(private_key)
    h = SHA256.new(transaction_data.encode())
    signer = DSS.new(key, 'fips-186-3')
    signature = signer.sign(h)
    return binascii.hexlify(signature).decode()

def verify_qr_signature(public_key, transaction_data, signature):
    key = ECC.import_key(public_key)
    h = SHA256.new(transaction_data.encode())
    verifier = DSS.new(key, 'fips-186-3')
    try:
        verifier.verify(h, binascii.unhexlify(signature))
        return True
    except ValueError:
        return False

# Test the functions
if __name__ == "__main__":
    priv, pub = generate_qr_keys()
    print(f"Private Key: {priv}")
    print(f"Public key: {pub}")
    message = "Test transaction"
    signature = sign_qr_transaction(priv, message)
    print(f"Signature: {signature}")
    print(f"Verification: {verify_qr_signature(pub, message, signature)}")
