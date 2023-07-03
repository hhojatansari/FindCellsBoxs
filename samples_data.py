import os

import cv2
import numpy as np
from tqdm import tqdm


class SamplesData:
    def __init__(self, samples_info):
        if not isinstance(samples_info, list):
            print('Data must be list of dict!')
            return
        self._samples_data = samples_info
        self._load_data()

    def _load_data(self):
        for index, sample in tqdm(enumerate(self._samples_data)):
            image_file_name = os.path.join(
                os.path.join(os.path.join(sample['RootFolder'], 'images'), sample['BaseFolder']),
                sample['BaseImageFileName']
            )
            label_file_name = os.path.join(
                os.path.join(os.path.join(sample['RootFolder'], 'labels'), sample['BaseFolder']),
                sample['BaseLabelFileName']
            )
            self._samples_data[index]['Image'] = cv2.imread(image_file_name)
            self._samples_data[index]['Label'] = self._read_label(label_file_name)

    @staticmethod
    def _read_label(label_file):
        label_dict = {}
        with open(label_file, 'r') as file:
            for index, point in enumerate(file.readlines()):
                point = [eval(p) for p in point.strip().split(',')]
                x = round(point[0])
                y = round(point[1])
                label_dict[index] = {'x': x, 'y': y}
        return label_dict

    def __len__(self):
        return len(self._samples_data)

    def __getitem__(self, value):
        try:
            if isinstance(value, slice):
                start = 0 if value.start is None else value.start
                stop = len(self._samples_data) if value.stop is None else value.stop
                return self._samples_data[start:stop]
            elif isinstance(value, int):
                return self._samples_data[value]
            else:
                return self._samples_data
        except:
            return None

    def split_data(self, split_number):
        return np.array_split(self._samples_data, split_number)
