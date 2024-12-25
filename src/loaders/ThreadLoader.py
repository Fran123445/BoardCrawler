from loaders.Loader import Loader
from models.models import AttachedFile

class ThreadLoader(Loader):

    def _insert_threads(self, cursor, thread_list, board_id):
        thread_tuples = []

        for thread in thread_list:
            thread_tuples.append((board_id, thread.thread_number, thread.title))

        cursor.executemany('EXEC uspInsertThread ?, ?, ?', thread_tuples)

    def _get_post_tuple(self, post, board_id, thread_number):
        post_tuple = (board_id,
                       post.post_id,
                       post.anon_name,
                       post.anon_id,
                       post.anon_country,
                       post.creation_time,
                       post.content,
                       thread_number)

        return post_tuple

    def _get_mentioned_posts(self, post, board_id):
        mentioned_posts_tuples = []

        for post_mentioned in post.posts_metioned:
            mentioned_posts_tuples.append((board_id, post.post_id, post_mentioned))

        return mentioned_posts_tuples

    def _get_file_tuple(self, board_id, post_id, file: AttachedFile):
        return (board_id, post_id, file.filename, file.file_timestamp, file.extension, file.size, file.width, file.height)

    def _insert_posts(self, cursor, thread_list, board_id):
        post_tuples = []
        mentioned_posts_tuples = []
        attached_file_tuples = []

        for thread in thread_list:
            for post in thread.posts:
                post_tuple = self._get_post_tuple(post, board_id, thread.thread_number)
                mentioned_posts = self._get_mentioned_posts(post, board_id)

                if post.file:
                    attached_file_tuple = self._get_file_tuple(board_id, post.post_id, post.file)
                    attached_file_tuples.append(attached_file_tuple)

                mentioned_posts_tuples.extend(mentioned_posts)
                post_tuples.append(post_tuple)

        cursor.executemany('EXEC uspInsertPost ?,?,?,?,?,?,?,?', post_tuples)

        if mentioned_posts_tuples:
            cursor.executemany('EXEC uspInsertMentionedPost ?,?,?', mentioned_posts_tuples)
        cursor.executemany('EXEC uspInsertAttachedFile ?,?,?,?,?,?,?,?', attached_file_tuples)

    def bulk_load(self, data_list: list):
        cursor = self.conn.cursor()
        cursor.execute('SELECT dbo.findBoardId(?)', (data_list[0].board_name))
        board_id = cursor.fetchone()[0]

        self._insert_threads(cursor, data_list, board_id)
        self._insert_posts(cursor, data_list, board_id)
        cursor.commit()

