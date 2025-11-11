import cv2
from Crypto.Cipher import AES
import base64
import secrets

# Generate a random AES key (Only run once and save it)
def generate_key():
    key = secrets.token_bytes(16)  # AES-128 requires 16 bytes
    with open("aes_key.key", "wb") as f:
        f.write(key)
    print("✅ AES Key saved in aes_key.key")

# Load the AES key
def load_key():
    with open("aes_key.key", "rb") as f:
        return f.read()

# Encrypt the message using AES
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

# Hide encrypted message in the LSB of the red channel
def hide_message(image_path, message, output_path):
    # Load image
    img = cv2.imread(image_path)

    if img is None:
        print("❌ Image not found!")
        return

    # Encrypt the message
    key = load_key()
    encrypted_message = encrypt_message(message, key)
    message_binary = ''.join(format(ord(char), '08b') for char in encrypted_message) + '1111111111111110'  # End marker

    rows, cols, _ = img.shape
    idx = 0

    # Hide message in the red channel's LSB
    for i in range(rows):
        for j in range(cols):
            if idx < len(message_binary):
                img[i, j, 2] = (img[i, j, 2] & 0b11111110) | int(message_binary[idx])  # Modify LSB
                idx += 1
            else:
                break

    # Save encoded image
    cv2.imwrite(output_path, img)
    print(f"✅ Encrypted message hidden in {output_path}")