import asyncio
from db import get_db
from struct import unpack
import json
from parkinglot import parkings


async def cleanup_background_tasks(app):
    app['mbed'].close()
    await app['mbed'].wait_closed()


def setup(app, from_ws, to_ws, loop):
    app['mbed'] = loop.run_until_complete(asyncio.start_server(
        embeddedhandler(from_ws, to_ws), '0.0.0.0', 8000, loop=loop))
    app.on_cleanup.append(cleanup_background_tasks)


def embeddedhandler(from_ws, to_ws):
    async def connected(module_id):
        print(f'connected {module_id.hex()}')
    async def disconnected(module_id):
        print(f'disconnected {module_id.hex()}')
    async def parkinglotstatus(module_id, parkingmask):
        print(f'status {module_id.hex()} {parkingmask.hex()}')
        event = {
                    'type': 'UPDATE',
                    'args': []
                }
        for i, byte in enumerate(bin(ord(parkingmask)).strip('0b')):
            key = module_id.hex() + i
            available = byte == '1'
            if parkings[key]['available'] != available:
                event['args'].append([key, parkings[key]])
                parkings[key]['available'] = available

        if len(event['args']) > 0:
            await to_ws.put(json.dumps(event))

    async def gaterequest(module_id, card_id):
        print(f'gate {module_id.hex()} {card_id.hex()}')
        user_id = unpack('>i', card_id)[0]
        c = get_db().execute(
                'select * from User where ID_User = ?', [user_id]
            )
        row = c.fetchone()
        event = {
                    'type': 'GATE',
                    'args': {
                        'success': user_id,
                        'id': row is not None
                    }
                }
        tasks = [to_ws.put(json.dumps(event))]
        if row is not None:
            tasks.append(from_ws.put(b'\x02\x07\x03\x01\x01'))

        await asyncio.wait(tasks)

    router = {
        b'\x00': connected,
        b'\x01': disconnected,
        b'\x02\x00': parkinglotstatus,
        b'\x02\x02': gaterequest
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
                module_id = await reader.readexactly(1)
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
