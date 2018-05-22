import boto3
s3 = boto3.client('s3')

# http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.select_object_content
r = s3.select_object_content(
        Bucket='shhorsfi-select-demo',
        Key='single_file_standard/342d86e2-b54d-4c20-9849-4ac71ac0cdba/profile-c11ae24f-94d9-4b3b-bfb4-1b001d42a82f.txt.gz',
        ExpressionType='SQL',
        Expression="select COUNT(*) from s3object s where s.\"mail\" like '%@gmail.com'",
        InputSerialization = {'CompressionType': 'GZIP',
                              'JSON': {"Type": "LINES"}
                              },
        OutputSerialization = {'CSV': {}},
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
