# lab1_AES256

# AES-256 Encryption/Decryption Tool

A Python implementation of AES-256 encryption and decryption with performance analysis capabilities. This tool provides secure file encryption using AES-256 in CBC mode and includes features for performance testing and visualization.

## Features

- AES-256 encryption and decryption in CBC mode
- File-based encryption and decryption
- Performance testing with visualization
- Secure random key generation
- Error handling and validation

## Security Considerations

- Uses CBC mode with secure padding
- Implements initialization vector (IV) for enhanced security
- Employs secure random number generation
- Includes error handling for cryptographic operations

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/aes-encryption-tool.git
cd aes-encryption-tool
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required dependencies:

```bash
pip install pycryptodome matplotlib
```

## Usage

### Basic Usage

1. Create a file named `plaintext.txt` with your content.

2. Run the script:

```bash
python encryption_tool.py
```

This will:

- Generate a new encryption key
- Encrypt `plaintext.txt` to `encrypted.bin`
- Decrypt `encrypted.bin` to `decrypted.txt`
- Run performance tests and display results

### API Usage

```python
from encryption_tool import generate_key, encrypt_file, decrypt_file

# Generate a new key
key = generate_key()

# Encrypt a file
encrypt_file(key, "input.txt", "encrypted.bin")

# Decrypt a file
decrypt_file(key, "encrypted.bin", "decrypted.txt")
```

## Code Explanation

### Key Components

1. **Key Generation**

   - Uses `get_random_bytes` from PyCryptodome for secure key generation
   - Generates 256-bit (32-byte) keys for AES-256

2. **Encryption Process**

   ```python
   def encrypt_data(key, plaintext):
       cipher = AES.new(key, AES.MODE_CBC)
       ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), BLOCK_SIZE))
       return cipher.iv + ciphertext
   ```

   - Creates new AES cipher in CBC mode
   - Pads input data to match block size
   - Prepends IV to ciphertext for decryption

3. **Decryption Process**

   ```python
   def decrypt_data(key, ciphertext):
       iv = ciphertext[:BLOCK_SIZE]
       actual_ciphertext = ciphertext[BLOCK_SIZE:]
       cipher = AES.new(key, AES.MODE_CBC, iv)
       return unpad(cipher.decrypt(actual_ciphertext), BLOCK_SIZE)
   ```

   - Extracts IV from ciphertext
   - Creates cipher with original IV
   - Removes padding after decryption

4. **Performance Testing**
   - Tests encryption/decryption with various input sizes
   - Generates performance visualization using matplotlib
   - Measures timing for both operations

## Security Best Practices

1. **Key Management**

   - Never store encryption keys in source code
   - Use secure key storage solutions (e.g., environment variables, HSM)
   - Implement proper key rotation policies

2. **Error Handling**

   - All cryptographic operations are wrapped in try-except blocks
   - Provides detailed error messages for debugging
   - Prevents information leakage in error messages

3. **Input Validation**
   - Validates input file existence and permissions
   - Ensures proper encoding of input data
   - Handles padding appropriately

## Performance Considerations

The tool includes performance testing functionality that:

- Tests different input sizes (1KB to 16KB)
- Measures encryption and decryption times
- Generates visualization of performance metrics

## Limitations

- Currently supports only CBC mode
- File-based operations are synchronous
- In-memory processing may not be suitable for very large files
