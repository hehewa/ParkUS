import sys, os
import unittest
import asyncio
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from embeddedhandler import embeddedhandler

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

    def test_gaterequest_success(self):
        reader = MockedReader(b"\x02\xaa\xbb\xcc\xdd\x01\x04\x00\x00\x00\x7b")
        writer = MockedWriter()
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(embeddedhandler(asyncio.Queue(), asyncio.Queue())(reader, writer))
        loop.close()
        self.assertEqual(writer.result, b"\x03\xaa\xbb\xcc\xdd")

    def test_gaterequest_fail(self):
        reader = MockedReader(b"\x02\xaa\xbb\xcc\xdd\x01\x04\xaa\xaa\xaa\x7b")
        writer = MockedWriter()
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(embeddedhandler(asyncio.Queue(), asyncio.Queue())(reader, writer))
        loop.close()
        self.assertEqual(writer.result, b"")


unittest.main()
