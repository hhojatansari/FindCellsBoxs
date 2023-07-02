import os
import traceback


class SamplesInfo:
    def __init__(self, data_path):
        self._data_path = data_path
        self._data = []

        self._folder_path = None
        self._folder_files = None
        self._image_file = None
        self._label_file = None
        self._filename = None

        self._load()

    def _load(self):
        folders = self._just_folders(self._data_path)
        folder_dict = {}

        for folder in folders:
            image_files_list = self._just_files(folder, extension_list=['jpg'])
            base_folder = os.path.basename(folder)
            folder_dict[base_folder] = {}

            for file in image_files_list:
                base_file_name = os.path.basename(file).split('.')[0]
                if self._check_files_exists(folder, base_file_name):
                    self._data.append(
                        {
                            'RootFolder': self._data_path,
                            'BaseFolder': base_folder,
                            'BaseImageFileName': base_file_name + '.jpg',
                            'BaseLabelFileName': base_file_name + '.txt'
                         }
                    )
                else:
                    print(f'Warning: file not exists!\nFile: {file}\n')
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

    @staticmethod
    def _check_files_exists(path, base_file_name):
        if os.path.isfile(os.path.join(path, base_file_name + '.jpg')) and \
                os.path.isfile(os.path.join(path, base_file_name + '.txt')):
            return True
        else:
            return False

    @staticmethod
    def _just_folders(path):
        folders = []
        for folder in os.listdir(path):
            if os.path.isdir(os.path.join(path, folder)):
                folders.append(os.path.join(path, folder))
        return folders

    @staticmethod
    def _just_files(path, extension_list):
        files = []
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                for ext in extension_list:
                    if ext in file:
                        files.append(os.path.join(path, file))
        return files
