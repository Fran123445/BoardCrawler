from models.models import Board

class BoardTransformer:

    def transformBoard(self, raw_board_data):
        board_name = raw_board_data['board']
        board_title = raw_board_data['title']

        return Board(board_name=board_name, title=board_title)

    def transformBoardList(self, raw_board_list):
        board_list = []

        for raw_board_info in raw_board_list:
                board_list.append(self.transformBoard(raw_board_info))

        return board_list