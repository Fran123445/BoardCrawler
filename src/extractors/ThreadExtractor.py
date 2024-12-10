import requests


class ThreadExtractor:
    """Extracts all threads from a given board"""

    def extractThreads(self, board_name):
        catalog_response = requests.get(f"https://a.4cdn.org/{board_name}/catalog.json")
        board_catalog = catalog_response.json()

        return board_catalog