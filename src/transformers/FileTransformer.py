import re
from models.models import AttachedFile

class FileTransfomer:

    def __init__(self):
        self.size_and_dims_regex_pattern = re.compile(pattern=r"\((\d+(?:\.\d+)?)\s?([KM]?B)(?:,\s?(\d+)x(\d+))?(?:,\s?(.+))?\)")
        """
            A little explanation of the regex pattern:
            On 4chan, next to the filename on a reply, you can see the size of the file, 
            its width and its height in the following format:
            (X KB, WxH)
            The idea behind the above pattern is to extract those into 4 groups, one
            for the size, one for the units, one for the width and another one for the height.
            The units group is because every size will be stored in KB.
            The whole second part is optional because some (all?) boards allow PDF files to be uploaded, which
            comply with the format (X KB, PDF).
        """

    def _get_filename_and_ext(self, container):
        filename_with_ext = container.get('title',  container.text)

        if filename_with_ext == 'Spoiler Image':
            parent = container.find_parent('div', class_='fileText')
            filename_with_ext = parent.get('title')

        filename, extension = filename_with_ext.rsplit('.', 1)

        return filename, extension

    def _get_file_timestamp(self, container):
        file_timestamp = container['href'].rsplit('/', 1)[1]
        file_timestamp_without_extension = file_timestamp.split('.')[0]

        return int(file_timestamp_without_extension)

    def _get_file_size_and_dimensions(self, container):
        match = self.size_and_dims_regex_pattern.search(container.text)

        size = float(match.group(1))
        units = match.group(2)

        if units == 'MB':
            size = size*1024
        elif units == 'B':
            size = size/1024

        if match.group(5) == 'PDF':
            return size, None, None

        width = int(match.group(3))
        height = int(match.group(4))

        return size, width, height


    def transform_file(self, file_container):
        filename_data = file_container.find('a')
        filename, extension = self._get_filename_and_ext(filename_data)
        file_timestamp = self._get_file_timestamp(filename_data)
        size, width, height = self._get_file_size_and_dimensions(file_container)

        file = AttachedFile(
            filename,
            file_timestamp,
            extension,
            size,
            width,
            height
        )

        return file