from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
import time
import psutil
import os
import matplotlib.pyplot as plt

# Function to generate RSA key pair
def generate_key_pair(key_size=2048):
    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Function to encrypt a message using RSA + AES (Hybrid encryption)
def hybrid_encrypt(public_key, message):
    rsa_key = RSA.import_key(public_key)
    # Generate a random AES session key
    session_key = get_random_bytes(16)
    cipher_aes = AES.new(session_key, AES.MODE_GCM)
    
    # Encrypt the message with AES
    ciphertext, tag = cipher_aes.encrypt_and_digest(message)
    
    # Encrypt the session key with RSA
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_session_key = cipher_rsa.encrypt(session_key)
    
    return encrypted_session_key, cipher_aes.nonce, tag, ciphertext

# Function to decrypt the message using RSA + AES (Hybrid decryption)
def hybrid_decrypt(private_key, encrypted_session_key, nonce, tag, ciphertext):
    rsa_key = RSA.import_key(private_key)
    
    # Decrypt the session key with RSA
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    session_key = cipher_rsa.decrypt(encrypted_session_key)
    
    # Decrypt the message with AES
    cipher_aes = AES.new(session_key, AES.MODE_GCM, nonce=nonce)
    decrypted_message = cipher_aes.decrypt_and_verify(ciphertext, tag)
    
    return decrypted_message

# Function to monitor memory usage and CPU utilization
def monitor_system_usage(interval=1):
    process = psutil.Process(os.getpid())
    # Get CPU usage over a given interval
    cpu_usage = psutil.cpu_percent(interval=interval)
    memory_info = process.memory_info()
    return cpu_usage, memory_info.rss  # Return CPU usage and memory usage (in bytes)

# Performance testing function
def performance_test(public_key, private_key, message_sizes):
    encryption_times = []
    decryption_times = []
    memory_usages = {'encryption': [], 'decryption': []}
    cpu_usages = {'encryption': [], 'decryption': []}

    for size in message_sizes:
        # Generate a random message of the current size
        message = get_random_bytes(size)

        # Measure encryption time and memory/CPU usage
        start_time = time.time()
        cpu_before, mem_before = monitor_system_usage(interval=1)  # Increase interval for better accuracy
        encrypted_session_key, nonce, tag, encrypted_message = hybrid_encrypt(public_key, message)
        encryption_time = time.time() - start_time
        cpu_after, mem_after = monitor_system_usage(interval=1)

        encryption_times.append(encryption_time)
        memory_usages['encryption'].append(mem_after - mem_before)
        cpu_usages['encryption'].append(cpu_after - cpu_before)

        # Measure decryption time and memory/CPU usage
        start_time = time.time()
        cpu_before, mem_before = monitor_system_usage(interval=1)
        decrypted_message = hybrid_decrypt(private_key, encrypted_session_key, nonce, tag, encrypted_message)
        decryption_time = time.time() - start_time
        cpu_after, mem_after = monitor_system_usage(interval=1)

        decryption_times.append(decryption_time)
        memory_usages['decryption'].append(mem_after - mem_before)
        cpu_usages['decryption'].append(cpu_after - cpu_before)

    return encryption_times, decryption_times, memory_usages, cpu_usages

# Visualization function
def plot_results(message_sizes, encryption_times, decryption_times, memory_usages, cpu_usages):
    # Plot encryption/decryption times
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 2, 1)
    plt.plot(message_sizes, encryption_times, label='Encryption Time')
    plt.plot(message_sizes, decryption_times, label='Decryption Time')
    plt.xlabel('Message Size (bytes)')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.title('Encryption/Decryption Times')

    # Plot memory usage
    plt.subplot(2, 2, 2)
    plt.plot(message_sizes, memory_usages['encryption'], label='Encryption Memory Usage')
    plt.plot(message_sizes, memory_usages['decryption'], label='Decryption Memory Usage')
    plt.xlabel('Message Size (bytes)')
    plt.ylabel('Memory Usage (bytes)')
    plt.legend()
    plt.title('Memory Usage')

    # Plot CPU usage
    plt.subplot(2, 2, 3)
    plt.plot(message_sizes, cpu_usages['encryption'], label='Encryption CPU Usage')
    plt.plot(message_sizes, cpu_usages['decryption'], label='Decryption CPU Usage')
    plt.xlabel('Message Size (bytes)')
    plt.ylabel('CPU Usage (%)')
    plt.legend()
    plt.title('CPU Usage')

    plt.tight_layout()
    plt.show()

# Main function to execute the performance test and plot results
def main():
    # Generate RSA key pair
    private_key, public_key = generate_key_pair()

    # Define different message sizes for testing
    message_sizes = [16, 64, 256, 1024, 2048, 4096]

    # Run the performance test
    encryption_times, decryption_times, memory_usages, cpu_usages = performance_test(
        public_key, private_key, message_sizes
    )

    # Plot the results
    plot_results(message_sizes, encryption_times, decryption_times, memory_usages, cpu_usages)

# Run the main function
if __name__ == "__main__":
    main()
