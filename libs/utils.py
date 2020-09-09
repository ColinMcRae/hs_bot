import numpy as np
import win32api

def distance(a, b):
    distance = 0
    for i in range(0, len(a)):
        distance += np.linalg.norm(a[i] - b[i])
    return distance

def get_coords(box):
    return [int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)]

def getIdleTime():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0
