from lab1_aes import encrypt_data, decrypt_data, generate_key
import os
import time
import matplotlib.pyplot as plt
import tracemalloc
import psutil

def combined_analysis():
    key = generate_key()
    input_sizes = [1024, 2048, 4096, 8192, 16384]
    encryption_times = []
    decryption_times = []
    memory_usages = []
    cpu_usages = []

    tracemalloc.start()
    process = psutil.Process()

    for size in input_sizes:
        data = os.urandom(size).decode('latin1')

        # Measure encryption time and memory usage
        start_time = time.time()
        encrypted = encrypt_data(key, data)
        encryption_times.append(time.time() - start_time)

        current_memory = tracemalloc.get_traced_memory()
        memory_usages.append(current_memory[1])  # Peak memory usage

        # Measure decryption time
        start_time = time.time()
        decrypt_data(key, encrypted)
        decryption_times.append(time.time() - start_time)

        # Measure CPU usage
        cpu_before = process.cpu_percent(interval=None)
        encrypt_data(key, data)  # Repeat to measure CPU usage accurately
        cpu_after = process.cpu_percent(interval=None)
        cpu_usages.append(cpu_after - cpu_before)

    tracemalloc.stop()

    # Visualization
    plt.figure(figsize=(12, 8))

    # Subplot 1: Speed Analysis
    plt.subplot(3, 1, 1)
    plt.plot(input_sizes, encryption_times, label='Encryption Time', marker='o')
    plt.plot(input_sizes, decryption_times, label='Decryption Time', marker='o')
    plt.title('Encryption/Decryption Speeds')
    plt.xlabel('Input Size (bytes)')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid()

    # Subplot 2: Memory Usage
    plt.subplot(3, 1, 2)
    plt.plot(input_sizes, memory_usages, label='Memory Usage', marker='o', color='orange')
    plt.title('Memory Usage During Encryption')
    plt.xlabel('Input Size (bytes)')
    plt.ylabel('Memory (bytes)')
    plt.legend()
    plt.grid()

    # Subplot 3: CPU Utilization
    plt.subplot(3, 1, 3)
    plt.plot(input_sizes, cpu_usages, label='CPU Usage', marker='o', color='green')
    plt.title('CPU Utilization During Encryption')
    plt.xlabel('Input Size (bytes)')
    plt.ylabel('CPU Usage (%)')
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.savefig('combined_analysis.png')
    print("Combined analysis saved as 'combined_analysis.png'")

if __name__ == "__main__":
    combined_analysis()