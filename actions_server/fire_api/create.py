import os
import boto3

#database setup
AWSAccessKeyId=os.environ.get('AWSAccessKeyId')
AWSSecretKey=os.environ.get('AWSSecretKey')

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWSAccessKeyId,
    aws_secret_access_key=AWSSecretKey,
    region_name='us-east-2'
)

fire_table = dynamodb.create_table(
        TableName='fires',
        KeySchema=[
            {
                'AttributeName': 'county',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'uuid',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'county',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'uuid',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
)

weather_table = dynamodb.create_table(
        TableName='weather',
        KeySchema=[
            {
                'AttributeName': 'city',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'time',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'city',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'time',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
)
