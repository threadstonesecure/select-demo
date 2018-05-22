import boto3
glacier = boto3.client("glacier")

# http://boto3.readthedocs.io/en/latest/reference/services/glacier.html
jobParameters = {
    "Type": "select", "ArchiveId": "ID",
    "Tier": "Expedited",
    "SelectParameters": {
        "InputSerialization": {"csv": {}},
        "ExpressionType": "SQL",
        "Expression": "SELECT * FROM archive WHERE _5='498960'",
        "OutputSerialization": {
            "csv": {}
        }
    },
    "OutputLocation": {
        "S3": {"BucketName": "glacier-select-output", "Prefix": "1"}
    }
}

glacier.initiate_job(vaultName="reInventSecrets", jobParameters=jobParameters)
