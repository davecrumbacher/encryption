1. Generate symmetric key in KMS:

`aws kms generate-data-key --key-id <MASTER_KEY_ARN> --key-spec AES_256 > data_key.json`

2. Install Python dependencies (preferable in a virtualenv)

`pip install -r requirements.txt`

3. Run Python script to encrypt and decrypt input file:

`python test.py <filename>`

4. Compare original file with .decrypted file:

`diff <filename> <filename>.decrypted`
