from libs.yolov3.yolov3 import Create_Yolov3
from libs.yolov3.utils import *
from cv.config import *
from screeninfo import get_monitors
import pyautogui
import math

#4 debug
import matplotlib.pyplot as plt
from libs.yolov3.utils import *

class ScreenScanner:
    def __init__(self):
        self.screen_W = get_monitors()[0].width
        self.screen_H = get_monitors()[0].height
        self.classes_names = []
        self.yolo = Create_Yolov3(input_size=SIZE, CLASSES=CLASSES)  # from config
        self.yolo.load_weights(WEIGHTS)

    def get_screen_boxes(self):
        screen = self.grab_screen()
        boxes = self.__scan_image(self.yolo, screen, SIZE, iou_threshold=IOU_THREASHOLD, score_threshold=SCORE_THRESHOLD)

        image = draw_bbox(screen, boxes, CLASSES=CLASSES)
        plt.figure(figsize=(30, 30))
        plt.imshow(image)
        plt.show()

        return boxes

    @staticmethod
    def grab_screen():
        screen = pyautogui.screenshot()
        screen = np.array(screen)
        return screen

    def __scan_image(self, yolo, input_image, SIZE, iou_threshold=0.3, score_threshold=0.25):
        sectors = self.__crop_image(input_image)
        all_boxes = []
        #sector = sectors[7]
        for sector in sectors:
            sector_image = sector['img']

            # sector_image = cv2.cvtColor(sector_image, cv2.COLOR_BGR2GRAY)
            sector_image = cv2.cvtColor(sector_image, cv2.COLOR_BGR2RGB)
            sector_image  = cv2.cvtColor(sector_image, cv2.COLOR_BGR2RGB)

            image_data = image_preprocess(np.copy(sector_image), [SIZE, SIZE])
            image_data = tf.expand_dims(image_data, 0)

            pred_bbox = yolo.predict(image_data)
            pred_bbox = [tf.reshape(x, (-1, tf.shape(x)[-1])) for x in pred_bbox]
            pred_bbox = tf.concat(pred_bbox, axis=0)

            #TODO perform nms on all image
            bboxes = postprocess_boxes(pred_bbox, sector_image, SIZE, score_threshold)
            bboxes = nms(bboxes, iou_threshold, method='nms')

            [x_shift, y_shift] = sector['shifts']
            for i, box in enumerate(bboxes):
                bboxes[i][0] += x_shift
                bboxes[i][1] += y_shift
                bboxes[i][2] += x_shift
                bboxes[i][3] += y_shift
            all_boxes += bboxes

        return all_boxes

    def __crop_image(self, img, size=416):
        (H, W) = img.shape[:2]
        h_segments = math.ceil(H / size)
        w_segments = math.ceil(W / size)

        segments = []
        shifts = []
        w_shift = 0
        h_shift = 0
        for h_seg in range(h_segments):
            if (h_shift + size) > H:
                h_shift = H - size
            for w_seg in range(w_segments):
                if (w_shift + size) > W:
                    w_shift = W - size
                segments.append({'img': img[h_shift:h_shift + size, w_shift:w_shift + size], #[y:y+h, x:x+w]
                                 'shifts': [w_shift, h_shift]}) #shifts - [x, y]
                w_shift += size - 40
            h_shift += size - 40
            w_shift = 0
        return segments
