"""Client to output chat transcriptions."""

import asyncio
import openai

import util


chat_label = "Franz"

prompt = """
Complete this dialog by completing the last line of dialog, spoken by "{}". Add only one line.

Dialog:
{}
{}:
"""

def generate_prompt(lines):
    return prompt.format(chat_label, '\n'.join(lines), chat_label)

# def normalize_chat_line(text):
#     try:
#         lines = text.split('\n')
#         last_line = lines.pop().strip()
#     except Exception:
#         return None
#     if last_line.startswith(chat_label):
#         return last_line
#     return None

async def chat_line(lines):
    response = await openai.Completion.acreate(
        # "gpt-4" "gpt-3.5-turbo" "text-davinci-003"
        model="text-davinci-003",
        prompt=generate_prompt(lines),
        temperature=0.6)
    #return normalize_chat_line(response.choices[0].text)
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
