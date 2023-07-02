import threading
import numpy as np
from samples_info import SamplesInfo
from samples_data import SamplesData
from find_cells_box import FindCellsBox


def find_cells_box(sample_data):
    print(f'{threading.current_thread().name} thread is started!')
    cells_detector = FindCellsBox(results_path='results_data')
    cells_detector.detect(sample_data, improve_method='mean', results_output='write_cells')


data_path = '/Users/hosein/Projects/Cells/samples/'
thread_number = 2

samples_info = SamplesInfo(data_path)
samples_data = SamplesData(samples_info[0:])

chunked_samples = samples_data.split_data(thread_number)

for index, data in enumerate(chunked_samples):
    threading.Thread(name=str(index), target=find_cells_box, args=(data,)).start()
