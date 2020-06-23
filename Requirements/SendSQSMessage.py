import boto3

# Create SQS client
sqs = boto3.client('sqs', region_name='us-east-1',
                   aws_access_key_id="XXX",
                   aws_secret_access_key="XXX")
# Queue URL
queue_url = 'https://sqs.us-east-1.amazonaws.com/175990529520/company_queue'

c_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']

for c in c_list:
    # Send message to SQS queue
    response = sqs.send_message(QueueUrl=queue_url, DelaySeconds=10, MessageAttributes={}, MessageBody=(c))
    print(response['MessageId'])
