

def lambda_handler(event, context):
    for record in event['Records']:
        try:
            print ("test")
            payload=record["body"]
            print(str(payload))
        except Exception as e:
            print(str(e))
            print("EXCEPTION OCCURED!")
