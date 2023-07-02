import os
import time
import uuid
import traceback

import cv2
import imutils
from tqdm import tqdm

from utils import distanceCalculate


class FindCellsBox:
    def __init__(self, results_path='results'):
        self._results_path = results_path
        os.makedirs(self._results_path, exist_ok=True)

        self._image = None
        self._label = None
        self._root_folder = None
        self._base_folder = None
        self._base_image_file_name = None

        self._patch_margin = None
        self._image_patches = {}

        self._canny_low = 101
        self._canny_high = 35

        self._improve_method = None
        self._results_output = None
    
    def _reset_vars(self):
        self._image = None
        self._label = None
        self._root_folder = None
        self._base_folder = None
        self._base_image_file_name = None
        self._patch_margin = None
        self._image_patches = {}

    def detect(self, samples_data, improve_method=None, results_output=None):
        try:
            self._improve_method = improve_method
            self._results_output = results_output
            for sample in tqdm(samples_data):
                time.sleep(1)
                self._reset_vars()
                image = sample['Image']
                self._image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
                self._label = sample['Label']
                self._root_folder = sample['RootFolder']
                self._base_folder = sample['BaseFolder']
                self._base_image_file_name = sample['BaseImageFileName']

                self._approximate_cells()
                self._result_image()
        except:
            traceback.print_exc()

    def _approximate_cells(self):
        self._crop_cells_image()
        self._approximate_boxes()

    def _crop_cells_image(self):
        for point in self._label:
            x = int(self._label[point]['x'])
            y = int(self._label[point]['y'])

            self._patch_margin = int(self._image.shape[1] / 20)
            start_point = x - self._patch_margin, y - self._patch_margin
            end_point = x + self._patch_margin, y + self._patch_margin
            
            self._image_patches[point] = {
                'Image': self._image[start_point[1]:end_point[1], start_point[0]:end_point[0]],
                'x': x,
                'y': y,
            }

    def _approximate_boxes(self):
        for patch_index in self._image_patches:
            continue_flag = False

            image = self._image_patches[patch_index]['Image']

            gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)

            cv2.equalizeHist(gray, gray)
            ret, gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
            
            # close_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
            # gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, close_kernel, iterations=1)

            erode_kernel = cv2.getStructuringElement(cv2.MORPH_ERODE, (5, 5))
            gray = cv2.morphologyEx(gray, cv2.MORPH_ERODE, erode_kernel, iterations=1)

            edges = cv2.Canny(gray, self._canny_low, self._canny_high)


            contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            good_contours = []
            height, width, _ = image.shape
            min_x, min_y = width, height
            max_x = max_y = 0
            for c in contours:
                try:
                    M = cv2.moments(c)
                    cX = int(M["m10"] / (M["m00"] + 0.0001))
                    cY = int(M["m01"] / (M["m00"] + 0.0001))

                    if distanceCalculate((cX, cY), (width/2, height/2)) < 100:
                        good_contours.append(c)

                except:
                    traceback.print_exc()
            if continue_flag:
                continue

            bx = []
            by = []
            for c in good_contours:
                try:
                    # compute the center of the contour
                    # if cv2.contourArea(c) < 1000:
                    #     continue
                    M = cv2.moments(c)
                    cX = int(M["m10"] / (M["m00"]+ 0.0001))
                    cY = int(M["m01"] / (M["m00"]+ 0.0001))
                    
                    if distanceCalculate((cX, cY), (width/2, height/2)) > 100:
                        continue

                    (x, y, w, h) = cv2.boundingRect(c)
                    min_x, max_x = min(x, min_x), max(x+w, max_x)
                    min_y, max_y = min(y, min_y), max(y+h, max_y)  
                    bx.append(min_x)
                    bx.append(max_x)
                    by.append(min_y)   
                    by.append(max_y)
                except:
                    traceback.print_exc()
            try:
                if len(bx) == 0:
                    print(f'Ops! Not detected cell in below image!\n{self._base_folder}-{self._base_image_file_name}\n')
                    continue
                x_padding = ((max(bx) - min(bx)) * 0.15)
                y_padding = ((max(by) - min(by)) * 0.15)
                x1 = int(min(bx) - x_padding)
                y1 = int(min(by) - y_padding)
                x2 = int(max(bx) + x_padding)
                y2 = int(max(by) + y_padding)
                # result_image= cv2.rectangle(image.copy(), (x1, y1), (x2, y2), (255, 0, 0), 2)

                self._image_patches[patch_index]['ApproximateBox'] = {
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2
                }
            except:
                traceback.print_exc()

    def _result_image(self):
        try:
            image = self._image.copy()
            if self._improve_method:
                width, height = self._improve_boxes_wh()
                for patch_index in self._image_patches:
                    x1 = self._image_patches[patch_index]['x'] - int(width/2)
                    y1 = self._image_patches[patch_index]['y'] - int(height/2)
                    x2 = self._image_patches[patch_index]['x'] + int(width/2)
                    y2 = self._image_patches[patch_index]['y'] + int(height/2)
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 15)
                    if self._results_output == 'write_cells':
                        self._save_cell_image(x1, y1, x2, y2)
            else:
                for patch_index in self._image_patches:
                    if 'ApproximateBox' not in self._image_patches[patch_index]:
                        continue
                    x1 = self._image_patches[patch_index]['x'] - self._patch_margin + self._image_patches[patch_index]['ApproximateBox']['x1']
                    y1 = self._image_patches[patch_index]['y'] - self._patch_margin + self._image_patches[patch_index]['ApproximateBox']['y1']
                    x2 = self._image_patches[patch_index]['x'] - self._patch_margin + self._image_patches[patch_index]['ApproximateBox']['x2']
                    y2 = self._image_patches[patch_index]['y'] - self._patch_margin + self._image_patches[patch_index]['ApproximateBox']['y2']
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 15)
                    if self._results_output == 'write_cells':
                        self._save_cell_image(x1, y1, x2, y2)
            if self._results_output == 'write_frames':
                folder = os.path.join(self._results_path, 'frames')
                folder = os.path.join(folder, self._base_folder)
                os.makedirs(folder, exist_ok=True)
                file_name = os.path.join(folder, self._base_image_file_name)
                cv2.imwrite(file_name, image)
            elif self._results_output == 'show':
                cv2.imshow('Result Image', imutils.resize(image, height=1300))
                cv2.moveWindow('Result Image', x=0, y=0)
                cv2.waitKey()
        except:
            traceback.print_exc()

    def _save_cell_image(self, x1, y1, x2, y2):
        folder = os.path.join(self._results_path, 'cells')
        folder = os.path.join(folder, self._base_folder)
        os.makedirs(folder, exist_ok=True)
        file_name = os.path.join(folder, f'{uuid.uuid4()}_{self._base_image_file_name}')
        cv2.imwrite(file_name, self._image[y1:y2, x1:x2])

    def _improve_boxes_wh(self):
        if self._improve_method == 'mean':
            t_width = 0
            t_height = 0
            counter = 0
            for patch_index in self._image_patches:
                if 'ApproximateBox' not in self._image_patches[patch_index]:
                    continue
                counter += 1
                box = self._image_patches[patch_index]['ApproximateBox']
                t_width += abs(box['x2'] - box['x1'])
                t_height += abs(box['y2'] - box['y1'])
            mean_width = int(t_width / counter)
            mean_height = int(t_height / counter)
            return mean_width, mean_height
