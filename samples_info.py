import os
import traceback


class SamplesInfo:
    def __init__(self, data_path):
        self._data_path = data_path
        self._data = []

        self._counter = 0
        self._folder_path = None
        self._folder_files = None
        self._image_file = None
        self._label_file = None
        self._filename = None

        self._load()

    def _load(self):
        for folder in os.listdir(self._data_path):
            self._folder_path = os.path.join(self._data_path, folder)
            self._folder_files = os.listdir(self._folder_path)

            # if not self.is_valid_files():
            #     continue
            if not self.files_exist():
                continue
            self._data.append(
                {
                    'Name': self._filename,
                    'FolderPath': self._folder_path,
                    'ImageFile': self._image_file,
                    'LabelFile': self._label_file
                }
            )
            self._counter += 1
        return self

    def __getitem__(self, value):
        try:
            if isinstance(value, slice):
                start = 0 if value.start is None else value.start
                stop = len(self._data) if value.stop is None else value.stop
                return self._data[start:stop]
            elif isinstance(value, int):
                return self._data[value]
            else:
                return self._data
        except:
            return None

    def is_valid_files(self):
        try:
            # if len(self._folder_files) != 2:
            #     print('Files number problem!', self._folder_path, self._folder_files)
            #     return False

            files_name = [file.split('.')[0] for file in self._folder_files]
            if files_name[0] != files_name[1]:
                print('Files name problem!', self._folder_path, self._folder_files)
                return False

            return True
        except:
            traceback.print_exc()

    def files_exist(self):
        self._filename = self._folder_files[0].split('.')[0]
        self._image_file = os.path.join(self._folder_path, self._filename) + '.jpg'
        self._label_file = os.path.join(self._folder_path, self._filename) + '.txt'

        if os.path.isfile(self._image_file) and os.path.isfile(self._label_file):
            return True
        else:
            print('Files exists problem!', self._folder_path, self._filename)
            return False

    def __len__(self):
        return len(self._data)
