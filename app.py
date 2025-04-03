import os
from flask import Flask, request, send_from_directory, jsonify, send_file
from cryptography.fernet import Fernet
from io import BytesIO

app = Flask(__name__)

# Encryption/Decryption key (for demo purposes, generate a new key each time)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Function to encrypt file data
def encrypt_data(file_data):
    encrypted_data = cipher_suite.encrypt(file_data)
    return encrypted_data

# Function to decrypt file data
def decrypt_data(encrypted_data):
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data

# Route for home page
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Route to process file encryption or decryption
@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    action = request.form.get('action')
    
    if not file.filename:
        return jsonify({'error': 'No file selected'}), 400
    
    # Read file data into memory
    file_data = file.read()
    
    try:
        if action == 'encrypt':
            processed_data = encrypt_data(file_data)
            filename = f"encrypted_{file.filename}"
        elif action == 'decrypt':
            processed_data = decrypt_data(file_data)
            filename = f"decrypted_{file.filename}"
        else:
            return jsonify({'error': 'Invalid action'}), 400
        
        # Create an in-memory file
        memory_file = BytesIO(processed_data)
        
        # Return the processed file directly to the client
        return send_file(
            memory_file,
            mimetype='application/octet-stream',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
