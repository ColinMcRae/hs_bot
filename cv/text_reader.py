import pytesseract
import os

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
        self.config = ('-l eng --oem 3 --psm 1 --tessdata-dir "models/"')

    def get_text_boxes(self, image, INVERT=True):
        # invert colors of game screen for better text recognition
        self.image = image
        if INVERT:
            image = ~image
        d = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        n_boxes = len(d['text'])
        for i in range(n_boxes):
            if int(d['conf'][i]) > 60:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                # ((startx, starty, endx, endy), name)
                self.textboxes.append(((x, y, x + w, y + h), d['text'][i]))

    def read_text(self, image):
        # TODO - read with image_to_data
        config = ('-l eng --oem 3 --psm 1 --tessdata-dir "models/"')
        text = pytesseract.image_to_string(image, config=config)
        return text

    # debug method
    def draw_result(self):
        font = cv2.FONT_HERSHEY_PLAIN
        output = copy.copy(self.image)
        for box in self.textboxes:
            x1, y1, x2, y2 = box[0]
            cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(output, box[1], (x1, y1 - 10), font, 1, (0, 255, 255), 2)

        pyplot.figure(figsize=(24, 24))
        pyplot.imshow(output)
        pyplot.show()
