import asyncio

import aiohttp
from models.models import Thread, Board

class ThreadExtractor:

    def __init__(self, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore):
        self.session = session
        self.semaphore = semaphore

    async def extract_thread(self, board: Board, thread: Thread):
        url = f"https://a.4cdn.org/{board.board_name}/thread/{thread.thread_number}.json"

        async with self.semaphore:
            async with self.session.get(url) as response:
                return await response.json()

    async def generate_extraction_tasks(self, board: Board, catalogue: list):
        tasks = []

        for thread in catalogue:
            task = asyncio.create_task(self.extract_thread(board, thread))
            tasks.append(task)

        raw_threads = await asyncio.gather(*tasks)

        return raw_threads