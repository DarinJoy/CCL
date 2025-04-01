import os
from flask import Flask, request, send_from_directory, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)

# Folders for encrypted and decrypted files
ENCRYPTED_FOLDER = 'static/encrypted_files'
DECRYPTED_FOLDER = 'static/decrypted_files'

# Ensure folders exist
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)
os.makedirs(DECRYPTED_FOLDER, exist_ok=True)

# Encryption/Decryption key (for demo purposes, generate a new key each time)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Function to encrypt file
def encrypt_file(file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    encrypted_data = cipher_suite.encrypt(file_data)
    encrypted_file_path = os.path.join(ENCRYPTED_FOLDER, os.path.basename(file_path))
    with open(encrypted_file_path, 'wb') as f:
        f.write(encrypted_data)
    return encrypted_file_path

# Function to decrypt file
def decrypt_file(file_path):
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    decrypted_file_path = os.path.join(DECRYPTED_FOLDER, os.path.basename(file_path))
    with open(decrypted_file_path, 'wb') as f:
        f.write(decrypted_data)
    return decrypted_file_path

# Route for home page
@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

# Route to process file encryption or decryption
@app.route('/process', methods=['POST'])
def process_file():
    file = request.files['file']
    action = request.form['action']
    file_path = os.path.join('static', file.filename)
    
    # Save the uploaded file temporarily
    file.save(file_path)
    
    if action == 'encrypt':
        encrypted_file = encrypt_file(file_path)
        return jsonify({'message': f'File encrypted successfully: {encrypted_file}'})
    elif action == 'decrypt':
        decrypted_file = decrypt_file(file_path)
        return jsonify({'message': f'File decrypted successfully: {decrypted_file}'})
    
    return jsonify({'message': 'Invalid action.'})

if __name__ == '__main__':
    app.run(debug=True)
