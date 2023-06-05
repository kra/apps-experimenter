#!/usr/bin/env python

import asyncio
import base64
import json
import time
import uuid
import websockets

import pipeline
import speech
import transcription
import util

#host = "localhost"
port = 6000

class Server:

    def __init__(self):
        """Yields media chunks with recieve_media()."""
        self.server = None
        self._stream_sid = None

    async def start(self):
        util.log("websocket server starting")
        self.server = await websockets.serve(self.handler, port=port)

    async def stop(self):
        await self.server.close()
        raise NotImplementedError

    def _message_to_chunk(self, message):
        return base64.b64decode(message["media"]["payload"])

    # def mark_message(self):
    #     """
    #     Return a mark message which can be sent to the Twilio websocket.
    #     """
    #     return {"event": "mark",
    #             "streamSid": self._stream_sid,
    #             "mark": {"name": uuid.uuid4().hex}}

    async def get_pipeline(self):
        """ Return a client pipeline for chunk requests and responses."""
        line = pipeline.Composer(transcription.Client(), speech.Client())
        await line.start()
        return line

    async def consumer_handler(self, line, websocket):
        """
        Handle every message in websocket until we receive a stop
        message or barf.
        """
        util.log("websocket connection opened")
        async for message in websocket:
            message = json.loads(message)
            if message["event"] == "connected":
                util.log(
                    f"websocket received event 'connected': {message}")
            elif message["event"] == "start":
                util.log(f"websocket received event 'start': {message}")
                if (self._stream_sid and
                    self._stream_sid != message['streamSid']):
                    raise Exception("Unexpected new streamSid")
                self._stream_sid = message['streamSid']
            elif message["event"] == "media":
                # util.log("Received event 'media'")
                # This assumes we get messages in order, we should instead
                # verify the sequence numbers? Or just skip?
                # message["sequenceNumber"]
                line.add_request(self._message_to_chunk(message))
            elif message["event"] == "stop":
                util.log(f"websocket received event 'stop': {message}")
                self._stream_sid = None
                break
            elif message["event"] == "mark":
                util.log(f"websocket received event 'mark': {message}")
        util.log("websocket connection closed")

    async def producer_handler(self, line, websocket):
        """
        Iterate over messages from line, and send them to
        the websocket.
        """
        async for chunk in line.receive_response():
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
        line = await self.get_pipeline()
        done, pending = await asyncio.wait(
            [asyncio.create_task(self.consumer_handler(line, websocket)),
             asyncio.create_task(self.producer_handler(line, websocket))],
            return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
        line.stop()
        util.log("websocket connection closed")

