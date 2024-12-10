import requests

class BoardExtractor:

    def extractBoards(self):
        boards_response = requests.get('https://a.4cdn.org/boards.json')
        boards_json = boards_response.json()
        board_list = boards_json['boards']

        return board_list