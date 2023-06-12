#!/usr/bin/env python3

import asyncio
import dotenv

dotenv.load_dotenv()
import chat

lines = [
    "97d2dfd2-cfb1-4efd-ae64-d02918ca7a47: hello?",
    "4c36ec80-cd51-4e9f-b5ba-1776bafee738: hello!",
    "Chat: who is this?",
    "97d2dfd2-cfb1-4efd-ae64-d02918ca7a47: hello"]

async def main():
    print(await chat.chat_line(lines))

asyncio.run(main())
