from bs4 import BeautifulSoup
from models.models import Post, Thread

class ThreadTransformer:

    def __init__(self, file_transformer):
        self.file_transformer = file_transformer

    def _get_post_id(self, container):
        return int(container['id'][2:])

    def _get_creation_time(self, container):
        date_time_span = container.find('span', class_='dateTime')
        return date_time_span['data-utc']

    def _get_content(self, container):
        post = container.find('blockquote', class_='postMessage')
        return post.get_text(separator='\n')

    def _get_posts_mentioned(self, container):
        posts_mentioned = []

        for a_tag in container.find_all('a', class_='quotelink', href=True):
            # Extract the post number from the href and remove the #p
            ref = a_tag['href']

            if not ref.startswith('#p'):
                # Only consider references inside the same thread
                continue

            post = ref[2:]

            posts_mentioned.append(post)

        return posts_mentioned

    def _get_anon_name(self, container):
        name_span = container.find('span', class_='name')
        return name_span.get_text()

    def _get_anon_id(self, container):
        posteruid_span = container.find('span', class_='posteruid')
        return posteruid_span.find('span', class_='hand').get_text() if posteruid_span else None

    def _get_anon_country(self, container):
        flag_span = container.find('span', class_='flag')
        return flag_span['title'] if flag_span else None

    def _get_file(self, container):
        file_container = container.find('div', class_='fileText')

        if file_container == None:
            return None

        return self.file_transformer.transform_file(file_container)

    def transform_thread(self, thread: Thread, thread_html):
        soup = BeautifulSoup(thread_html, 'lxml')

        post_containers = soup.find_all('div', class_='postContainer')

        for container in post_containers:
            post = container.find('div', class_='post')
            post_info = post.find('div', class_='postInfo')
            name_block = post_info.find('span', class_='nameBlock')

            post_id = self._get_post_id(post_info)
            creation_time = int(self._get_creation_time(post_info))
            anon_name = self._get_anon_name(name_block)
            anon_id = self._get_anon_id(name_block)
            anon_country = self._get_anon_country(name_block)
            attached_file = self._get_file(post)
            content = self._get_content(post)
            posts_mentioned = self._get_posts_mentioned(post)

            thread.posts.append(Post(post_id=post_id,
                                      creation_time=creation_time,
                                      content=content,
                                      posts_metioned=posts_mentioned,
                                      file=attached_file,
                                      anon_name=anon_name,
                                      anon_id=anon_id,
                                      anon_country=anon_country))

        return thread

    def transform_thread_sequentially(self, catalogue: list, thread_htmls: list):
        thread_amount = len(catalogue)
        for i in range(0, thread_amount):
            thread = catalogue[i]
            thread_html = thread_htmls[i]
            self.transform_thread(thread, thread_html)