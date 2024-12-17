from loaders.Loader import Loader
from models.models import AttachedFile

class ThreadLoader(Loader):

    def _insert_threads(self, cursor, thread_list, board_id):
        thread_tuples = []

        for thread in thread_list:
            thread_tuples.append((board_id, thread.thread_number, thread.title))

        cursor.executemany('EXEC uspInsertThread ?, ?, ?', thread_tuples)

    def _get_reply_tuple(self, reply, board_id, thread_number):
        reply_tuple = (board_id,
                     reply.reply_id,
                     reply.anon_name,
                     reply.anon_id,
                     reply.anon_country,
                     reply.creation_time,
                     reply.content,
                     thread_number)

        return reply_tuple

    def _get_mentioned_replies(self, reply, board_id):
        mentioned_reply_tuples = []

        for reply_mentioned in reply.replies_metioned:
            mentioned_reply_tuples.append((board_id, reply.reply_id, reply_mentioned))

        return mentioned_reply_tuples

    def _get_file_tuple(self, board_id, reply_id, file: AttachedFile):
        return (board_id, reply_id, file.filename, file.file_timestamp, file.extension, file.size, file.width, file.height)

    def _insert_replies(self, cursor, thread_list, board_id):
        reply_tuples = []
        mentioned_reply_tuples = []
        attached_file_tuples = []

        for thread in thread_list:
            for reply in thread.replies:
                reply_tuple = self._get_reply_tuple(reply, board_id, thread.thread_number)
                mentioned_replies = self._get_mentioned_replies(reply, board_id)

                if reply.file:
                    attached_file_tuple = self._get_file_tuple(board_id, reply.reply_id, reply.file)
                    attached_file_tuples.append(attached_file_tuple)

                mentioned_reply_tuples.extend(mentioned_replies)
                reply_tuples.append(reply_tuple)

        cursor.executemany('EXEC uspInsertReply ?,?,?,?,?,?,?,?', reply_tuples)

        if mentioned_reply_tuples:
            cursor.executemany('EXEC uspInsertMentionedReply ?,?,?', mentioned_reply_tuples)
        cursor.executemany('EXEC uspInsertAttachedFile ?,?,?,?,?,?,?,?', attached_file_tuples)

    def bulk_load(self, data_list: list):
        cursor = self.conn.cursor()
        cursor.execute('SELECT dbo.findBoardId(?)', (data_list[0].board_name))
        board_id = cursor.fetchone()[0]

        self._insert_threads(cursor, data_list, board_id)
        self._insert_replies(cursor, data_list, board_id)
        cursor.commit()

