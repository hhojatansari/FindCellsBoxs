import threading
import numpy as np
from samples_info import SamplesInfo
from samples_data import SamplesData
from find_cells_box import FindCellsBox


def find_cells_box(batch):
    print(f'{threading.current_thread().name} thread is started! len:', len(batch))
    batch_data = SamplesData(batch.tolist())
    cells_detector = FindCellsBox(results_path='results_data')
    cells_detector.detect(batch_data[0:], improve_method='mean', results_output='write_frames')
    print(f'{threading.current_thread().name} thread is finished!')


data_path = '/mnt/data1/mousavi/BM_labeled/'
thread_number = 50

samples_info = SamplesInfo(data_path)
print("Length of samples:", len(samples_info))

chunked_samples = samples_info.split_data(thread_number)
print(len(chunked_samples), chunked_samples[0], chunked_samples[1])

for index, data in enumerate(chunked_samples):
	print(len(data))
	threading.Thread(name=str(index), target=find_cells_box, args=(data,)).start()

