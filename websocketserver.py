#!/usr/bin/env python

import asyncio
import base64
import json
import time
import uuid
import websockets

import transcription
import util

send_qsize_log = 2
recv_qsize_log = 3

#host = "localhost"
port = 6000

class Server:

    def __init__(self):
        """Yields media chunks with recieve_media()."""
        self.server = None
        self._stream_sid = None
        self._send_queue = asyncio.Queue() # Bytes to send to socket.
        self._recv_queue = asyncio.Queue() # Bytes received from socket.

    async def start(self):
        util.log("websocket server starting")
        self.server = await websockets.serve(self.handler, port=port)

    async def stop(self):
        await self.server.close()
        raise NotImplementedError

    async def receive_response(self):
        """Generator for received media chunks."""
        while True:
            yield await self._recv_queue.get()
            qsize = self._recv_queue.qsize()
            if qsize >= recv_qsize_log:
                util.log(f"websocket recv queue size {qsize}")

    def add_request(self, buffer):
        """Add a chunk of bytes to the sending queue."""
        buffer = bytes(buffer)
        self._send_queue.put_nowait(buffer)
        qsize = self._send_queue.qsize()
        if qsize >= send_qsize_log:
            util.log(f"websocket send queue size {qsize}")

    def _enqueue_media(self, message):
        """Add a chunk of bytes to the receiving queue."""
        media = message["media"]
        chunk = base64.b64decode(media["payload"])
        self._recv_queue.put_nowait(chunk)

    # def mark_message(self):
    #     """
    #     Return a mark message which can be sent to the Twilio websocket.
    #     """
    #     return {"event": "mark",
    #             "streamSid": self._stream_sid,
    #             "mark": {"name": uuid.uuid4().hex}}

    async def consumer_handler(self, websocket):
        """
        Handle every message in websocket until we receive a stop
        message or barf.
        """
        util.log("websocket connection opened")
        async for message in websocket:
            message = json.loads(message)
            if message["event"] == "connected":
                util.log(f"websocket received event 'connected': {message}")
            elif message["event"] == "start":
                util.log(f"websocket received event 'start': {message}")
                if self._stream_sid and self._stream_sid != message['streamSid']:
                    raise Exception("Unexpected new streamSid")
                self._stream_sid = message['streamSid']
            elif message["event"] == "media":
                # util.log("Received event 'media'")
                # This assumes we get messages in order, we should instead
                # verify the sequence numbers? Or just skip?
                # message["sequenceNumber"]
                self._enqueue_media(message)
            elif message["event"] == "stop":
                util.log(f"websocket received event 'stop': {message}")
                self._stream_sid = None
                break
            elif message["event"] == "mark":
                util.log(f"websocket received event 'mark': {message}")
        util.log("websocket connection closed")

    async def producer_handler(self, websocket):
        """ Wait for messages from our send queue, and send them to the websocket."""
        while True:
            chunk = await self._send_queue.get()
            payload = base64.b64encode(chunk).decode()
            await websocket.send(
                json.dumps(
                    {"event": "media",
                     "streamSid": self._stream_sid,
                     "media": {"payload": payload}}))
            util.log("websocket sent response")

    async def handler(self, websocket):
        """
        Set up, run, and tear down consumer and producer tasks
        for this websocket connection.
        """
        util.log("websocket connection opened")
        done, pending = await asyncio.wait(
            [asyncio.create_task(self.consumer_handler(websocket)),
             asyncio.create_task(self.producer_handler(websocket))],
            return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
        util.log("websocket connection closed")
