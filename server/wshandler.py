import asyncio
from aiohttp import web
import json
from parkinglot import parkings


async def start_background_tasks(app):
    app['wsbroadcast'] = app.loop.create_task(wsbroadcast(app))


async def cleanup_background_tasks(app):
    app['wsbroadcast'].cancel()


def setup(app, to_mbed, from_mbed):
    app['websockets'] = []
    app['to_mbed'] = to_mbed
    app['from_mbed'] = from_mbed
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)


async def wsbroadcast(app):
    while True:
        payload = await app['from_mbed'].get()
        for ws in app['websockets']:
            ws.send_str(payload)
        app['from_mbed'].task_done()


async def wshandler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].append(ws)

    async for msg in ws:
        if msg.type == web.MsgType.text:
            event = json.loads(msg.data)
            if event["type"] == "connection":
                await ws.send_str(json.dumps(
                    {'type': 'FULL_SYNC', 'args': list(parkings.items())})
                )
            elif event["type"] == "RESERVATION":
                key = event['args']['key']
                #await request.app['to_mbed'].put("reservation " + key)
                if parkings[key]['reserved'] != event['args']['reserved']:
                    parkings[key]['reserved'] = event['args']['reserved']
                    for ws in request.app['websockets']:
                        ws.send_str(
                            json.dumps(
                                {
                                    'type': 'UPDATE',
                                    'args': [[key, parkings[key]]]
                                }
                            )
                        )
                    module_id = key[:2].encode()
                    keys = [ module_id + spot_id for spot_id in map(str,range(8)) ]
                    #keys = filter(lambda x: x in parkings, keys)
                    keys = [ key for key in keys if key in parkings else None ]
                    mask = bytes([int(''.join([ '1' for key in keys if key is not None and parkings[key]['reserved'] else '0' ]), 2)])
                    await request.app['to_mbed'].put(b'\x02' + module_id + b'\x01\x01' + mask)
        else:
            break

    request.app['websockets'].remove(ws)

    return ws
