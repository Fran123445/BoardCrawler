import asyncio

import aiohttp
from models.models import Thread, Board

class ReplyExtractor:

    def __init__(self, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore):
        self.session = session
        self.semaphore = semaphore

    async def extractReplies(self, board: Board, thread: Thread):
        url = f"https://boards.4chan.org/{board.board_name}/thread/{thread.thread_number}/"

        async with self.semaphore:
            async with self.session.get(url) as response:
                return await response.text()

