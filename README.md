# select-demo
An overview and demo of Amazon S3 SELECT and Amazon Glacier SELECT.

## Resources

* [Blog Post - S3 Select and Glacier Select – Retrieving Subsets of Objects ](https://aws.amazon.com/blogs/aws/s3-glacier-select/)
* [SQL Reference](https://docs.aws.amazon.com/amazonglacier/latest/dev/s3-glacier-select-sql-reference.html)
* [re:Invent - STG313](https://www.youtube.com/watch?v=p-JkncBZcc4)
* [re:Invent Twitch Video](https://www.twitch.tv/videos/206752912)
* [AWS Summit Video](https://www.youtube.com/watch?v=uxcyoc6uaLM)

## Demo 1 - S3 Select

1. Open S3 Console, View Bucket/Prefix/Key Structure
2. Navigate to Larger Standard Archive, Select, Check-Box, More-Dropdown, Select From
3. Demo S3 Select GUI
4. Show and Execute Select Script

```
python 3 examples/example-query-s3.py
```
## Demo 2 - Glacier Select

1. Open S3 Console and Navigate to Glacier prefix. Show CSV File.
2. Open Terminal and Show Vault

```
aws glacier list-vaults --account-id [accountID]
```
3. Show and Execute Select Script.

```
python 3 examples/example-query-glacier.py
```
4. Wait for SNS notification, then show restored results in restore prefix.

## Demo 3 - Lambda Processing S3 Select to DynamoDB

1. Configure generate-data.py to generate processing data.

```
python3 generate-data.py
```

## Running Demo

1. Package and Deploy Lambda function

```
sam package \
    --template-file template.yaml \
    --output-template-file packaged.yaml \
    --s3-bucket [DEPLOY_BUCKET_NAME]

sam deploy \
    --template-file packaged.yaml \
    --stack-name select-demo \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides BucketName=[DEMO_BUCKET_NAME] BucketPrefix=[PREFIX_TO_PROCESS]

aws cloudformation describe-stacks \
    --stack-name select-demo --query 'Stacks[].Outputs'

```

2. Generate Data

```
NOTE: Update generate-data.py as needed, bucket is created by Lambda function template.

BATCH_COUNT = 1
BATCH_SIZE = 10
BUCKET = '[DEMO_BUCKET_NAME]'
STANDARD_PREFIX = 'standard'
GLACIER_PREFIX = 'glacier'

python3 generate-data.py

```

3. Update examples/* scripts as needed.
4. NOTE: If you want to demo Glacier you need to manually vault an object, or setup a lifecycle policy and wait for the object to be vaulted. Quickest is to download one of the generated .CSVs and manually vault it with the CLI.
