import pytesseract
import os
import numpy as np

#debug zone
import cv2
from matplotlib import pyplot
import copy

class TextReader():
    def __init__(self):
        t_path = os.path.join('C:/', 'Program Files', 'Tesseract-OCR', 'tesseract.exe')
        pytesseract.pytesseract.tesseract_cmd = t_path
        self.image = ''
        self.textboxes = []
        # self.config = ('-l eng --oem 3 --psm 1 --tessdata-dir "models/"')
        self.config = ('-l eng --oem 3 --psm 11 --tessdata-dir "models/"')

    def get_text_boxes(self, image, INVERT=True):
        self.textboxes = []
        self.image = image

        # resize image for better text recognition
        scale = 2
        shape = np.shape(image)
        resized_image = cv2.resize(image, (shape[1] * 2, shape[0] * 2))

        # thresholding image
        image = ~resized_image
        _, image = cv2.threshold(image, 127, 255, cv2.THRESH_TOZERO)

        d = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        n_boxes = len(d['text'])
        for i in range(n_boxes):
            if int(d['conf'][i]) > 60:
                coords = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                # scale coordinates to original size
                (x, y, w, h) = [int(a / scale) for a in coords]
                self.textboxes.append(((x, y, x + w, y + h), d['text'][i]))

        return self.textboxes

    def read_text(self, image):
        # TODO - read with image_to_data
        config = ('-l eng --oem 3 --psm 1 --tessdata-dir "models/"')
        text = pytesseract.image_to_string(image, config=config)
        return text

    # debug method
    def draw_result(self, title=''):
        text_color = (255, 234, 54)
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        output = copy.copy(self.image)
        for box in self.textboxes:
            x1, y1, x2, y2 = box[0]
            cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(output, box[1], (x1, y1 - 10), font, 0.75, text_color, 1, lineType=cv2.LINE_AA)

        pyplot.figure(figsize=(24, 24))
        pyplot.imshow(output, 'gray')
        pyplot.title(title)
        pyplot.show()
