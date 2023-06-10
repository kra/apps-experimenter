#!/usr/bin/env python3

import asyncio
import dotenv

dotenv.load_dotenv()
import chat

async def main():
    print(await chat.chat_line(None))

asyncio.run(main())
