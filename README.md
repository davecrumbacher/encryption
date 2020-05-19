# encryption

Two example approaches are provided for encrypting and decrypting files:

## symmetric-only ##
This uses a single symmetric key generated from KMS, encrypts the input file with this key, and then decrypts the encrypted file using the same key.

## symmetric-asymmetric ##
This uses a combination of symmetric and asymmetric keys. For each encryption operation, KMS is used to generate a new symmetric data key. The input file is encrypted with this data key, and the data key is encrypted with the provided public key (RSA) and saved along with the encrypted file data. The decryption operation first reads the encrypted data key, decrypts it with the provided private key (RSA), then uses the unencrypted data key to decrypt the data file and save an unencrypted version of the file.
