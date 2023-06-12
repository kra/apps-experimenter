"""Client to write attibuted transcription lines."""

import asyncio

import util

def write_line(sid, text):
    # Q&D test, log the line.
    util.log("{}: {}".format(sid, text), 'lines')

def read_lines():
    try:
        with open('/tmp/lines', 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def line_label(line):
    return line.split(':')[0]

def latest_line_label():
    try:
        return line_label(read_lines()[-1])
    except IndexError:
        return None

class Client():
    def __init__(self, socket):
        # We only want the stream_sid, but we have to store the socket
        # because it doesn't have it yet.
        self.socket = socket
        self.recv_queue = asyncio.Queue()
    async def start(self):
        pass
    def stop(self):
        pass
    def add_request(self, text):
        # Q&D test, log the line.
        write_line(self.socket.stream_sid, text)
        self.recv_queue.put_nowait(text)
    async def receive_response(self):
        """Generator for responses."""
        while True:
            yield await self.recv_queue.get()
