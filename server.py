#!/usr/bin/env python

import asyncio
import functools
import os

import speech
import util
import transcription
import websocketserver

# def save_chunk(chunk):
#     # testing
#     now = time.time()
#     filename = f"chunk{now}"
#     with open(filename, "ab") as f:
#         f.write(chunk)

def pipeline_task(producer, consumer):
    """Return task to send producer messages to consumer."""
    async def step_generator():
        """ Async generator to receive from producer and send to consumer."""
        async for item in producer.receive_response():
            consumer.add_request(item)
    step_task = asyncio.create_task(step_generator())
    return step_task

async def main():
    util.log("server starting")
    speaker = speech.Client()
    transcriber = transcription.SpeechClientBridge()
    websocket = websocketserver.Server()

    await speaker.start()
    await transcriber.start()
    await websocket.start()

    producer_tasks = []
    #foo = asyncio.create_task(asyncio.Event().wait())
    #producer_tasks.append(foo)
    producer_tasks.append(pipeline_task(speaker, websocket))
    producer_tasks.append(pipeline_task(transcriber, speaker))
    producer_tasks.append(pipeline_task(websocket, transcriber))

    util.log("xxx bar")
    await asyncio.wait(
        producer_tasks, return_when=asyncio.FIRST_COMPLETED)
    util.log("a task completed") # XXX This is an error.

asyncio.run(main())
