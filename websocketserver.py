#!/usr/bin/env python

import asyncio
import base64
import json
import time
import uuid
import websockets

import chat
import pipeline
import lines
import speech
import transcription
import util

#host = "localhost"
port = 6000


class Socket:
    def __init__(self, websocket):
        self.websocket = websocket
        self.line = None
        self.stream_sid = None


class FakeSocket:
    """Object to hold a line and a stream_sid identifier."""
    stream_sid = "chat"


class Server:
    def __init__(self):
        """Yields media chunks with recieve_media()."""
        self.server = None
        self.sockets = set()
        self.chat_socket = None

    async def start(self):
        util.log("websocket server starting")
        await self.fake_handler()
        await self.periodic_task()
        self.server = await websockets.serve(self.handler, port=port)

    # async def stop(self):
    #     await self.server.close()
    #     raise NotImplementedError

    async def chat_requester(self):
        """Return a chat line if the latest line is not a chat line."""
        if lines.latest_line_label() != "chat":
            return await chat.chat_line(None)

    async def periodic_task(self):
        """Return a task to do the periodic things."""
        async def p_d():
            while True:
                line = await self.chat_requester()
                if line:
                    self.chat_socket.line.add_request(line)
                await asyncio.sleep(10)
        return asyncio.create_task(p_d())

    def _message_to_chunk(self, message):
        return base64.b64decode(message["media"]["payload"])

    # def mark_message(self):
    #     """
    #     Return a mark message which can be sent to the Twilio websocket.
    #     """
    #     return {"event": "mark",
    #             "streamSid": self._stream_sid,
    #             "mark": {"name": uuid.uuid4().hex}}

    async def get_pipeline(self, socket):
        """ Return a client pipeline for chunk requests and responses."""
        line = pipeline.Composer(
            transcription.Client(), lines.Client(socket))
        line = pipeline.Composer(line, speech.Client())
        await line.start()
        return line

    async def consumer_handler(self, socket):
        """
        Handle every message in socket's websocket until we receive a stop
        message or barf.
        """
        util.log("websocket connection opened")
        async for message in socket.websocket:
            message = json.loads(message)
            if message["event"] == "connected":
                util.log(
                    f"websocket received event 'connected': {message}")
            elif message["event"] == "start":
                util.log(f"websocket received event 'start': {message}")
                #if (self._stream_sid and
                #    self._stream_sid != message['streamSid']):
                #    raise Exception("Unexpected new streamSid")
                socket.stream_sid = message['streamSid']
            elif message["event"] == "media":
                # util.log("Received event 'media'")
                # This assumes we get messages in order, we should instead
                # verify the sequence numbers? Or just skip?
                # message["sequenceNumber"]
                socket.line.add_request(self._message_to_chunk(message))
            elif message["event"] == "stop":
                util.log(f"websocket received event 'stop': {message}")
                #self._stream_sid = None
                break
            elif message["event"] == "mark":
                util.log(f"websocket received event 'mark': {message}")
        util.log("websocket connection closed")

    async def send(self, socket, chunk):
        """Send chunk to websocket in a media message."""
        payload = base64.b64encode(chunk).decode()
        await socket.websocket.send(
            json.dumps(
                {"event": "media",
                 "streamSid": socket.stream_sid,
                 "media": {"payload": payload}}))

    async def producer_handler(self, socket):
        """
        Iterate over messages from socket's line, and send them to
        the other websockets.
        """
        async for chunk in socket.line.receive_response():
            for s in self.sockets:
                if s != socket:
                    await self.send(s, chunk)
                    util.log(
                        f"websocket sent response from "
                        "{socket.stream_sid} to {s.stream_sid}")

    async def handler(self, websocket):
        """
        Set up, run, and tear down consumer and producer tasks
        for this websocket connection.
        """
        util.log("websocket connection opened")
        socket = Socket(websocket)
        line = await self.get_pipeline(socket)
        socket.line = line
        self.sockets.add(socket)
        util.log("websocket connections: {}".format(len(self.sockets)))
        done, pending = await asyncio.wait(
            [asyncio.create_task(self.consumer_handler(socket)),
             asyncio.create_task(self.producer_handler(socket))],
            return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
        line.stop()
        self.sockets.remove(socket)
        util.log("websocket connection closed")

    async def get_fake_handler_pipeline(self, socket):
        """
        Return a client pipeline for string requests and chunk responses.
        """
        line = pipeline.Composer(
            chat.Client(), lines.Client(socket))
        line = pipeline.Composer(line, speech.Client())
        await line.start()
        return line

    async def fake_handler(self):
        """
        Set up and run a producer task without a consumer.
        """
        # This isn't really a handler, because there is no consumer
        # callback. The fake chat_socket recives requests directly from
        # a task.
        socket = FakeSocket()
        line = await self.get_fake_handler_pipeline(socket)
        socket.line = line
        self.chat_socket = socket
        # We don't clean this up, we should do that in stop().
        asyncio.create_task(self.producer_handler(socket))
