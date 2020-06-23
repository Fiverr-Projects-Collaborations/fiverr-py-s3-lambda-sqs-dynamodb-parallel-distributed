import boto3
import uuid
import datetime


def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
    for record in event['Records']:
        idx = uuid.uuid4().hex
        payload = record["body"]
        print(str(payload))
        direction = str(payload).split(',')[0]
        client = str(payload).split(',')[1]
        dt = str(datetime.datetime.now())
        response = dynamodb.put_item(
            TableName='crossroad_output',
            Item={
                'id': {'S': idx},
                'direction': {'S': direction},
                'client_name': {'S': client},
                'date_time': {'S': dt}
            }
        )
        print(response)
