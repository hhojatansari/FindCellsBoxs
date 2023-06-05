import cv2
import imutils


class FindCellsBox:
    def __init__(self):
        pass

    @staticmethod
    def process(samples_data):
        for sample in samples_data:
            image = sample['Image']
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

            label = sample['Label']
            point_image = image.copy()
            for point in label:
                x = int(label[point]['x'])
                y = int(label[point]['y'])
                cv2.circle(point_image, (x, y), 20, (0, 255, 0), -1)

                margin = int(image.shape[1] / 20)
                start_point = x - margin, y - margin
                end_point = x + margin, y + margin
                cv2.rectangle(point_image, start_point, end_point, (0, 0, 0), 5)
                cell_image = image[start_point[1]:end_point[1], start_point[0]:end_point[0]]

                cv2.imshow(str(point), imutils.resize(cell_image, height=100))

            # cv2.imwrite(sample['FolderPath']+'/draw_'+sample['Name']+'.jpg', image)
            cv2.imshow('Org image', imutils.resize(point_image, height=1000))

            cv2.waitKey()

    