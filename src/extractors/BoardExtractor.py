import requests

class BoardFetcher:

    def fetchBoardNames():
        boards_response = requests.get('https://a.4cdn.org/boards.json')
        boards_json = boards_response.json()
        print(boards_json)


BoardFetcher.fetchBoardNames()