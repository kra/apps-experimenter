"""Text to speech client."""

import asyncio
import itertools
import random
from google.cloud import texttospeech_v1

import util

voices = [
    "en-US-Standard-A",
    "en-US-Standard-B",
    "en-US-Standard-C",
    "en-US-Standard-D",
    "en-US-Standard-E",
    "en-US-Standard-F",
    "en-US-Standard-G",
    "en-US-Standard-H",
    "en-US-Standard-I",
    "en-US-Standard-J",
    "en-US-News-K",
    "en-US-News-L",
    "en-US-News-M",
    "en-US-News-N",
    "en-US-Studio-M",
    "en-US-Studio-O",
    "en-US-Polyglot-1"]
voices = random.sample(voices, len(voices))
voices = itertools.cycle(voices)

audio_config = texttospeech_v1.AudioConfig()
audio_config.audio_encoding = "MULAW"
audio_config.sample_rate_hertz = 8000


class Client:
    """
    Class to take string requests and give chunk responses.
    Yields result chunks with recieve_response().
    Call start() to begin. Call stop() to stop.
    Call add_request() to add strings.
    """
    def __init__(self):
        self._send_queue = asyncio.Queue() # Text to send to server.
        self._recv_queue = asyncio.Queue() # Bytes received from server.
        self._client = None
        self.voice = texttospeech_v1.VoiceSelectionParams()
        self.voice.language_code = "en-US"
        self.voice.name = next(voices)

    async def start(self):
        """
        Process our requests and enqueue chunk response.
        """
        util.log("text to speech client starting")
        self._client = texttospeech_v1.TextToSpeechAsyncClient()
        self.response_task = asyncio.create_task(self.response_iter())

    def stop(self):
        """Stop sending requests to the client."""
        # We should clear the queue also.
        self.response_task.cancel()
        self._client = None
        util.log("text to speech client stopped")

    async def response_iter(self):
        async for request in self.request_generator():
            response = await self._client.synthesize_speech(
                request=request)
            chunk = util.wav_to_chunk(response.audio_content)
            self._recv_queue.put_nowait(chunk)

    async def receive_response(self):
        """Generator for received media chunks."""
        while True:
            yield await self._recv_queue.get()
            util.log(f"text to speech sent response in {self.voice.name}")

    def add_request(self, text):
        """Add text to the processing queue."""
        self._send_queue.put_nowait(text)

    async def request_generator(self):
        while True:
            text = await self._send_queue.get()
            util.log(f"text to speech received request: {text}")
            yield self.text_to_request(text)

    def text_to_request(self, text):
        input_ = texttospeech_v1.SynthesisInput()
        input_.text = text
        return texttospeech_v1.SynthesizeSpeechRequest(
            input=input_,
            voice=self.voice,
            audio_config=audio_config)
