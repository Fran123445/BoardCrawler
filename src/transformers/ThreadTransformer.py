import re

from bs4 import BeautifulSoup
from models.models import Post, Thread, AttachedFile

class ThreadTransformer:

    def _get_file(self, post):
        file = None

        if post.get("filename", None):
            file = AttachedFile(
                post["filename"],
                post["tim"],
                post["ext"],
                post["fsize"],
                post["w"],
                post["h"]
            )

        return file

    def _get_post_content(self, post):
        raw_post_body = post.get("com", "")

        post_html = raw_post_body.replace("<wbr>", "").replace("<br>", "\n")
        soup = BeautifulSoup(post_html, 'html.parser')

        return soup.getText()

    def _get_posts_mentioned(self, post_content):
        posts_mentioned = re.findall(r">>\s*(\d+)", post_content)

        return posts_mentioned

    def transform_thread(self, thread: Thread, thread_json):
        post_list = thread_json["posts"]

        for post in post_list:
            post_id = post["no"]
            creation_time = int(post["time"])
            anon_name = post.get("name", None)
            anon_id = post.get("id", None)
            anon_country = post.get("country_name", None)
            attached_file = self._get_file(post)
            content = self._get_post_content(post)
            posts_mentioned = self._get_posts_mentioned(content)

            thread.posts.append(Post(post_id=post_id,
                                      creation_time=creation_time,
                                      content=content,
                                      posts_metioned=posts_mentioned,
                                      file=attached_file,
                                      anon_name=anon_name,
                                      anon_id=anon_id,
                                      anon_country=anon_country))

        return thread

    def transform_threads_sequentially(self, catalogue: list, thread_jsons: list):
        thread_amount = len(catalogue)
        for i in range(0, thread_amount):
            thread = catalogue[i]
            thread_json = thread_jsons[i]
            self.transform_thread(thread, thread_json)