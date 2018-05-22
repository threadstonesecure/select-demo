# Import Dependencies
import boto3
import os
import urllib.parse
import json

print('Loading Function')

# Handle Event
def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    s3 = boto3.client('s3')
    results = s3.select_object_content(
            Bucket=bucket,
            Key=key,
            ExpressionType='SQL',
            Expression="select * from s3object s where s.\"name\" like '%John %'",
            InputSerialization = {'CompressionType': 'GZIP',
                                  'JSON': {"Type": "LINES"}
                                  },
            OutputSerialization = {'JSON': {}},
    )

    ddb = boto3.resource('dynamodb')

    print(results)

    for event in results['Payload']:
        if 'Records' in event:
            record = event['Records']['Payload'].decode('utf-8')

            print('Record Found')
            print(record)

            s = record.splitlines()
            for line in s:
                print('Adding to DynamoDB')
                print(line)

                table = ddb.Table(os.environ['RESULTS_TABLE'])
                table.put_item(
                      Item=json.loads(line)
                      )
