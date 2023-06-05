from samples_info import SamplesInfo
from samples_data import SamplesData
from find_cells_box import FindCellsBox


data_path = '/home/hosein/Work/Hara/Projects/Cells/samples/'

samples_info = SamplesInfo(data_path)
samples_data = SamplesData(samples_info[0:1])
cells_detector = FindCellsBox()


cells_detector.process(samples_data[0:])
