# Secure Steganography App

This project implements a secure steganography application that allows users to hide messages within images using AES encryption and the least significant bit (LSB) method. The application is built using Streamlit, providing a user-friendly interface for both encryption and decryption processes.

## Project Structure

```
secure-steganography-app
├── src
│   ├── app.py               # Main entry point for the Streamlit web application
│   ├── stego.py             # Functions for AES key generation, message encryption, and hiding messages in images
│   ├── stego_decrypt.py     # Functions for loading the AES key, decrypting messages, and extracting hidden messages from images
│   └── utils
│       └── __init__.py      # Placeholder for utility functions or classes
├── assets
│   └── .gitkeep             # Keeps the assets directory tracked by Git
├── uploads
│   └── .gitkeep             # Keeps the uploads directory tracked by Git
├── requirements.txt          # Lists the dependencies required for the project
├── .gitignore                # Specifies files and directories to be ignored by Git
└── README.md                 # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd secure-steganography-app
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run src/app.py
   ```

## Usage

- **Encrypt a Message:**
  - Enter the secret message you want to hide.
  - Upload an image file (e.g., JPEG).
  - Click the button to encrypt the message and hide it in the image.
  - Download the encoded image.

- **Decrypt a Message:**
  - Upload the encoded image.
  - Click the button to extract and decrypt the hidden message.

## Dependencies

- Streamlit
- OpenCV
- PyCryptodome

## License

This project is licensed under the MIT License. See the LICENSE file for more details.