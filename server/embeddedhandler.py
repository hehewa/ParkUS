import asyncio
from db import get_db
from struct import unpack
import json
from parkinglot import parkings, users


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
        if module_id == b'\x03':
            left, right = count_spots()
            await update_spots(left, right)
    async def disconnected(module_id):
        print(f'disconnected {module_id.hex()}')
    async def parkinglotstatus(module_id, parkingmask):
        print(f'status {module_id.hex()} {parkingmask.hex()}')
        event = {
                    'type': 'UPDATE',
                    'args': []
                }
        for i, byte in enumerate(bin(ord(parkingmask))[2:].zfill(8)):
            key = module_id.hex() + str(7-i)
            available = byte == '0'
            if key in parkings and parkings[key]['available'] != available:
                if parkings[key]['available']:
                    parkings[key]['reserved'] = False
                parkings[key]['available'] = available
                event['args'].append([key, parkings[key]])

        if len(event['args']) > 0:
            await to_ws.put(json.dumps(event))
            left, right = count_spots()
            await update_spots(left, right)

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
                        'success': row is not None,
                        'full': sum(count_spots()) == 0,
                        'id': user_id
                    }
                }
        tasks = []
        if card_id.hex() in users and users[card_id.hex()]:
            users[card_id.hex()] = False
            tasks.append(from_ws.put(b'\x02\x07\x03\x01\x01'))
        else:
            if not event['args']['full'] and event['args']['success']:
                users[card_id.hex()] = True
            tasks.append(to_ws.put(json.dumps(event)))

        await asyncio.wait(tasks)

    async def update_spots(left, right):
        await from_ws.put(b'\x02\x03\x04\x04' + bytes([left + 0x30]) + b'\xff\xff' + bytes([right + 0x30]))

    def count_spots():
        left = sum(value['available'] and key[:2] == '01' for key, value in parkings.items())
        right = sum(value['available'] and key[:2] == '02' for key, value in parkings.items())
        return left, right

    router = {
        b'\x00': connected,
        b'\x01': disconnected,
        b'\x02\x00': parkinglotstatus,
        b'\x02\x02': gaterequest
    }
    async def handler(reader, writer):
        loop = asyncio.get_event_loop()
        print("new connection")
        async def command_writer():
            while True:
                data = await from_ws.get()
                print(f'sending {data.hex()}')
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
        except Exception as e:
            print(f"exception {e.args} {type(e).__name__}")
            print(f"{e}")
        finally:
            print("end connection")
            await from_ws.join()
            writetask.cancel()
            writer.close()
            print("closed connection")
    return handler
