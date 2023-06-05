import cv2


class SamplesData:
    def __init__(self, samples_info):
        if not isinstance(samples_info, list):
            print('Data must be list of dict!')
            return
        self._samples_data = samples_info
        self._load_data()

    def _load_data(self):
        for index, sample in enumerate(self._samples_data):
            self._samples_data[index]['Image'] = cv2.imread(sample['ImageFile'])
            self._samples_data[index]['Label'] = self._read_label(sample['LabelFile'])

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