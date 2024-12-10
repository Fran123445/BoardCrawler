from models.models import Thread

class ThreadTransformer:

    def transformThreads(self, board, catalog):
        thread_list = []

        for page in catalog:
            raw_threads = page['threads']

            for raw_thread_data in raw_threads:
                thread_number = raw_thread_data['no']
                thread_title = raw_thread_data['sub'] if 'sub' in raw_thread_data else None

                thread = Thread(thread_number=thread_number, title=thread_title, board_name=board, replies=[])
                thread_list.append(thread)

        return thread_list