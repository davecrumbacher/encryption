#!/bin/sh

echo "Adding files to zip archive..."
rm -f deployment.zip
zip -qr deployment.zip * .[^.]*

echo "Updating AWS Lambda function..."
aws lambda update-function-code --function-name SymmetricEncryption --zip-file fileb://deployment.zip >/dev/null
rm -f deployment.zip

echo "Success."
