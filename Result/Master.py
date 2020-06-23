import asyncio
import websockets

file1Free = True


async def hello(websocket, path):
    while True:
        global file1Free

        name = await websocket.recv()
        print(f"{name}")

        client = f"{name} can start"

        if file1Free == True:
            file1Free = False
            print("!!")
            await websocket.send(client)
            status = await websocket.recv()
            if "finished" in f"{status}":
                file1Free = True
                print(f"{status}")
                break;
        else:
            await websocket.send("please wait")
            continue


start_server = websockets.serve(hello, "172.31.40.21", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
