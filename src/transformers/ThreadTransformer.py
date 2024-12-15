from bs4 import BeautifulSoup
from models.models import Reply

class ThreadTransformer:

    def _get_reply_id(self, container):
        return int(container.find('div', class_='post')['id'][1:])

    def _get_creation_time(self, container):
        date_time_span = container.find('span', class_='dateTime')
        return date_time_span['data-utc']

    def _get_content(self, container):
        return [post.get_text(separator='\n') for post in container.find_all('blockquote', class_='postMessage')]

    def _get_replies_mentions(self, container):
        replies_metioned = []

        for a_tag in container.find_all('a', class_='quotelink'):
            # Extract the text content (e.g., >>103467046) and remove the ">>"
            reply = a_tag.text[2:]
            replies_metioned.append(reply)

        return replies_metioned

    def _get_filename(self, container):
        filename = None
        file_text_div = container.find('div', class_='fileText')
        if file_text_div:
            file_link = file_text_div.find('a')
            if file_link:
                filename = file_link.get_text()
        return filename

    def _get_anon_name(self, container):
        name_span = container.find('span', class_='name')
        return name_span.get_text().strip() if name_span else None

    def _get_anon_id(self, container):
        posteruid_span = container.find('span', class_='posteruid')
        return posteruid_span.find('span', class_='hand').get_text().strip() if posteruid_span else None

    def _get_anon_country(self, container):
        flag_span = container.find('span', class_='flag')
        return flag_span['title'] if flag_span else None

    def transformThread(self, thread_html):
        soup = BeautifulSoup(thread_html, 'html.parser')
        replies = []

        post_containers = soup.find_all('div', class_='postContainer')
        for container in post_containers:
            reply_id = self._get_reply_id(container)
            creation_time = int(self._get_creation_time(container))
            filename = self._get_filename(container)
            anon_name = self._get_anon_name(container)
            anon_id = self._get_anon_id(container)
            anon_country = self._get_anon_country(container)

            content = self._get_content(container)
            replies_metioned = self._get_replies_mentions(container)

            replies.append(Reply(reply_id=reply_id,
                                 creation_time=creation_time,
                                 content=content,
                                 replies_metioned=replies_metioned,
                                 filename=filename,
                                 anon_name=anon_name,
                                 anon_id=anon_id,
                                 anon_country=anon_country))

        return replies