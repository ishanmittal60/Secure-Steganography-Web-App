# filepath: secure-steganography-app/src/stego_decrypt.py
import cv2
import base64
from Crypto.Cipher import AES

# Load AES key
def load_key():
    with open("aes_key.key", "rb") as f:
        return f.read()

# Decrypt the message using AES
def decrypt_message(encrypted_text, key):
    raw_data = base64.b64decode(encrypted_text)
    nonce, tag, ciphertext = raw_data[:16], raw_data[16:32], raw_data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

# Extract hidden message from the red channel's LSB (prints to console)
def extract_message(image_path):
    img = cv2.imread(image_path)

    if img is None:
        print("❌ Image not found!")
        return

    binary_data = ""
    rows, cols, _ = img.shape

    # Extract binary message from LSB of red channel
    for i in range(rows):
        for j in range(cols):
            binary_data += str(img[i, j, 2] & 1)

    # Find the end marker and convert binary to text
    end_marker = "1111111111111110"
    end_index = binary_data.find(end_marker)

    if end_index == -1:
        print("⚠️ No hidden message found!")
        return

    message_binary = binary_data[:end_index]
    encrypted_text = ''.join(chr(int(message_binary[i:i+8], 2)) for i in range(0, len(message_binary), 8))

    # Decrypt the message
    key = load_key()
    decrypted_text = decrypt_message(encrypted_text, key)
    print("✅ Hidden Message:", decrypted_text)

# New function that returns the decrypted message (for Streamlit)
def extract_message_return(image_path):
    """Extract and return the hidden message from an image"""
    try:
        img = cv2.imread(image_path)

        if img is None:
            return None

        binary_data = ""
        rows, cols, _ = img.shape

        # Extract binary message from LSB of red channel
        for i in range(rows):
            for j in range(cols):
                binary_data += str(img[i, j, 2] & 1)

        # Find the end marker and convert binary to text
        end_marker = "1111111111111110"
        end_index = binary_data.find(end_marker)

        if end_index == -1:
            return None

        message_binary = binary_data[:end_index]
        encrypted_text = ''.join(chr(int(message_binary[i:i+8], 2)) for i in range(0, len(message_binary), 8))

        # Decrypt the message
        key = load_key()
        decrypted_text = decrypt_message(encrypted_text, key)
        return decrypted_text
    except Exception as e:
        print(f"Decryption error: {e}")
        return None