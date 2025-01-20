def display_binary_file(file_path):
    try:
        # Open the binary file in read mode
        with open(file_path, "rb") as file:
            # Read the contents of the file
            file_content = file.read()
            
            # Convert each byte to its binary representation and join them
            binary_representation = ''.join(format(byte, '08b') for byte in file_content)
            
            # Display the binary representation
            print(binary_representation)
    except Exception as e:
        print(f"Error: {e}")

# Example usage
file_path = "encrypted_message.txt"  # Replace with the path to your binary file
display_binary_file(file_path)
