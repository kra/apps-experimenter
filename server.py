#!/usr/bin/env python

import asyncio
import functools
import os

import pipeline
import speech
import transcription
import util
import websocketserver

# def save_chunk(chunk):
#     # testing
#     now = time.time()
#     filename = f"chunk{now}"
#     with open(filename, "ab") as f:
#         f.write(chunk)

async def main():
    util.log("server starting")
    speaker = speech.Client()
    transcriber = transcription.Client()
    websocket = websocketserver.Server()

    util.cred_kluge()

    line = pipeline.Composer(transcriber, speaker)
    await line.start()
    await websocket.start()
    producer_tasks = []
    producer_tasks.append(pipeline.pipeline_task(line, websocket))
    producer_tasks.append(pipeline.pipeline_task(websocket, line))

    await asyncio.wait(
        producer_tasks, return_when=asyncio.FIRST_COMPLETED)
    util.log("a task completed") # XXX This is an error.

asyncio.run(main())
