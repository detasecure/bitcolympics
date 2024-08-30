// qr_crypto.js

// Check if we're in a Node.js environment and use a polyfill if necessary
if (typeof window === 'undefined') {
    global.crypto = require('crypto').webcrypto;
}

class QRCrypto {
    static async generateQRKeys() {
        const keyPair = await crypto.subtle.generateKey(
            {
                name: "ECDSA",
                namedCurve: "P-256"
            },
            true,
            ["sign", "verify"]
        );

        const privateKey = await crypto.subtle.exportKey("pkcs8", keyPair.privateKey);
        const publicKey = await crypto.subtle.exportKey("spki", keyPair.publicKey);

        return {
            privateKey: this._arrayBufferToBase64(privateKey),
            publicKey: this._arrayBufferToBase64(publicKey)
        };
    }

    static async signQRTransaction(privateKeyBase64, transactionData) {
        const privateKey = await crypto.subtle.importKey(
            "pkcs8",
            this._base64ToArrayBuffer(privateKeyBase64),
            {
                name: "ECDSA",
                namedCurve: "P-256"
            },
            false,
            ["sign"]
        );

        const signature = await crypto.subtle.sign(
            {
                name: "ECDSA",
                hash: {name: "SHA-256"},
            },
            privateKey,
            new TextEncoder().encode(transactionData)
        );

        return this._arrayBufferToBase64(signature);
    }

    static async verifyQRSignature(publicKeyBase64, transactionData, signatureBase64) {
        const publicKey = await crypto.subtle.importKey(
            "spki",
            this._base64ToArrayBuffer(publicKeyBase64),
            {
                name: "ECDSA",
                namedCurve: "P-256"
            },
            false,
            ["verify"]
        );

        return await crypto.subtle.verify(
            {
                name: "ECDSA",
                hash: {name: "SHA-256"},
            },
            publicKey,
            this._base64ToArrayBuffer(signatureBase64),
            new TextEncoder().encode(transactionData)
        );
    }

    static _arrayBufferToBase64(buffer) {
        let binary = '';
        const bytes = new Uint8Array(buffer);
        for (let i = 0; i < bytes.byteLength; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return btoa(binary);
    }

    static _base64ToArrayBuffer(base64) {
        const binaryString = atob(base64);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        return bytes.buffer;
    }
}

// Export the class for Node.js environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QRCrypto;
}
