import boto3
glacier = boto3.client("glacier")

# http://boto3.readthedocs.io/en/latest/reference/services/glacier.html
jobParameters = {
    "Type": "select", "ArchiveId": "yuvgrcdN4vgCtd8SeVDORHzJnRFR1kFv-PLxQQMEWUudosLKGYv-f7os8IItsGfmOECuvOx_XzTZqDZZvpmfNwu2QRNDuBK3yv7qxgsH9U9n5tKvtuI9l_3zngiBmCEiy6Y5kw4bQg",
    "Tier": "Expedited",
    'SNSTopic': 'arn:aws:sns:us-west-2:174570359254:GlacierNotify',
    "SelectParameters": {
        "InputSerialization": {"csv": {}},
        "ExpressionType": "SQL",
        "Expression": "SELECT * FROM archive WHERE _9 LIKE '%John %'",
        "OutputSerialization": {
            "csv": {}
        }
    },
    "OutputLocation": {
        "S3": {"BucketName": "shhorsfi-select-demo", "Prefix": "restored"}
    }
}


glacier.initiate_job(vaultName="select-demo", jobParameters=jobParameters)
