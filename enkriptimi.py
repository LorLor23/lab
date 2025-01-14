from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import csv


# AES Encryption and Decryption Functions
def aes_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')  # Initialization Vector (IV)
    ct = base64.b64encode(ct_bytes).decode('utf-8')  # Ciphertext
    return iv, ct


def aes_decrypt(iv, ct, key):
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
    return decrypted


# RSA Encryption and Decryption Functions
def rsa_encrypt(data, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher.encrypt(data.encode())
    return base64.b64encode(encrypted_data).decode('utf-8')


def rsa_decrypt(encrypted_data, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher.decrypt(base64.b64decode(encrypted_data))
    return decrypted_data.decode('utf-8')


# Generate RSA Keys (Public and Private)
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


# Function to process and encrypt CSV data using AES or RSA
def process_and_encrypt_csv(input_csv_filename, output_csv_filename, encryption_method="AES"):
    # Read the input CSV file
    with open(input_csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)  # Read all rows

    headers = rows[0]
    data_rows = rows[1:]

    # Generate RSA keys if needed (only if using RSA)
    if encryption_method == "RSA":
        private_key, public_key = generate_rsa_keys()
        public_key_obj = RSA.import_key(public_key)
        private_key_obj = RSA.import_key(private_key)

    # AES Key (for AES encryption)
    aes_key = get_random_bytes(16)  # AES key should be 16, 24, or 32 bytes

    # Open the output CSV to write the encrypted data
    with open(output_csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header row (same as input, with added columns for encrypted data)
        writer.writerow(headers + ['Encrypted Data', 'Encryption Method'])

        for row in data_rows:
            data_to_encrypt = ','.join(row)  # Combine all columns as a string to encrypt

            if encryption_method == "AES":
                # Encrypt data using AES
                iv, encrypted_data = aes_encrypt(data_to_encrypt, aes_key)
                writer.writerow(row + [f"{iv},{encrypted_data}", "AES"])
                print(f"AES Encryption applied for row: {row}")

            elif encryption_method == "RSA":
                # Encrypt data using RSA
                encrypted_data_rsa = rsa_encrypt(data_to_encrypt, public_key_obj)
                writer.writerow(row + [encrypted_data_rsa, "RSA"])
                print(f"RSA Encryption applied for row: {row}")

            else:
                print("Unsupported encryption method!")

    print(f"Encrypted data saved to {output_csv_filename}")


# Example of processing with AES encryption
input_csv_filename = "products_with_description.csv"  # The CSV file you generated
output_csv_filename = "encrypted_products_data_aes.csv"
process_and_encrypt_csv(input_csv_filename, output_csv_filename, encryption_method="AES")

# Example of processing with RSA encryption
output_csv_filename = "encrypted_products_data_rsa.csv"
process_and_encrypt_csv(input_csv_filename, output_csv_filename, encryption_method="RSA")
