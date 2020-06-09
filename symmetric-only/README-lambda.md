

1. Launch an EC2 instance with the Amazon Linux 2 AMI. Login to the instance.

2. Configure aws CLI:

`aws configure`

(enter access key, secret key, default region, and default output)

3. Generate symmetric key in KMS:

`aws kms generate-data-key --key-id <MASTER_KEY_ARN> --key-spec AES_256 > data_key.json`

4. Install Python 3:

`sudo yum install python3 -y`

5. Install git client:

`sudo yum install git -y`

6. Clone repo:

`git clone https://github.com/davecrumbacher/encryption.git`

7. Install Python dependencies locally:

`cd encryption/symmetric-only`

`pip3 install -t . -r requirements.txt`

8. Create sample text file:

`echo "This is a test" >test.txt`

9. Create Lambda function in AWS console in the same region as selected in "aws configure" in step #2. Deployment script expects the name "SymmetricEncryption". Select Python 3.7 for the version. Create or select execution role.

10. Test locally:

`python3 run.py test.txt`

11. Deploy the Lambda function (this deploys a slightly modified version of the script -- lambda_function.py):

`sh deploy.sh`

12. Test the Lambda function in the AWS console. The test event can contain any JSON because it is not used.

13. Examine the output.

