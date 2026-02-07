# CCL — File Encryption & Decryption Web App

CCL is a simple web application for encrypting and decrypting files using symmetric encryption.  
It is built with Flask and uses the `cryptography` library’s Fernet implementation to securely process files in memory.

The application provides a browser-based UI as well as a single API endpoint for file processing.

---

## Live Demo

- URL: https://ccl-sage.vercel.app/

---

## Features

- Encrypt uploaded files using Fernet symmetric encryption
- Decrypt files that were previously encrypted using the same key
- Single API endpoint for both encryption and decryption
- Files are processed entirely in memory (no server-side storage)
- Minimal backend with a static frontend
- Ready for deployment on Vercel using `@vercel/python`

---

## Tech Stack

- **Backend:** Flask (Python)
- **Encryption:** `cryptography` (Fernet)
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Vercel

---

## Application Flow

1. On startup, the server attempts to load an encryption key from `secret.key`
2. If the key does not exist, a new one is generated and saved
3. Users upload a file and choose an action (encrypt or decrypt)
4. The file is read into memory and processed using the Fernet cipher
5. The processed file is returned to the client as a downloadable attachment

---

## API Reference

### Endpoint

```

POST /process

````

### Request (multipart/form-data)

| Field   | Description |
|--------|------------|
| `file` | File to be encrypted or decrypted |
| `action` | Either `encrypt` or `decrypt` |

### Response

- Returns the processed file as a download
- Encrypted files are prefixed with `encrypted_`
- Decrypted files are prefixed with `decrypted_`

### Example (cURL)

```bash
# Encrypt a file
curl -X POST "<DEPLOYED_URL>/process" \
  -F "action=encrypt" \
  -F "file=@example.pdf" \
  --output encrypted_example.pdf

# Decrypt a file
curl -X POST "<DEPLOYED_URL>/process" \
  -F "action=decrypt" \
  -F "file=@encrypted_example.pdf" \
  --output decrypted_example.pdf
````

---

## Running Locally

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

**Dependencies**

* flask==2.0.1
* cryptography==41.0.1
* Werkzeug==2.0.1

### 3. Start the application

```bash
python app.py
```

Access the application at:

```
http://127.0.0.1:5000/
```

---

## Deployment (Vercel)

The project includes a `vercel.json` configuration file.

### Deployment steps

```bash
vercel
vercel --prod
```

### Configuration details

* Uses `@vercel/python` to run `app.py`
* Routes all incoming requests to the Flask application
* Sets `PYTHONPATH` to the project root

---

## Important Notes

* **Key persistence:**
  Encryption and decryption depend on the same `secret.key` file.
  If this file is deleted or regenerated, previously encrypted files cannot be decrypted.

* **Security considerations:**
  Files are processed on the server. For sensitive data, deploy in a controlled environment with HTTPS enabled.

* **File size limitations:**
  Files are read fully into memory. Very large files may cause memory or timeout issues.

---
