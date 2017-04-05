import asyncio
from db import get_db
from struct import unpack

def embeddedhandler(from_ws, to_ws):
    async def connected(module_id):
        pass
    async def disconnected(module_id):
        pass
    async def parkinglotstatus(module_id, parkingmask):
        pass
    async def gaterequest(module_id, card_id):
        c = get_db().execute(
                'select * from User where ID_User = ?', [unpack('>i', card_id)[0]]
            )
        row = c.fetchone()
        if row is not None:
            await from_ws.put(b'\x03' + module_id)

    router = {
        b'\x00': connected,
        b'\x01': disconnected,
        b'\x02\x00': parkinglotstatus,
        b'\x02\x01': gaterequest
    }
    async def handler(reader, writer):
        loop = asyncio.get_event_loop()
        async def command_writer():
            while True:
                data = await from_ws.get()
                writer.write(data)
                await writer.drain()
                from_ws.task_done()
        writetask = loop.create_task(command_writer())

        try:
            while True:
                frame_id = await reader.readexactly(1)
                route = frame_id
                module_id = await reader.readexactly(4)
                args = [module_id]
                if ord(frame_id) >= 2:
                    function_id = await reader.readexactly(1)
                    argc = await reader.readexactly(1)
                    argv = await reader.readexactly(ord(argc))
                    args += [argv]
                    route = route + function_id

                if route not in router:
                    print(f'warning unknown function code: {route.hex()}')
                else:
                    await router[route](*args)
        except:
            pass
        finally:
            await from_ws.join()
            writetask.cancel()
            writer.close()
    return handler
