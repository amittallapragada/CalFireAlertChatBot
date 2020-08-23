import os
import boto3

#database setup
AWSAccessKeyId=os.environ.get('AWSAccessKeyId')
AWSSecretKey=os.environ.get('AWSSecretKey')

client = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWSAccessKeyId,
    aws_secret_access_key=AWSSecretKey,
    region_name='us-east-2'
)

fires_table = client.Table("fires")
weather_table = client.Table("weather")
