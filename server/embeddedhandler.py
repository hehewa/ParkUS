import asyncio
from db import get_db

def embeddedhandler(from_ws, to_ws):
    async def handler(reader, writer):
        loop = asyncio.get_event_loop()
        async def command_writer():
            while True:
                data = await from_ws.get()
                print("got " + data)
                #writer.write(data)
                #await writer.drain()
        writetask = loop.create_task(command_writer())

        async for message in reader:
            print("Send: %r" % message)

        writetask.cancel()
        writer.close()
    return handler
