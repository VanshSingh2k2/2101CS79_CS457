from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

# Function to generate RSA key pair
def generate_key_pair(key_size=2048):
    try:
        key = RSA.generate(key_size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key
    except Exception as e:
        print(f"Error generating key pair: {e}")
        return None, None

# Function to encrypt a message using the public key
def encrypt_message(public_key, message):
    try:
        rsa_key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        encrypted_message = cipher.encrypt(message)
        return encrypted_message
    except Exception as e:
        print(f"Error encrypting message: {e}")
        return None

# Function to decrypt a message using the private key
def decrypt_message(private_key, encrypted_message):
    try:
        rsa_key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        decrypted_message = cipher.decrypt(encrypted_message)
        return decrypted_message
    except Exception as e:
        print(f"Error decrypting message: {e}")
        return None

# Function to handle different message sizes (splitting for large messages)
def encrypt_large_message(public_key, message, chunk_size=190):
    try:
        rsa_key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        encrypted_chunks = [cipher.encrypt(message[i:i+chunk_size]) for i in range(0, len(message), chunk_size)]
        return encrypted_chunks
    except Exception as e:
        print(f"Error encrypting large message: {e}")
        return None

# Example usage
def main():
    # Step 1: Generate key pair
    private_key, public_key = generate_key_pair()
    if not private_key or not public_key:
        return

    print("Private Key:")
    print(private_key.decode())
    print("Public Key:")
    print(public_key.decode())

    # Step 2: Read message from a file
    try:
        with open("message.txt", "rb") as file:
            message = file.read()
    except Exception as e:
        print(f"Error reading message file: {e}")
        return

    # Step 3: Encrypt and decrypt the message
    encrypted_message = encrypt_message(public_key, message)

    if encrypted_message:
        print("\nEncrypted Message:")
        print(encrypted_message)

        # Save encrypted message to a file
        try:
            with open("encrypted_message.txt", "wb") as file:
                file.write(encrypted_message)
            print("\nEncrypted message saved to 'encrypted_message.txt'.")
        except Exception as e:
            print(f"Error writing encrypted message to file: {e}")

        decrypted_message = decrypt_message(private_key, encrypted_message)

        if decrypted_message:
            print("\nDecrypted Message:")
            print(decrypted_message.decode())

            # Step 4: Save decrypted message to a file
            try:
                with open("decrypted_message.txt", "w") as file:
                    file.write(decrypted_message.decode())
                print("\nDecrypted message saved to 'decrypted_message.txt'.")
            except Exception as e:
                print(f"Error writing decrypted message to file: {e}")

if __name__ == "__main__":
    main()
