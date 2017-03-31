import asyncio
from aiohttp import web
import json
from parkinglot import parkings

async def wshandler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].append(ws)

    async for msg in ws:
        if msg.type == web.MsgType.text:
            event = json.loads(msg.data)
            if event["type"] == "connection":
                await ws.send_str(json.dumps({'type':'FULL_SYNC', 'args':list(parkings.items())}))
            elif event["type"] == "RESERVATION":
                key = ','.join(map(str,event['args']['position']))
                await request.app['to_mbed'].put("reservation " + key)
                if parkings[key]['reserved'] != event['args']['reserved']:
                    parkings[key]['reserved'] = event['args']['reserved']
                    for _ws in request.app['websockets']:
                        _ws.send_str(json.dumps({'type':'UPDATE', 'args':[[key, parkings[key]]]}))
        elif msg.type == web.MsgType.binary:
            await ws.send_bytes(msg.data)
        elif msg.type == web.MsgType.close:
            break

    request.app['websockets'].remove(ws)

    return ws
