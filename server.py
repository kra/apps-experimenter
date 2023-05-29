#!/usr/bin/env python

import asyncio
import functools

#import speech
import util
#import transcription
import websocketserver

# def save_chunk(chunk):
#     # testing
#     now = time.time()
#     filename = f"chunk{now}"
#     with open(filename, "ab") as f:
#         f.write(chunk)

# def pipeline_task(producer, consumer):
#     """Return task to send producer messages to consumer."""
#     async def step_generator():
#         """ Async generator to receive from producer and send to consumer."""
#         async for item in producer.receive_response():
#             consumer.add_request(item)
#     step_task = asyncio.create_task(step_generator())
#     return step_task

async def main():
    util.log("server starting")
    #speaker = speech.Client()
    #transcriber = transcription.SpeechClientBridge()
    websocket = websocketserver.Server()

    #(speaker_to_websocket_task, speaker_task) = pipeline_tasks(speaker, websocket)
    #(transcriber_to_speaker_task, transcriber_task) = pipeline_tasks(transcriber, speaker)
    await websocket.start()
    util.log("xxx foo")
    await asyncio.Event().wait()
    # producer_tasks = []
    # producer_tasks.append(pipeline_task(websocket, transcriber))
    # util.log("xxx bar")
    # # We should gather these if we want to be able to shut down or cancel.
    # await asyncio.wait(producer_tasks, return_when=asyncio.FIRST_COMPLETED)
    # util.log("a task completed") # XXX This is an error.
    # #await transcriber_task
    # #await transcriber_to_speaker_task
    # #await speaker_task
    # #await speaker_to_websocket_task

asyncio.run(main())