import boto3
from urllib.parse import unquote_plus

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket, key)
        body = obj.get()['Body'].read()
        print(body.decode("utf-8") )
        sqs = boto3.client('sqs')
        queue_url = 'https://sqs.us-east-2.amazonaws.com/696261928910/crossroadQueue'
        response = sqs.send_message(QueueUrl=queue_url, DelaySeconds=10, MessageAttributes={}, MessageBody=(body.decode("utf-8") +','+str(key).split('.')[0]))
        print(body.decode("utf-8") +','+str(key).split('.')[0])
        
