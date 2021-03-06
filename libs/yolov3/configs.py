#================================================================
#
#   File name   : configs.py
#   Author      : PyLessons
#   Created date: 2020-06-04
#   Website     : https://pylessons.com/
#   GitHub      : https://github.com/pythonlessons/TensorFlow-2.x-YOLOv3
#   Description : yolov3 configuration file
#
#================================================================

# YOLO options
YOLO_DARKNET_WEIGHTS        = "cfg/yolov3.weights"
YOLO_DARKNET_TINY_WEIGHTS   = "cfg/yolov3-tiny.weights"
YOLO_COCO_CLASSES           = "models/classes_voc.txt"
YOLO_STRIDES                = [8, 16, 32]
YOLO_IOU_LOSS_THRESH        = 0.5
YOLO_ANCHOR_PER_SCALE       = 3
YOLO_MAX_BBOX_PER_SCALE     = 100
YOLO_INPUT_SIZE             = 416
YOLO_ANCHORS                = [[[10,  13], [16,   30], [33,   23]],
                               [[30,  61], [62,   45], [59,  119]],
                               [[116, 90], [156, 198], [373, 326]]]
# Train options
TRAIN_YOLO_TINY             = True
TRAIN_SAVE_BEST_ONLY        = True # saves only best model according validation loss (True recommended)
TRAIN_SAVE_CHECKPOINT       = False # saves all best validated checkpoints in training process (may require a lot disk space) (False recommended)
TRAIN_CLASSES               = 'models/classes_voc.txt'
TRAIN_ANNOT_PATH            = "dataset/train.txt"
TRAIN_LOGDIR                = "log_tb"
TRAIN_CHECKPOINTS_FOLDER    = "checkpoints"
TRAIN_MODEL_NAME            = "yolov3_hs"
TRAIN_LOAD_IMAGES_TO_RAM    = True #False # faster training, but need more RAM
TRAIN_GRAYSCALE             = False #make all images gray
TRAIN_BATCH_SIZE            = 12
TRAIN_INPUT_SIZE            = 416
TRAIN_DATA_AUG              = False
TRAIN_TRANSFER              = False
TRAIN_FROM_CHECKPOINT       = "checkpoints/yolov3_hs_Tiny" # yolov3_hs_Tiny
TRAIN_LR_INIT               = 0.0007 #1e-4
TRAIN_LR_END                = 0.00001 #1e-6
TRAIN_WARMUP_EPOCHS         = 2
TRAIN_EPOCHS                = 20

# TEST options
TEST_ANNOT_PATH             = "dataset_hs/test.txt"
TEST_BATCH_SIZE             = 4
TEST_INPUT_SIZE             = 416
TEST_DATA_AUG               = False
TEST_DECTECTED_IMAGE_PATH   = ""
TEST_SCORE_THRESHOLD        = 0.3
TEST_IOU_THRESHOLD          = 0.45


#YOLOv3-TINY WORKAROUND
if TRAIN_YOLO_TINY:
    YOLO_STRIDES            = [16, 32, 64]    
    YOLO_ANCHORS            = [[[10,  14], [23,   27], [37,   58]],
                               [[81,  82], [135, 169], [344, 319]],
                               [[0,    0], [0,     0], [0,     0]]]
