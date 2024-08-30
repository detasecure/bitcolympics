// qr_btf_demo.js

// In a Node.js environment, you would use:
// const QRCrypto = require('./qr_crypto.js');

// For browser environments, ensure qr_crypto.js is loaded before this script

async function runQRBTFDemo() {
    try {
        // Generate QR keys
        console.log("Generating QR keys...");
        const keys = await QRCrypto.generateQRKeys();
        console.log("Private Key:", keys.privateKey);
        console.log("Public Key:", keys.publicKey);

        // Create a sample transaction
        const transactionData = JSON.stringify({
            from: "0x1234...",
            to: "0x5678...",
            amount: "1.5 BTC"
        });
        console.log("\nTransaction Data:", transactionData);

        // Sign the transaction
        console.log("\nSigning transaction...");
        const signature = await QRCrypto.signQRTransaction(keys.privateKey, transactionData);
        console.log("Signature:", signature);

        // Verify the signature
        console.log("\nVerifying signature...");
        const isValid = await QRCrypto.verifyQRSignature(keys.publicKey, transactionData, signature);
        console.log("Signature is valid:", isValid);

    } catch (error) {
        console.error("An error occurred:", error);
    }
}

// Run the demo
runQRBTFDemo();
