import boto3
import uuid
import gzip
import io
import os
import json

from faker import Faker

NUM_BATCH = 10
BATCH_SIZE = 1000
BUCKET = 'shhorsfi-select-demo'

def create_profile():
    fake = Faker()
    user = fake.profile()
    return user

## Main Execution
if __name__ == '__main__':

    s3 = boto3.client('s3')

    print("Generate Random Data")
    for _ in range(NUM_BATCH):
        print("Generating Batch: {}".format(_))
        batch_id = uuid.uuid4()

        outfilename = 'profile-{}.txt.gz'.format(batch_id)
        with gzip.open(outfilename, 'wb') as output:
            with io.TextIOWrapper(output, encoding='utf-8', newline='\n') as enc:
                for _ in range(BATCH_SIZE):
                    print('.', end='', flush=True)
                    enc.write(json.dumps(create_profile(), default=str))
                    enc.write('\n')

        s3.upload_file(outfilename, BUCKET, '{}/{}'.format(uuid.uuid4(), outfilename))
