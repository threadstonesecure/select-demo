import boto3
import time
import json
import io
import shutil

import gzip

BUCKET = "shhorsfi-select-demo"
KEY = "standard/c796b57e-c1fd-4c89-a6ba-08b1c9cde66d/profile-3118de38-e4c0-4c2e-984e-873bc4a7d16f.txt.gz"

## S3 Download File
print("\n\nDownloading Object from S3")
print("-----------------------------------------")
start_time = time.time()
s3 = boto3.resource('s3')

bucket = s3.Bucket(BUCKET)
compressed_file = io.BytesIO()

with open('download.txt', 'wb') as fp:
    bucket.download_fileobj(KEY, compressed_file)
    compressed_file.seek(0)
    with gzip.GzipFile(fileobj=compressed_file, mode='rb') as gz:
            shutil.copyfileobj(gz, fp)

with open("download.txt", "r") as profiles:
    count = 0
    for line in profiles:
        profile = json.loads(line)
        if "@gmail.com" in profile['mail']:
            count += 1

    print("Record Count: {}".format(count))
end_time = time.time()
print("Completed in: {}".format(end_time-start_time))
print("-----------------------------------------")

## S3 Select
print("\n\nSelecing Count of Records")
print("-----------------------------------------")
start_time = time.time()
s3 = boto3.client('s3')
# http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.select_object_content
r = s3.select_object_content(
        Bucket='shhorsfi-select-demo',
        Key='standard/c796b57e-c1fd-4c89-a6ba-08b1c9cde66d/profile-3118de38-e4c0-4c2e-984e-873bc4a7d16f.txt.gz',
        ExpressionType='SQL',
        Expression="select count(*) from s3object s where s.\"mail\" like '%@gmail.com'",
        InputSerialization = {'CompressionType': 'GZIP',
                              'JSON': {"Type": "LINES"}
                              },
        OutputSerialization = {'CSV': {}},
)

for event in r['Payload']:
    if 'Records' in event:
        records = event['Records']['Payload'].decode('utf-8')
        print("Record Count: {}".format(records))
    elif 'Stats' in event:
        statsDetails = event['Stats']['Details']
        print("Stats details bytesScanned: {} ".format(statsDetails['BytesScanned']))
        print("Stats details bytesProcessed: {} ".format(statsDetails['BytesProcessed']))

end_time = time.time()

print("Completed in: {}".format(end_time-start_time))
print("-----------------------------------------")
