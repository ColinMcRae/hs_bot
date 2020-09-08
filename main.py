import cv
from game.objects import SolarSystem
from game.cargo_delivery import CargoDelivery

#debug
import libs.utils as utils
from game.config import TRADE_STATIONS, PLANETS
#debug

import time

import pyautogui
import numpy as np
from matplotlib import pyplot as plt


def sort():
    interface = cv.CVGameInterface()

    sol = SolarSystem(interface)
    # sol.debug()
    delivery = CargoDelivery(sol)
    delivery.sort_cargo()



if __name__ == '__main__':
    sort()
