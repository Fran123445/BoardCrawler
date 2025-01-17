import asyncio
import time

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

async def main():
    connection = pyodbc.connect() # a config file will handle this, among other things

    session = aiohttp.ClientSession()
    sem = asyncio.Semaphore(25)

    board_extractor = BoardExtractor()
    catalog_extractor = CatalogExtractor()
    thread_extractor = ThreadExtractor(session, sem)

    board_transformer = BoardTransformer()
    catalog_transformer = CatalogTransformer()
    thread_transformer = ThreadTransformer()

    board_loader = BoardLoader(connection)
    thread_loader = ThreadLoader(connection)

    raw_boards = board_extractor.extract_boards()
    boards = board_transformer.transform_board_list(raw_boards)
    board_loader.bulk_load(boards)

    total_amount = len(boards)
    current = 1

    t1 = time.time()
    for board in boards:
        print(f"Scraping /{board.board_name}/ - {current}/{total_amount}")
        current += 1

        raw_catalog = catalog_extractor.extract_catalog(board)
        catalog = catalog_transformer.transform_catalog(board, raw_catalog)

        raw_threads = await thread_extractor.generate_extraction_tasks(board, catalog)
        thread_transformer.transform_threads_sequentially(catalog, raw_threads)

        thread_loader.bulk_load(catalog)

    await session.close()

if __name__=='__main__':
    asyncio.run(main())