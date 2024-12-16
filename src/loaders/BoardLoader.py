from loaders.Loader import Loader

class BoardLoader(Loader):

        def bulk_load(self, data_list: list):
            sql_query = 'EXEC uspInsertBoard ?, ?'
            cursor = self.conn.cursor()
            board_tuples = []

            for board in data_list:
                board_tuples.append((board.board_name, board.title))

            cursor.executemany(sql_query, board_tuples)
            cursor.commit()