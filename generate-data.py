import boto3
import uuid
import gzip
import io
import os
import json
import csv

from faker import Faker

BATCH_COUNT = 10
BATCH_SIZE = 100
BUCKET = 'shhorsfi-select-demo-bucket'
STANDARD_PREFIX = 'standard'
GLACIER_PREFIX = 'glacier'
PROCESS_PREFIX = 'process'

def create_profile():
    fake = Faker()
    user = fake.profile()
    return user

def generate_json_data(bucket, prefix, batch_count, batch_size):
    s3 = boto3.client('s3')

    for _ in range(batch_count):
        batch_id = uuid.uuid4()
        outfilename = 'profile-{}.txt.gz'.format(batch_id)

        with gzip.open(outfilename, 'wb') as output:
            with io.TextIOWrapper(output, encoding='utf-8', newline='\n') as enc:
                for _ in range(batch_size):
                    enc.write(json.dumps(create_profile(), default=str))
                    enc.write('\n')

        s3.upload_file(outfilename, bucket, '{}/{}/{}'.format(prefix, uuid.uuid4(), outfilename))
        os.remove(outfilename)

def generate_csv_data(bucket, prefix, batch_count, batch_size):
    s3 = boto3.client('s3')

    batch_id = uuid.uuid4()

    for _ in range(batch_count):
        outfilename = 'profile-{}.csv'.format(batch_id)
        outfile = open('profile-{}.csv'.format(batch_id), 'w')
        csvwriter = csv.writer(outfile)
        count = 0
        for _ in range(batch_size):
            profile = create_profile()
            if count == 0:
                header = profile.keys()
                csvwriter.writerow(header)
                count += 1
            csvwriter.writerow(profile.values())
        outfile.close()

    s3.upload_file(outfilename, bucket, '{}/{}/{}'.format(prefix, uuid.uuid4(), outfilename))
    os.remove(outfilename)

## Main Execution
if __name__ == '__main__':
    #print("Generating JSON data for S3 Demo")
    #generate_json_data(BUCKET, STANDARD_PREFIX, BATCH_COUNT, BATCH_SIZE)
    #print("Generating CSV data for Glacier Demo")
    #generate_csv_data(BUCKET, GLACIER_PREFIX, BATCH_COUNT, BATCH_SIZE)
    print("Generating JSON data for Process Demo")
    generate_json_data(BUCKET, PROCESS_PREFIX, BATCH_COUNT, BATCH_SIZE)
