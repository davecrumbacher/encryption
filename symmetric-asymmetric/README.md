1. Make sure you have AWS credentials setup: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html?highlight=role

2. Edit test.py and change the value for cmk_id to be your KMS key ID

3. Save your RSA public key as public.key

4. Save your RSA private key as private.key

5. Install Python dependencies (preferable in a virtualenv)

`pip install -r requirements.txt`

6. Run Python script to encrypt and decrypt input file:

`python test.py <filename>`

7. Compare original file with .decrypted file:

`diff <filename> <filename>.decrypted`
