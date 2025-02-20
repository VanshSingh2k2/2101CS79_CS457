# Part 2: Potential Vulnerabilities & Mitigation Strategies

## Potential Vulnerabilities

The given implementation uses RSA encryption with PKCS1_OAEP, a secure encryption scheme. However, several potential vulnerabilities or weaknesses should be considered:

### a. Key Storage

- **Vulnerability**: The private key is saved as an unprotected string, which could potentially be accessed by unauthorized users if not handled securely.
- **Mitigation Strategy**: 
  - Store private keys securely using a hardware security module (HSM) or encrypted key storage systems.
  - If stored on disk, the private key should be encrypted using a symmetric encryption algorithm (e.g., AES).

### b. Message Length Limitation

- **Vulnerability**: The PKCS1_OAEP encryption method has a limitation on the maximum size of the message it can encrypt (depending on the key size). For example, with a 2048-bit RSA key, the maximum plaintext size that can be encrypted is approximately 214 bytes.
- **Mitigation Strategy**:
  - The code already implements message splitting into chunks. Ensure that the chunk size is always well within the acceptable limit for RSA encryption.
  - Consider using hybrid encryption, where the message is encrypted using a symmetric algorithm like AES, and the AES key is then encrypted using RSA.

### c. Error Handling

- **Vulnerability**: The current error handling only prints errors to the console, which may expose sensitive data such as part of the message or key.
- **Mitigation Strategy**:
  - Log errors securely (without exposing sensitive data).
  - Ensure the system responds with generic error messages to avoid revealing details that might assist an attacker.

### d. Lack of Authentication/Integrity

- **Vulnerability**: The implementation doesn't ensure the integrity or authenticity of the message. Attackers could modify the ciphertext, and the receiver wouldn't know it.
- **Mitigation Strategy**:
  - Implement digital signatures or use authenticated encryption like RSA-PSS or AES-GCM to ensure the integrity and authenticity of messages.
  - You can sign the message with the private key before encryption and verify the signature after decryption.

### e. Weak Key Generation/Parameter Choice

- **Vulnerability**: A key size of 2048 bits is considered secure but may be vulnerable to future attacks with advancements in computational power.
- **Mitigation Strategy**:
  - Consider using a larger key size (e.g., 3072 or 4096 bits) to future-proof the encryption. This decision depends on the security and performance trade-offs.

## Mitigation Strategies

### a. Key Management

- **Private Key Protection**: Use secure storage mechanisms (like an HSM, TPM, or a secure enclave) to store the private key. For software storage, use strong encryption with secure key management practices.

### b. Hybrid Encryption

- **Hybrid Encryption**: Encrypt the message with a fast symmetric algorithm (e.g., AES) and then encrypt the symmetric key with RSA. This avoids the message size limitations inherent in RSA encryption.

### c. Digital Signatures

- **Digital Signatures**: Use RSA signing with SHA256 or other secure hash functions to ensure the message’s integrity. The recipient can verify the signature and ensure the message hasn't been altered.

### d. Error Handling Best Practices

- **Error Logging**: Avoid exposing sensitive data in error messages. Log errors securely in a way that doesn't leak critical information (e.g., private keys, plaintext data).

### e. Key Rotation

- **Key Rotation**: Implement regular key rotation practices to limit the risks of key compromise. Use different keys for different sessions or periods.

## Impact of Different Key Sizes

The RSA key size directly impacts both the security and performance of the encryption process.

### a. Security Considerations

- **2048-bit RSA**: Considered secure against current attack vectors but vulnerable to future advancements in quantum computing. It is generally the minimum recommended size for many applications.
- **3072-bit RSA**: More secure than 2048-bit and recommended for stronger security. It provides a higher level of protection but may impact performance more than 2048-bit RSA.
- **4096-bit RSA**: Provides even stronger security but will have a significant performance impact in terms of both key generation and encryption/decryption speeds.

### b. Performance Considerations

- **Larger Key Sizes**: The larger the key size, the slower the encryption and decryption operations. For example, a 4096-bit key will take more time for both encryption and decryption than a 2048-bit key.
- **Trade-off**: You need to balance between performance and security. For large volumes of data, symmetric encryption (like AES) might be more practical, and RSA can be used only for securing the key exchange.

### c. Quantum Resistance

- **Impact of Quantum Computers**: RSA encryption could become vulnerable to quantum attacks using Shor’s algorithm, which could break RSA encryption with much smaller computational resources than classical computers. This has led to the exploration of quantum-resistant algorithms.

## Side-Channel Attacks

Side-channel attacks exploit information leaked during cryptographic operations, such as timing information, power consumption, or electromagnetic emissions.

### a. Timing Attacks

- **Vulnerability**: If the decryption or signing operations are not constant-time, attackers might be able to infer private key information by analyzing the time it takes to perform operations.
- **Mitigation Strategy**: Ensure the cryptographic operations are implemented in constant-time to avoid leaking information through timing differences.

### b. Power Analysis Attacks

- **Vulnerability**: By analyzing the power consumption during RSA operations, an attacker could potentially extract the private key.
- **Mitigation Strategy**: Implement countermeasures like using power analysis-resistant hardware or applying techniques like blinding (randomizing intermediate values during the cryptographic operation).

### c. Cache Attacks

- **Vulnerability**: Cache timing differences might reveal information about private keys if the algorithm depends on secret data.
- **Mitigation Strategy**: Use cache-constant-time implementations or isolate cryptographic operations on dedicated hardware.

### d. Radiation/EM Attacks

- **Vulnerability**: Sensitive information could be extracted by analyzing the electromagnetic radiation emitted by a device performing cryptographic operations.
- **Mitigation Strategy**: Use shielding techniques to prevent unauthorized access to electromagnetic emissions.

---

In conclusion, while the implementation is secure with standard encryption schemes, it should be carefully analyzed for key management, error handling, and other best practices, especially in production environments. By incorporating better error handling, secure storage for private keys, and hybrid encryption for large messages, the system's security and performance can be improved. Additionally, addressing side-channel vulnerabilities is essential for protecting sensitive data in high-security environments.

---

# Part 3: Performance Monitoring and Optimization

## Key Points

- **Message Sizes**: The script tests different message sizes, including small (16 bytes) to larger sizes (4096 bytes).
- **Performance Monitoring**: 
  - `time.time()` is used to measure encryption and decryption times.
  - `psutil` is used to monitor CPU usage and memory consumption.
- **Visualization**: The results for encryption/decryption times, memory usage, and CPU utilization are plotted using `matplotlib`.

## What the Code Does

- **Encryption/Decryption Speeds**: Measures how long it takes to encrypt and decrypt messages of various sizes.
- **Memory Usage**: Monitors memory usage before and after the encryption/decryption process.
- **CPU Utilization**: Records CPU usage during encryption and decryption.
- **Visualization**: Displays line charts to help analyze the performance.

## Running the Code

When you run the script, you should see the following:

- A plot showing the time taken for encryption and decryption for different message sizes.
- A plot showing memory usage for both encryption and decryption.
- A plot showing CPU usage during encryption and decryption.

## Analysis & Recommendations

Based on the results:

### Encryption/Decryption Speed
- As the message size increases, both encryption and decryption times will likely increase.
- Optimizing RSA key sizes or using hybrid encryption (AES for the message and RSA for key encryption) can improve performance.

### Memory Usage
- Memory consumption should remain relatively constant unless the message size is extremely large. However, with very large keys or longer operations, memory usage might increase.

### CPU Usage
- Encryption and decryption can be CPU-intensive, especially for larger messages.
- If CPU usage is a concern, consider switching to more efficient encryption algorithms for larger datasets.

## Optimization Recommendations

- For large message sizes, use hybrid encryption where RSA is used only for encrypting the symmetric key (e.g., AES).
- Consider using parallel processing to speed up encryption or decryption when dealing with multiple large files.
- If using RSA for large files, consider breaking up the file into smaller chunks that fit within the RSA encryption size limit.
