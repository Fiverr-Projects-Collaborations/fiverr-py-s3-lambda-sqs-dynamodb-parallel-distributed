Resources:
S3 input bucket - com.crossroad.input
S3 output bucket - com.crossroad.output
SQS - crossroadQueue
Lambda1 - sendSQSMessage
Lambda2 - writeToDB
DynamoDB table - crossroad_output
NOTE: instances running on Ohio (us-east-2)
ec2 - master - 3.12.138.58
ec2 - slave-1 - 3.128.119.204
ec2 - slave-2 - 3.19.166.251
ec2 - slave-3 - 3.15.118.255
ec2 - slave-4 - 3.23.132.22

Key file to login: crossroad.pem
aws_access_key_id='AKIAIIDE2YIOSM5QN46A'
aws_secret_access_key='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'

Scripts:
Master.py - deployed on master ec2
Client1.py - deployed on slave-1 ec2
Client2.py - deployed on slave-2 ec2
Client3.py - deployed on slave-3 ec2
Client4.py - deployed on slave-4 ec2
lambda_readS3_sendSQS.py - deployed in Lambda1
lambda_readSQS_writeDynamoDB.py - deployed in Lambda2

code at location: /home/ubuntu/crossroad

Cron: 0 * * * * python3 /home/ubuntu/crossroad/Client4.py
crontab -l
#Setup on all slave ec2 instances client scripts run every hour

Process:
1. Master is running continuosly. Logs are at /home/ubuntu/crossroad/nohup.out
2. At 0th minute of each hour, each of the slave nodes send a message to master asynchronously to process,
the master node check if any other slave is being processed or not, if not, it replies to slave to start process.
However, if it finds that someone is processing, it asks the slave to wait. Every 2 seconds,
slaves poll master until green signal is received.
3. Once slave gets green signal, it gets input from S3 input bucket by randomly choose a direction available in
one of the four input files.
4. There is a sleep time of 10 seconds to simulate the traffic (assume car is too slow to cross a signal and takes 10 secs)
5. After this, the message is stored to output file in S3 output bucket with filename as client name and content as direction.
6. There is a lambda1 trigger enabled on S3 output bucket, so as soon as output stored in S3, the lambda sends the
  direction,client_name to SQS.
7. Again on SQS, a Lambda2 trigger is enabled, so as soon as message is found on SQS, the message is processed and data is
stored in DynamoDB as id,client_name,date_time,direction.
