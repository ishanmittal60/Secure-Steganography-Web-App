import streamlit as st
import cv2
import os
from PIL import Image
from stego import generate_key, hide_message, load_key
from stego_decrypt import extract_message_return

# Set page config
st.set_page_config(
    page_title="Secure Steganography",
    page_icon="🔐",
    layout="wide"
)

# Initialize session state
if 'encoded_image_path' not in st.session_state:
    st.session_state.encoded_image_path = None
if 'original_image_path' not in st.session_state:
    st.session_state.original_image_path = None
if 'encryption_complete' not in st.session_state:
    st.session_state.encryption_complete = False

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app title
st.title("🔐 Secure Steganography App")
st.markdown("Hide and extract secret messages in images using AES encryption")
st.markdown("---")

# Create tabs
tab1, tab2 = st.tabs(["🔒 Encrypt & Hide Message", "🔓 Decrypt & Extract Message"])

# ==================== ENCRYPTION TAB ====================
with tab1:
    st.header("Encrypt a Message")
    
    col1, col2 = st.columns(2)
    
    with col1:
        message = st.text_area("Enter the secret message you want to hide:", height=150, placeholder="Type your secret message here...")
    
    with col2:
        image_file = st.file_uploader("Upload an image to hide the message:", type=["jpg", "jpeg", "png"], key="encrypt_upload")
        
        if image_file:
            st.image(image_file, caption="Original Image", use_column_width=True)

    if st.button("🔒 Encrypt and Hide Message", type="primary"):
        if message and image_file:
            try:
                with st.spinner("Encrypting and hiding your message..."):
                    # Save the uploaded image temporarily
                    img_path = "temp_image.jpg"
                    with open(img_path, "wb") as f:
                        f.write(image_file.getbuffer())
                    
                    # Generate key if not already generated
                    if not os.path.exists("aes_key.key"):
                        generate_key()
                    
                    # Hide the message in the image
                    output_image_path = "encoded_image.png"
                    hide_message(img_path, message, output_image_path)
                    
                    # Store in session state
                    st.session_state.encoded_image_path = output_image_path
                    st.session_state.original_image_path = img_path
                    st.session_state.encryption_complete = True
                    
                    st.success("✅ Message successfully encrypted and hidden!")
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.encryption_complete = False
        else:
            st.warning("⚠️ Please enter a message and upload an image.")
    
    # Display results if encryption is complete
    if st.session_state.encryption_complete and st.session_state.encoded_image_path:
        # Display the encoded image
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("Original Image")
            if os.path.exists(st.session_state.original_image_path):
                st.image(st.session_state.original_image_path, use_column_width=True)
        
        with col_b:
            st.subheader("Encoded Image")
            if os.path.exists(st.session_state.encoded_image_path):
                st.image(st.session_state.encoded_image_path, use_column_width=True)
        
        # Provide download buttons
        st.markdown("### 📥 Download Files")
        
        download_col1, download_col2 = st.columns(2)
        
        with download_col1:
            if os.path.exists(st.session_state.encoded_image_path):
                with open(st.session_state.encoded_image_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Encoded Image",
                        data=f,
                        file_name="encoded_image.png",
                        mime="image/png"
                    )
        
        with download_col2:
            if os.path.exists("aes_key.key"):
                with open("aes_key.key", "rb") as f:
                    st.download_button(
                        label="🔑 Download Encryption Key",
                        data=f,
                        file_name="aes_key.key",
                        mime="application/octet-stream"
                    )
        
        st.info("ℹ️ **Important:** Keep the encryption key safe! You'll need it to decrypt the message later.")

# ==================== DECRYPTION TAB ====================
with tab2:
    st.header("Decrypt a Message")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_image = st.file_uploader("Upload an encoded image:", type=["png", "jpg", "jpeg"], key="decrypt_upload")
        
        if uploaded_image:
            st.image(uploaded_image, caption="Encoded Image", use_column_width=True)
    
    with col2:
        key_file = st.file_uploader("Upload the encryption key (aes_key.key):", type=["key"], key="key_upload")
        
        if key_file:
            # Save the key temporarily
            with open("aes_key.key", "wb") as f:
                f.write(key_file.getbuffer())
            st.success("✅ Encryption key uploaded successfully!")

    if st.button("🔓 Decrypt and Extract Message", type="primary"):
        if uploaded_image and key_file:
            try:
                with st.spinner("Extracting and decrypting your message..."):
                    # Save the uploaded encoded image temporarily
                    encoded_img_path = "temp_encoded_image.png"
                    with open(encoded_img_path, "wb") as f:
                        f.write(uploaded_image.getbuffer())
                    
                    # Extract and decrypt the message
                    decrypted_message = extract_message_return(encoded_img_path)
                    
                    if decrypted_message:
                        st.success("✅ Message successfully decrypted!")
                        st.markdown("### 📜 Decrypted Message:")
                        st.info(decrypted_message)
                        
                        # Display in a code block for easy copying
                        st.code(decrypted_message, language=None)
                    else:
                        st.error("❌ No hidden message found or decryption failed. Make sure you're using the correct key and encoded image.")
                    
                    # Clean up temporary encoded image
                    if os.path.exists(encoded_img_path):
                        os.remove(encoded_img_path)
                        
            except Exception as e:
                st.error(f"❌ Decryption error: {str(e)}")
        elif not uploaded_image:
            st.warning("⚠️ Please upload an encoded image.")
        elif not key_file:
            st.warning("⚠️ Please upload the encryption key file.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>🔐 Secure Steganography App | AES-128 Encryption | LSB Steganography Method</p>
    </div>
""", unsafe_allow_html=True)