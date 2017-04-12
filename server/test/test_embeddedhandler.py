import sys, os
import unittest
import asyncio
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from embeddedhandler import embeddedhandler
from parkinglot import users

class MockedWriter():

    def __init__(self):
        self.result = b""

    def write(self, data):
        self.result += data

    async def drain(self):
        pass

    def close(self):
        pass

class MockedReader():

    def __init__(self, to_write):
        self.to_write = to_write
        self.cursor = 0

    async def readexactly(self, n):
        chunk = self.to_write[self.cursor:self.cursor + n]
        if len(chunk) == n:
            self.cursor += n
            return chunk
        else:
            self.cursor = len(self.to_write)
            raise Exception()

class TestMbedHandler(unittest.TestCase):

    def test_open_gaterequest(self):
        reader = MockedReader(b'\x02\xaa\x02\x04\x00\x00\x00\x7b')
        writer = MockedWriter()
        users['0000007b'] = True
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(embeddedhandler(asyncio.Queue(), asyncio.Queue())(reader, writer))
        loop.close()
        self.assertEqual(writer.result, b'\x02\x07\x03\x01\x01')

    def test_7segments(self):
        reader = MockedReader(b'\x02\x01\x00\x01\x03' + b'\x02\x02\x00\x01\x02')
        writer = MockedWriter()
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(embeddedhandler(asyncio.Queue(), asyncio.Queue())(reader, writer))
        loop.close()
        self.assertEqual(writer.result, b'\x02\x03\x04\x044\xff\xff6' + b'\x02\x03\x04\x044\xff\xff5')


unittest.main()
