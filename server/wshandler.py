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
        print(payload)
        event = json.loads(payload)
        print(event)
        if True:
            print(len(app['websockets']))
            for ws in app['websockets']:
                ws.send_str(
                    json.dumps(
                        {
                            'type': 'GATE',
                            'args': {
                                'success': event['gate'],
                                'id': event['id']
                            }
                        }
                    )
                )
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
                key = ','.join(map(str, event['args']['position']))
                await request.app['to_mbed'].put("reservation " + key)
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
        else:
            break

    request.app['websockets'].remove(ws)

    return ws
