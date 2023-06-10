"""Client to output chat transcriptions."""

import asyncio
import openai

import util


prompt = """
Complete this dialog.

Moe: Hello!
Larry: Who are you?
Moe: I am Jimmy, who is this?
Larry: I am Mary.
Curly: I have an idea.
Larry: What are we supposed to be doing?
Curly:
"""

def generate_prompt(lines):
    return prompt

async def chat_line(lines):
    response = await openai.Completion.acreate(
        # "gpt-4" "gpt-3.5-turbo" "text-davinci-003"
        model="text-davinci-003",
        prompt=generate_prompt(lines),
        temperature=0.6)
    return response.choices[0].text


class Client():
    """Client to pass requests directly to responses."""
    def __init__(self):
        self.recv_queue = asyncio.Queue()
    async def start(self):
        util.log("chatbot client starting")
    def stop(self):
        util.log("chatbot client stopped")
    def add_request(self, text):
        self.recv_queue.put_nowait(text)
    async def receive_response(self):
        """Generator for responses."""
        while True:
            yield await self.recv_queue.get()
            util.log(f"chatbot sent response")
