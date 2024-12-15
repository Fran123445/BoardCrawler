import requests
from models.models import Board


class CatalogExtractor:
    """Extracts all threads from a given board"""

    def extractCatalog(self, board: Board):
        board_name = board.board_name

        catalog_response = requests.get(f"https://a.4cdn.org/{board_name}/catalog.json")
        board_catalog = catalog_response.json()

        return board_catalog