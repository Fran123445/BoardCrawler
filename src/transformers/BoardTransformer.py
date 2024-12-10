from models.models import Board

class BoardTransformer:

    def transformBoard(self, raw_board_list):
        board_list = []

        for raw_board_info in raw_board_list:
            board_name = raw_board_info['board']
            board_title = raw_board_info['title']

            board_list.append(Board(board_name=board_name, title=board_title))

        return board_list