import asyncio
import websockets
import time
from random import randrange
import boto3

INPUT_BUCKET = 'com.crossroad.input'
OUTPUT_BUCKET = 'com.crossroad.output'

s3 = boto3.resource('s3', aws_access_key_id='AKIAIIDE2YIOSM5QN46A',
                    aws_secret_access_key='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')


def read_file(bucket_name, file_name):
    obj = s3.Object(bucket_name, file_name)

    data = obj.get()['Body'].read().decode("utf-8")

    return data


def write_file(bucket_name, file_name, data):
    obj = s3.Object(bucket_name, file_name)
    obj.put(Body=data.encode("utf-8"))
    return True


success = False


async def hello():
    uri = "ws://3.12.138.58:8765"

    async with websockets.connect(uri) as websocket:
        global success

        idx = randrange(4) + 1

        direction = read_file(INPUT_BUCKET, str(idx) + '.txt')

        while success != True:

            await websocket.send('Client 3: ' + direction)
            print("message sent")
            print(f"{direction}")

            greeting = await websocket.recv()
            print(f"{greeting}")

            if "wait" in f"{greeting}":
                print(f"{greeting}")
                time.sleep(2)
                continue
            if "start" in f"{greeting}":
                print("client 3 started")
                time.sleep(10)
                message = "client 3 finished"
                print(f"{message}")
                await websocket.send(message)
                print("message sent for finish")

                write_file(OUTPUT_BUCKET, 'client_3.txt', direction)
                success = True


asyncio.get_event_loop().run_until_complete(hello())
