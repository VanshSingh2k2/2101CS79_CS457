from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os
import time
import matplotlib.pyplot as plt

# Constants
BLOCK_SIZE = 16
KEY_SIZE = 32  # AES-256 requires a 256-bit (32-byte) key

# Function to generate a random AES-256 key
def generate_key():
    """Generate a random 256-bit key."""
    return get_random_bytes(KEY_SIZE)

# Function to encrypt data
def encrypt_data(key, plaintext):
    """Encrypt plaintext using AES-256."""
    try:
        cipher = AES.new(key, AES.MODE_CBC)  # CBC mode requires IV
        ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), BLOCK_SIZE))
        return cipher.iv + ciphertext  # Prepend IV to ciphertext
    except Exception as e:
        raise ValueError(f"Encryption failed: {e}")

# Function to decrypt data
def decrypt_data(key, ciphertext):
    """Decrypt ciphertext using AES-256."""
    try:
        iv = ciphertext[:BLOCK_SIZE]  # Extract IV
        actual_ciphertext = ciphertext[BLOCK_SIZE:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(actual_ciphertext), BLOCK_SIZE)
        return plaintext.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")

# Function to handle file encryption
def encrypt_file(key, input_file, output_file):
    """Encrypt the contents of a file."""
    try:
        with open(input_file, 'r') as f:
            plaintext = f.read()
        encrypted_data = encrypt_data(key, plaintext)
        with open(output_file, 'wb') as f:
            f.write(encrypted_data)
    except Exception as e:
        raise ValueError(f"File encryption failed: {e}")

# Function to handle file decryption
def decrypt_file(key, input_file, output_file):
    """Decrypt the contents of a file."""
    try:
        with open(input_file, 'rb') as f:
            ciphertext = f.read()
        decrypted_data = decrypt_data(key, ciphertext)
        with open(output_file, 'w') as f:
            f.truncate(0)  # Clear existing data
            f.write(decrypted_data)
    except Exception as e:
        raise ValueError(f"File decryption failed: {e}")

# Analysis and Testing
# Potential Vulnerabilities and Mitigation
# 1. Key Management: Ensure secure storage of keys using hardware security modules (HSM) or environment variables.
# 2. Padding Oracle Attack: Use authenticated encryption modes (e.g., GCM) to prevent padding oracle attacks.
# 3. Weak Randomness: Ensure cryptographic randomness using secure libraries like PyCryptodome.

# Side-channel attacks:
# Timing attacks and power analysis can be mitigated by avoiding branch and timing variations during cryptographic operations.

# Performance Testing
def performance_test():
    """Test encryption and decryption performance with varying input sizes."""
    key = generate_key()
    input_sizes = [1024, 2048, 4096, 8192, 16384]  # Bytes
    encryption_times = []
    decryption_times = []

    for size in input_sizes:
        data = os.urandom(size).decode('latin1')  # Generate random data
        
        # Encryption performance
        start_time = time.time()
        encrypted = encrypt_data(key, data)
        encryption_times.append(time.time() - start_time)

        # Decryption performance
        start_time = time.time()
        decrypt_data(key, encrypted)
        decryption_times.append(time.time() - start_time)

    # Visualization
    plt.figure(figsize=(10, 5))
    plt.plot(input_sizes, encryption_times, label='Encryption Time', marker='o')
    plt.plot(input_sizes, decryption_times, label='Decryption Time', marker='o')
    plt.title('Performance of AES-256 Encryption/Decryption')
    plt.xlabel('Input Size (bytes)')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    # Example usage
    key = generate_key()

    # File paths
    plaintext_file = "plaintext.txt"
    encrypted_file = "encrypted.bin"
    decrypted_file = "decrypted.txt"

    # Encrypt and decrypt file
    encrypt_file(key, plaintext_file, encrypted_file)
    decrypt_file(key, encrypted_file, decrypted_file)

    print(f"Encryption and decryption completed. Check {decrypted_file} for output.")

    # Run performance tests
    performance_test()
