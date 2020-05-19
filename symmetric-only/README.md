1. Install AWS command line utility and ensure you have permissions to use KMS.

2. Generate symmetric key in KMS:

`aws kms generate-data-key --key-id <MASTER_KEY_ARN> --key-spec AES_256 > data_key.json`

3. Install Python dependencies (preferable in a virtualenv)

`pip install -r requirements.txt`

4. Run Python script to encrypt and decrypt input file:

`python test.py <filename>`

5. Compare original file with .decrypted file:

`diff <filename> <filename>.decrypted`
