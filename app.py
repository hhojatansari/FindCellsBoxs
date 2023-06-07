from samples_info import SamplesInfo
from samples_data import SamplesData
from find_cells_box import FindCellsBox


data_path = '/Users/hosein/Projects/Cells/samples/'

samples_info = SamplesInfo(data_path)
samples_data = SamplesData(samples_info[0:])
cells_detector = FindCellsBox()

cells_detector.detect(samples_data[0:], improve_method='mean')
