from bs4 import BeautifulSoup
from models.models import Reply, Thread

class ThreadTransformer:

    def __init__(self, file_transformer):
        self.file_transformer = file_transformer

    def _get_reply_id(self, container):
        return int(container.find('div', class_='post')['id'][1:])

    def _get_creation_time(self, container):
        date_time_span = container.find('span', class_='dateTime')
        return date_time_span['data-utc']

    def _get_content(self, container):
        post = container.find('blockquote', class_='postMessage')
        return post.get_text(separator='\n')

    def _get_replies_mentions(self, container):
        replies_metioned = []

        for a_tag in container.find_all('a', class_='quotelink', href=True):
            # Extract the reply number from the href and remove the #p
            ref = a_tag['href']

            if not ref.startswith('#p'):
                # Only consider references inside the same thread
                continue

            reply = ref[2:]

            replies_metioned.append(reply)

        return replies_metioned

    def _get_anon_name(self, container):
        name_span = container.find('span', class_='name')
        return name_span.get_text().strip() if name_span else None

    def _get_anon_id(self, container):
        posteruid_span = container.find('span', class_='posteruid')
        return posteruid_span.find('span', class_='hand').get_text().strip() if posteruid_span else None

    def _get_anon_country(self, container):
        flag_span = container.find('span', class_='flag')
        return flag_span['title'] if flag_span else None

    def _get_file(self, container):
        file_container = container.find('div', class_='fileText')

        if file_container == None:
            return None

        return self.file_transformer.transform_file(file_container)

    def transform_thread(self, thread: Thread, thread_html):
        soup = BeautifulSoup(thread_html, 'html.parser')

        post_containers = soup.find_all('div', class_='postContainer')
        for container in post_containers:
            reply_id = self._get_reply_id(container)
            creation_time = int(self._get_creation_time(container))
            anon_name = self._get_anon_name(container)
            anon_id = self._get_anon_id(container)
            anon_country = self._get_anon_country(container)
            attached_file = self._get_file(container)
            content = self._get_content(container)
            replies_metioned = self._get_replies_mentions(container)

            thread.replies.append(Reply(reply_id=reply_id,
                                 creation_time=creation_time,
                                 content=content,
                                 replies_metioned=replies_metioned,
                                 file=attached_file,
                                 anon_name=anon_name,
                                 anon_id=anon_id,
                                 anon_country=anon_country))