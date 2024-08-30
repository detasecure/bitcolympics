from flask import Flask, request, jsonify, render_template_string
from qr_crypto import generate_qr_keys, sign_qr_transaction, verify_qr_signature
from bitcoin_simulator import QRBitcoinSimulator
import json

app = Flask(__name__)
simulator = QRBitcoinSimulator()

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR-BTF Demo</title>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script>
        async function generateKeys() {
            const response = await axios.post('/generate_keys');
            document.getElementById('publicKey').value = response.data.public_key;
            document.getElementById('privateKey').value = response.data.private_key;
        }

        async function createTransaction() {
            const transaction = {
                sender: document.getElementById('publicKey').value,
                recipient: document.getElementById('recipient').value,
                amount: document.getElementById('amount').value
            };
            const privateKey = document.getElementById('privateKey').value;
            const response = await axios.post('/create_transaction', { transaction, privateKey });
            document.getElementById('result').innerText = JSON.stringify(response.data, null, 2);
        }

        async function getBlockchain() {
            const response = await axios.get('/blockchain');
            document.getElementById('result').innerText = JSON.stringify(response.data, null, 2);
        }
    </script>
</head>
<body>
    <h1>QR-BTF Demo</h1>
    <button onclick="generateKeys()">Generate Keys</button><br>
    Public Key: <input id="publicKey" size="50"><br>
    Private Key: <input id="privateKey" size="50"><br>
    Recipient: <input id="recipient"><br>
    Amount: <input id="amount" type="number"><br>
    <button onclick="createTransaction()">Create Transaction</button><br>
    <button onclick="getBlockchain()">View Blockchain</button><br>
    <pre id="result"></pre>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/generate_keys', methods=['POST'])
def api_generate_keys():
    private_key, public_key = generate_qr_keys()
    return jsonify({'private_key': private_key, 'public_key': public_key})

@app.route('/create_transaction', methods=['POST'])
def api_create_transaction():
    data = request.json
    transaction = data['transaction']
    private_key = data['privateKey']
    transaction_data = json.dumps(transaction)
    signature = sign_qr_transaction(private_key.encode(), transaction_data)
    try:
        simulator.new_transaction(transaction['sender'], transaction['recipient'], float(transaction['amount']), signature)
        simulator.new_block(None)
        return jsonify({'status': 'success', 'message': 'Transaction added to blockchain'})
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/blockchain', methods=['GET'])
def api_get_blockchain():
    return jsonify(simulator.blockchain)

if __name__ == '__main__':
    app.run(debug=True)