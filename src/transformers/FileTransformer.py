import re
from models.models import AttachedFile

class FileTransfomer:

    def __init__(self):
        self.size_and_dims_regex_pattern = r"\((\d+(?:\.\d+)?)\s?([KM]?B),\s?(\d+)x(\d+)\)"
        """
            A little explanation of the regex pattern:
            On 4chan, next to the filename on a reply, you can see the size of the file, 
            its width and its height in the following format:
            (X KB, WxH)
            The idea behind the above pattern is to extract those into 4 groups, one
            for the size, one for the units, one for the width and another one for the height.
            The units group is because every size will be stored in KB.
        """

    def _get_filename_and_ext(self, container):
        filename_with_ext = container['title'] if container.get('title') else container.text
        split = filename_with_ext.split('.')
        filename = split[0]
        extension = split[1]

        return filename, extension

    def _get_file_timestamp(self, container):
        file_timestamp = container['href'].split('/')[-1]
        file_timestamp_without_extension = file_timestamp.split('.')[0]

        return int(file_timestamp_without_extension)

    def _get_file_size_and_dimensions(self, container):
        match = re.search(self.size_and_dims_regex_pattern, container.text)
        size = float(match.group(1))
        units = match.group(2)
        width = int(match.group(3))
        height = int(match.group(4))

        if units == 'MB':
            size = size*1024
        elif units == 'B':
            size = size/1024

        return size, width, height


    def transform_file(self, file_container):
        filename_data = file_container.find('a')
        filename, extension = self._get_filename_and_ext(filename_data)
        fileTimestamp = self._get_file_timestamp(filename_data)
        size, width, height = self._get_file_size_and_dimensions(file_container)

        file = AttachedFile(
            filename,
            fileTimestamp,
            extension,
            size,
            width,
            height
        )

        return file