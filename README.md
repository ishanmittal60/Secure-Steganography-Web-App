# Secure Steganography App (ECC + LSB)

This project hides secret text inside images using least significant bit (LSB) steganography, and protects the message content with Elliptic Curve Cryptography (ECC). The UI is built with Streamlit for simple encryption and decryption.

The encryption design is hybrid:
- ECC is used for key agreement (ECDH).
- The derived shared key is used with AES-GCM for fast, authenticated encryption.
- The encrypted payload is embedded into the image using LSB.

## Project Structure

```
secure-steganography-app
├── src
│   ├── app.py               # Streamlit UI and user flow
│   ├── stego.py             # ECC keypair, ECDH, AES-GCM encryption, LSB hide
│   ├── stego_decrypt.py     # ECC private key load, ECDH, AES-GCM decrypt, LSB extract
│   └── utils
│       └── __init__.py      # Placeholder for utilities
├── assets
│   └── .gitkeep             # Keeps the assets directory tracked by Git
├── uploads
│   └── .gitkeep             # Keeps the uploads directory tracked by Git
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore rules
└── README.md                # Project documentation
```

## Quick Start (Windows PowerShell)

### 1) Create and activate a virtual environment

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

If activation is blocked, run this once in PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
```

### 3) Run the Streamlit app

```powershell
streamlit run src/app.py
```

If you see a module error, ensure you are using the venv:

```powershell
& .\.venv\Scripts\python.exe -m streamlit run src/app.py
```

## How It Works (Detailed)

### A) ECC keypair creation

- When you first encrypt a message, the app generates an ECC keypair:
   - `ecc_private_key.pem` (private key, must be kept secret)
   - `ecc_public_key.pem` (public key, safe to share)
- The curve used is `secp256r1` (also known as P-256), a widely supported NIST curve.

### B) ECDH (Elliptic Curve Diffie-Hellman)

- For each encryption, the app creates a fresh ephemeral ECC keypair.
- It performs ECDH using:
   - Ephemeral private key (new each time)
   - Receiver public key (stored in `ecc_public_key.pem`)
- This produces a shared secret that both sides can compute, but attackers cannot.

### C) Key derivation (HKDF)

- The raw shared secret is not used directly as a key.
- HKDF (HMAC-based Key Derivation Function) derives a 32-byte AES key.
- A random 16-byte salt is included to make derived keys unique.

### D) AES-GCM encryption

- The derived key encrypts the message using AES-GCM:
   - AES = Advanced Encryption Standard
   - GCM = Galois/Counter Mode (provides confidentiality + integrity)
- AES-GCM requires a 12-byte nonce (random each time).
- Output includes ciphertext plus authentication tag.

### E) Payload format (binary layout)

The encrypted payload is serialized and then Base64-encoded before embedding:

```
[2 bytes: ephemeral public key length]
[N bytes: ephemeral public key (DER)]
[16 bytes: salt]
[12 bytes: nonce]
[ciphertext + tag]
```

### F) LSB steganography (image hiding)

- The Base64 string is converted to bits.
- Each bit is stored in the least significant bit of the red channel.
- A fixed end marker `1111111111111110` is appended to stop extraction.

### G) Decryption flow

1. Extract bits from the image until the end marker is found.
2. Convert bits back to a Base64 string.
3. Decode the payload and rebuild components.
4. Use private key + ephemeral public key to compute shared secret.
5. Derive AES key with HKDF and decrypt using AES-GCM.

## Usage (Step-by-step)

### Encrypt and Hide

1. Open the app.
2. Enter a secret message.
3. Upload an image (PNG or JPG).
4. Click **Encrypt and Hide Message**.
5. Download:
    - Encoded image (`encoded_image.png`)
    - Public key (`ecc_public_key.pem`)
    - Private key (`ecc_private_key.pem`)

### Decrypt and Extract

1. Open the app.
2. Upload the encoded image.
3. Upload the private key (`ecc_private_key.pem`).
4. Click **Decrypt and Extract Message**.

## File Outputs

- `encoded_image.png`: Image containing the hidden payload.
- `ecc_public_key.pem`: ECC public key (shareable).
- `ecc_private_key.pem`: ECC private key (secret).

## Dependencies

- streamlit
- opencv-python-headless
- cryptography
- Pillow

## Common Errors and Fixes

### ModuleNotFoundError: No module named 'cryptography'

Make sure you installed dependencies in the active venv:

```powershell
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Streamlit cannot find app.py

Use the correct path from the project root:

```powershell
streamlit run src/app.py
```

## Security Notes

- Keep `ecc_private_key.pem` safe. Anyone with it can decrypt.
- Do not embed the private key into the image or share it publicly.
- LSB steganography is not robust against heavy compression or resizing.

## License

MIT