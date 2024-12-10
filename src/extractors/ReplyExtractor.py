import requests


class ReplyExtractor:

    def extractReplies(self, board, thread_number):
        url = f"https://boards.4chan.org/{board}/thread/{thread_number}/"

        response = requests.get(url)

        return response.content

