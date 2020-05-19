from cryptography.fernet import Fernet
import Crypto
from Crypto.PublicKey import RSA
import boto3
import json
import base64
import sys

if len(sys.argv) < 2:
    print('usage: python {0} <filename>'.format(sys.argv[0]))
    sys.exit()
original_filename = sys.argv[1]

cmk_id = '<YOUR-KMS-MASTER-KEY-ID>'
public_key_filename = 'public.key'
private_key_filename = 'private.key'
NUM_BYTES_FOR_LEN = 512

def create_data_key(cmk_id, key_spec='AES_256'):
    """Generate a data key to use when encrypting and decrypting data

    :param cmk_id: KMS CMK ID or ARN under which to generate and encrypt the
    data key.
    :param key_spec: Length of the data encryption key. Supported values:
        'AES_128': Generate a 128-bit symmetric key
        'AES_256': Generate a 256-bit symmetric key
    :return PlaintextDataKey where:
        PlaintextDataKey: Plaintext base64-encoded data key as binary string
    :return None if error
    """

    # Create data key
    kms_client = boto3.client('kms')
    try:
        response = kms_client.generate_data_key(KeyId=cmk_id, KeySpec=key_spec)
    except ClientError as e:
        print('ERROR: {0}'.format(e))
        return None

    # Return the plaintext data key
    return base64.b64encode(response['Plaintext'])

def encrypt_file(filename, cmk_id):
    """Encrypt a file using an AWS KMS CMK

    A data key is generated and associated with the CMK.
    The encrypted data key is saved with the encrypted file. This enables the
    file to be decrypted at any time in the future and by any program that
    has the credentials to decrypt the data key.
    The encrypted file is saved to <filename>.encrypted
    Limitation: The contents of filename must fit in memory.

    :param filename: File to encrypt
    :param cmk_id: AWS KMS CMK ID or ARN
    :return: True if file was encrypted. Otherwise, False.
    """

    # Read the entire file into memory
    try:
        with open(filename, 'rb') as file:
            file_contents = file.read()
    except IOError as e:
        print('ERROR: {0}'.format(e))
        return False

    # Generate a data key associated with the CMK
    # The data key is used to encrypt the file. Each file can use its own
    # data key or data keys can be shared among files.
    # Specify either the CMK ID or ARN
    data_key_plaintext = create_data_key(cmk_id)
    print('Created new AWS KMS data key')

    # Load public key to encrypt symmetric data key
    with open(public_key_filename, 'r') as f:
        public_key = RSA.importKey(f.read())

    # Encrypt the data key
    data_key_encrypted = public_key.encrypt(data_key_plaintext, None)[0]

    # Encrypt the file
    f = Fernet(data_key_plaintext)
    file_contents_encrypted = f.encrypt(file_contents)

    # Write the encrypted data key and encrypted file contents together
    encrypted_filename = filename + '.encrypted'
    try:
        with open(encrypted_filename, 'wb') as file_encrypted:
            file_encrypted.write(len(data_key_encrypted).to_bytes(NUM_BYTES_FOR_LEN, byteorder='big'))
            file_encrypted.write(data_key_encrypted)
            file_encrypted.write(file_contents_encrypted)
    except IOError as e:
        print('ERROR: {0}'.format(e))
        return False

    # For the highest security, the data_key_plaintext value should be wiped
    # from memory. Unfortunately, this is not possible in Python. However,
    # storing the value in a local variable makes it available for garbage
    # collection.
    return encrypted_filename

def decrypt_file(filename):
    """Decrypt a file encrypted by encrypt_file()

    The encrypted file is read from <filename>.encrypted
    The decrypted file is written to <filename>.decrypted

    :param filename: File to decrypt
    :return: True if file was decrypted. Otherwise, False.
    """

    # Load private key from file for decryption
    with open(private_key_filename, 'r') as f:
        private_key = RSA.importKey(f.read())

    # Read the encrypted file into memory
    try:
        with open(filename + '.encrypted', 'rb') as file:
            file_contents = file.read()
    except IOError as e:
        logging.error(e)
        return False

    # The first NUM_BYTES_FOR_LEN bytes contain the integer length of the
    # encrypted data key.
    # Add NUM_BYTES_FOR_LEN to get index of end of encrypted data key/start
    # of encrypted data.
    data_key_encrypted_len = int.from_bytes(file_contents[:NUM_BYTES_FOR_LEN], byteorder='big') + NUM_BYTES_FOR_LEN
    data_key_encrypted = file_contents[NUM_BYTES_FOR_LEN:data_key_encrypted_len]

    # Decrypt the data key before using it
    data_key_plaintext = private_key.decrypt(data_key_encrypted)
    if data_key_plaintext is None:
        return False

    # Decrypt the rest of the file
    f = Fernet(data_key_plaintext)
    file_contents_decrypted = f.decrypt(file_contents[data_key_encrypted_len:])

    # Write the decrypted file contents
    decrypted_filename = filename + '.decrypted'
    try:
        with open(decrypted_filename, 'wb') as file_decrypted:
            file_decrypted.write(file_contents_decrypted)
    except IOError as e:
        logging.error(e)
        return False

    # The same security issue described at the end of encrypt_file() exists
    # here, too, i.e., the wish to wipe the data_key_plaintext value from
    # memory.
    return decrypted_filename

print('\n> Encrypt')
encrypted_filename = encrypt_file(original_filename, cmk_id)
print('Encypted file created: {0}'.format(encrypted_filename))

print('\n> Decrypt')
decrypted_filename = decrypt_file(original_filename)
print('Decrypted file created: {0}'.format(decrypted_filename))

print('\n> Done. Compare "{0}" and "{1}" to make sure they are identical.\n'.format(original_filename, decrypted_filename))

