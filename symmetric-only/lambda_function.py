from cryptography.fernet import Fernet
import json
import sys

def lambda_handler(event, context):
    original_filename = "test.txt"

    data_key_file = 'data_key.json'
    encrypted_filename = '/tmp/' + original_filename + '.encrypted'
    decrypted_filename = '/tmp/' + original_filename + '.decrypted'

    # Read the datakey
    print('\n> Read data key file: {0}'.format(data_key_file))
    with open(data_key_file, 'r') as f:
        data_key_json = json.load(f)
    data_key_plaintext = data_key_json['Plaintext']

    # Read the file into memory
    print('\n> Read original file: {0}'.format(original_filename))
    with open(original_filename, 'rb') as f:
        original_contents = f.read()
    print('\n> Original file contents:\n\n{0}'.format(original_contents))

    # Encrypt the file
    print('\n> Encrypt the file')
    cipher = Fernet(data_key_plaintext)
    encrypted_contents = cipher.encrypt(original_contents)

    # Write the encrypted data file contents
    print('\n> Write encrypted file: {0}'.format(encrypted_filename))
    with open(encrypted_filename, 'wb') as f:
        f.write(encrypted_contents)
    print('\n> Encrypted file contents:\n\n{0}'.format(encrypted_contents))

    # Read the encrypted file into memory
    print('\n> Read encrypted file: {0}'.format(encrypted_filename))
    with open(encrypted_filename, 'rb') as f:
        encrypted_contents = f.read()

    # Decrypt the contents
    print('\n> Decrypt the file')
    decrypted_contents = cipher.decrypt(encrypted_contents)

    # Write the decrypted data file contents
    print('\n> Write decrypted file: {0}'.format(decrypted_filename))
    with open(decrypted_filename, 'wb') as f:
        f.write(decrypted_contents)
    print('\n> Decrypted file contents:\n\n{0}'.format(decrypted_contents))

    print('\n> Done. Compare "{0}" and "{1}" to make sure they are identical.\n'.format(original_filename, decrypted_filename))
