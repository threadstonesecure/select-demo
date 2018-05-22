import boto3
s3 = boto3.client('s3')

# http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.select_object_content
r = s3.select_object_content(
        Bucket='shhorsfi-select-demo',
        Key='standard/c796b57e-c1fd-4c89-a6ba-08b1c9cde66d/profile-3118de38-e4c0-4c2e-984e-873bc4a7d16f.txt.gz',
        ExpressionType='SQL',
        Expression="select * from s3object s where s.\"mail\" like '%@gmail.com'",
        InputSerialization = {'CompressionType': 'GZIP',
                              'JSON': {"Type": "LINES"}
                              },
        OutputSerialization = {'JSON': {}},
)

for event in r['Payload']:
    if 'Records' in event:
        records = event['Records']['Payload'].decode('utf-8')
        print("Response: {}".format(records))
    elif 'Stats' in event:
        statsDetails = event['Stats']['Details']
        print("Stats details bytesScanned: ")
        print(statsDetails['BytesScanned'])
        print("Stats details bytesProcessed: ")
        print(statsDetails['BytesProcessed'])
