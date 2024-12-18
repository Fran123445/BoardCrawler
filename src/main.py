import asyncio
import concurrent.futures

import pyodbc
import aiohttp
from extractors.BoardExtractor import BoardExtractor
from src.extractors.ThreadExtractor import ThreadExtractor
from src.extractors.CatalogExtractor import CatalogExtractor
from src.transformers.BoardTransformer import BoardTransformer
from src.transformers.ThreadTransformer import ThreadTransformer
from src.transformers.CatalogTransformer import CatalogTransformer
from src.loaders.BoardLoader import BoardLoader
from src.loaders.ThreadLoader import ThreadLoader
from src.transformers.FileTransformer import  FileTransfomer

async def main():
    # Will eventually be divided into different classes or functions, but for now it's this

    connection = pyodbc.connect() # a config file will handle this, among other things

    session = aiohttp.ClientSession()
    sem = asyncio.Semaphore(10)

    board_extractor = BoardExtractor()
    catalog_extractor = CatalogExtractor()
    thread_extractor = ThreadExtractor(session, sem)

    board_transformer = BoardTransformer()
    catalog_transformer = CatalogTransformer()
    file_transformer = FileTransfomer()
    thread_transformer = ThreadTransformer(file_transformer)

    board_loader = BoardLoader(connection)
    thread_loader = ThreadLoader(connection)

    raw_boards = board_extractor.extract_boards()
    boards = board_transformer.transform_board_list(raw_boards)
    board_loader.bulk_load(boards)

    executor = concurrent.futures.ProcessPoolExecutor()
    total_amount = len(boards)
    current = 1
    futures = []

    for board in boards:
        print(f"Scraping /{board.board_name}/ - {current}/{total_amount}")
        current += 1

        if board.board_name == 'f':
            # it crashes. Probably something to do with the filetype, haven't
            # really looked into it yet.
            continue

        raw_catalog = catalog_extractor.extract_catalog(board)
        catalog = catalog_transformer.transform_catalog(board, raw_catalog)

        raw_threads = await thread_extractor.generate_extraction_tasks(board, catalog)

        for i in range(0, len(catalog)):
            futures.append(executor.submit(thread_transformer.transform_thread, catalog[i], raw_threads[i]))

        concurrent.futures.wait(futures)

        results = [future.result() for future in futures]

        thread_loader.bulk_load(results)

        futures.clear()

    executor.shutdown(wait=True)
    await session.close()

if __name__=='__main__':
    asyncio.run(main())