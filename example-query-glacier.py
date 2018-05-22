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
        "S3": {"BucketName": "shhorsfi-select-demo", "Prefix": "restored"}
    }
}

glacier.initiate_job(vaultName="shhorsfi-select-demo", jobParameters=jobParameters)
