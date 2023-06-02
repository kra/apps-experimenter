import asyncio
from google.cloud import texttospeech_v1

import util

voice = texttospeech_v1.VoiceSelectionParams()
voice.language_code = "en-US"
audio_config = texttospeech_v1.AudioConfig()
audio_config.audio_encoding = "MULAW"
audio_config.sample_rate_hertz = 8000

class Client:
    """
    Class to process and emit speech.
    Calls callback with responses.
    Call add_request() to add text.
    """
    def __init__(self):
        self._send_queue = asyncio.Queue() # Text to send to server.
        self._recv_queue = asyncio.Queue() # Bytes received from server.
        self._client = None

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
            response = await self._client.synthesize_speech(request=request)
            chunk = util.wav_to_chunk(response.audio_content)
            self._recv_queue.put_nowait(chunk)

    async def receive_response(self):
        """Generator for received media chunks."""
        while True:
            yield await self._recv_queue.get()
            util.log(f"text to speech sent response")

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
            voice=voice,
            audio_config=audio_config)
