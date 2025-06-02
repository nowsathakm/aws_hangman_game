"""
AWS Cloud Services Words Module for Hangman Game

This module provides AWS cloud service categories and names for the Hangman game.
"""

custom_categories = {
    "AWS Compute": [
        "EC2",
        "LAMBDA",
        "FARGATE",
        "LIGHTSAIL",
        "BEANSTALK",
        "BATCH",
        "ECS",
        "EKS",
        "OUTPOSTS",
        "LOCALZONES"
    ],
    "AWS Storage": [
        "S3",
        "EBS",
        "EFS",
        "FSX",
        "GLACIER",
        "SNOWBALL",
        "SNOWMOBILE",
        "STORAGEGATEWAY",
        "BACKUP",
        "DATASYNC"
    ],
    "AWS Database": [
        "RDS",
        "DYNAMODB",
        "AURORA",
        "REDSHIFT",
        "DOCUMENTDB",
        "NEPTUNE",
        "ELASTICACHE",
        "KEYSPACES",
        "TIMESTREAM",
        "QLDB"
    ],
    "AWS Networking": [
        "VPC",
        "CLOUDFRONT",
        "ROUTE53",
        "APIGATEWAY",
        "DIRECTCONNECT",
        "GLOBALACCELERATOR",
        "TRANSITGATEWAY",
        "APPFABRIC",
        "PRIVATELINK",
        "CLOUDMAP"
    ],
    "AWS Security": [
        "IAM",
        "COGNITO",
        "GUARDDUTY",
        "INSPECTOR",
        "MACIE",
        "FIREWALL",
        "SHIELD",
        "WAF",
        "SECRETSMANAGER",
        "KMS"
    ],
    "AWS Analytics": [
        "ATHENA",
        "EMR",
        "OPENSEARCH",
        "KINESIS",
        "GLUE",
        "QUICKSIGHT",
        "DATAZONE",
        "LAKEFORMATION",
        "MSK",
        "DATAEXCHANGE"
    ],
    "AWS ML & AI": [
        "SAGEMAKER",
        "REKOGNITION",
        "COMPREHEND",
        "POLLY",
        "TEXTRACT",
        "TRANSCRIBE",
        "TRANSLATE",
        "KENDRA",
        "BEDROCK",
        "LEX"
    ],
    "AWS Management": [
        "CLOUDWATCH",
        "CLOUDTRAIL",
        "CONFIG",
        "CLOUDFORMATION",
        "ORGANIZATIONS",
        "CONTROLCATALOG",
        "SYSTEMSMANAGER",
        "TRUSTEDADVISOR",
        "COSTEXPLORER",
        "CHATBOT"
    ]
}

def get_custom_categories():
    """Returns the custom categories dictionary"""
    return custom_categories
