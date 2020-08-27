from cv import ScreenScanner, TextReader
from cv.config import CLASSES
from controller import clicker
import time
import libs.utils as utils
import numpy as np
import re

from game.config import TRADE_STATIONS, PLANETS

import cv2
import copy
from matplotlib import pyplot as plt
import _pickle as pickle

class CVGameInterface:
    def __init__(self):
        self.screenscanner = ScreenScanner()
        self.textreader = TextReader()
        #buttons coords
        self.loadplanet = [1081, 1113] #hardcoded yet
        self.unloadall = []
        self.loadall = [329, 711]
        #text coords
        self.planet_name_box = (1010, 759, 1032, 890) #HARDCODE/static val
        self.cargolist_box = []
        self.transport_capacity_box = [] # coords of (0/24) caption
        self.planet_capacity_box = []
        self.planet_cargo_box = []
        self.transport_buttons = [] #we eill search it at every game start

        self.classes = []
        with open(CLASSES, 'r') as data:
            for ID, name in enumerate(data):
                self.classes.append(name.strip('\n'))

    def select_planet(self):
        pass

    def init_objects(self):
        with open('objects.pkl', 'rb') as file:
            objects = pickle.load(file)

        return objects

        objects = self.__get_objects()

        if not objects['tradestation']:
            print('no objects found')
            return

        if objects['planet'] and not self.planet_name_box:
            self.__find_planet_namebox(objects['planets'])

        if not self.transport_buttons:
            self.__find_transport_buttons(objects)

        # with open('objects.pkl', 'wb') as file:
        #     pickle.dump(objects, file)

        return objects

    def get_planets(self, coords):
        with open('planets.pkl', 'rb') as file:
            planets = pickle.load(file)
        return planets

        #click every planet, and find it's name
        print('getting planets')
        planets = []
        for planet in coords:
            clicker.leftclick(planet)
            time.sleep(0.2)
            screen = self.screenscanner.grab_screen()
            name = self.__get_planet_name(screen)
            planets.append({'name': name, 'coords': planet})

        #############
        with open('planets.pkl', 'wb') as file:
            pickle.dump(planets, file)
        #############

        return planets

    def planet_cargos(self):
        if not self.cargolist_box:
            self.__find_cargolist_box()
        print(self.cargolist_box)

        screen = ScreenScanner.grab_screen()
        startX, startY, endX, endY = self.cargolist_box

        cargobox = copy.copy(screen[startX:endX, startY:endY])
        textboxes = self.textreader.get_text_boxes(cargobox)
        self.textreader.draw_result()
        cargoboxes = []

        output = copy.copy(screen)

        for coords, text in textboxes:
            if text in PLANETS or text in TRADE_STATIONS:
                x1, y1, x2, y2 = coords
                x1 += startY
                x2 += startY
                y1 += startX
                y2 += startX
                cargoboxes.append((text, (x1, y1, x2, y2)))
                cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(output, text, (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)

        # DEBUG SHOW
        # plt.figure(figsize=(24, 24))
        # plt.imshow(output)
        # plt.show()

        return cargoboxes

    def is_transport_docked(self, transport):
        clicker.leftclick(transport.button)
        time.sleep(0.2)
        objects = self.__get_objects()

        return len(objects['loadplanet']) > 0

    def transport_load(self):
        if not self.transport_capacity_box:
            self.__find_capacity_box()

        screen = ScreenScanner.grab_screen()

        startX, startY, endX, endY = self.transport_capacity_box
        loadbox = screen[startY:endY, startX:endX]

        load = self.textreader.read_text(loadbox)
        load = ''.join(re.findall('\d', load.split('/')[0]))
        return int(load)

    # TODO
    def send_transport(self, transport, dest):
        clicker.leftclick(transport.button)
        clicker.rightclick(dest.coords)

    def __get_planet_name(self, screen):
        if not self.planet_name_box:
            print('namebox not avaliable')
            return ''

        startX, startY, endX, endY = self.planet_name_box
        namebox = screen[startX:endX, startY:endY]
        text = self.textreader.read_text(namebox).split(' ')[0]
        if text in PLANETS:
            print(text)
            return text

        # move frame, because tesseract can't read text in some text positions
        # UPD - maybe, this code will be removed
        for shift in range(-5, 10):
            startX, startY, endX, endY = self.planet_name_box
            startY -= shift
            endY -= shift
            namebox = screen[startX:endX, startY:endY]
            text = self.textreader.read_text(namebox).split(' ')[0]

            if text in PLANETS:
                return text
                break

        #############
        #############
        plt.imshow(namebox)
        plt.show()

        ###############
        #########
        print('!!!!!!failed to read name!!!!!')
        print(text)  ##########################

    def __get_objects(self):
        boxxes = self.screenscanner.get_screen_boxes()
        result = {}

        for box in boxxes:
            for class_name in self.classes:
                if class_name not in result.keys():
                    result[class_name] = []
                idx = self.classes.index(class_name)
                if int(box[5]) == idx:
                    result[class_name].append(utils.get_coords(box))

        print(result)
        return result

    def __find_planet_namebox(self, objects):
        # click all planets
        planet_name_boxes = []

        # take 3 planets to find names
        for planet in objects[:3]:
            clicker.leftclick(planet)
            time.sleep(0.2)
            screen = self.screenscanner.grab_screen()

            textboxes = self.textreader.get_text_boxes(screen)
            xmin, ymin = 0, 0
            planet_name_boxes = []

            # print(textboxes)
            for box in textboxes:
                if box[1] in PLANETS:
                    name = box[1]
                    planet_name_boxes.append((box[0]))
                    self.textreader.textboxes = []
                    print('name found', box[1])
                    break

        startX, startY, endX, endY = 2000, 2000, 0, 0
        for row in planet_name_boxes:
            y1, x1, y2, x2 = row  # (14, 11, 42, 27)
            x1 = x1
            x2 = x2
            y1 = y1
            y2 = y2

            if startX > x1:
                startX = x1
            if startY > y1:
                startY = y1
            if endX < x2:
                endX = x2
            if endY < y2:
                endY = y2

        # extend frame a bit
        self.planet_name_box = (startX - 5, startY - 5, endX + 5, endY + 50)

    def __find_transport_buttons(self, objects):
        if not objects['transportcontrol']:
            print('no transport buttons found')
            return

        all_buttons = sorted(objects['transportcontrol'], key=lambda x: x[1])

        # Here we calculate average distance between buttons in group based on 3 first buttons
        a = all_buttons[:3]
        avg_distance = 0
        for i in range(0, len(a) - 1):
            avg_distance += utils.distance(a[i + 1], a[i])

        avg_distance = int(avg_distance / 2)

        # Add other buttons in group
        # Buttons are sorted from top to bottom, so, top buttons are in our group
        group_btns = [all_buttons[0]]
        for i in range(1, len(all_buttons)):
            btn = all_buttons[i]
            dist = utils.distance(btn, all_buttons[0])
            if (avg_distance * i * 1.1) > dist > (avg_distance * i * 0.9):
                group_btns.append(btn)

        self.transport_buttons = group_btns

    def __find_capacity_box(self):
        screen = self.screenscanner.grab_screen()
        textboxes = self.textreader.get_text_boxes(screen)

        for coords, text in textboxes:
            if re.match("\(\d+/\d+\)", text):
                startX, startY, endX, endY = coords
                self.transport_capacity_box = (startX - 5, startY - 5, endX + 5, endY + 5)
            if re.match("\d+/\d+", text):
                startX, startY, endX, endY = coords
                self.planet_capacity_box = (startX - 5, startY - 5, endX + 5, endY + 5)

    def __find_cargolist_box(self):
        objects = self.__get_objects()
        # set bottom box border on load button
        X1, Y1, X2, Y2 = 1200, 1900, 0, 0
        if objects['loadall'] or objects['unloadall']:
            Y2, X2 = objects['loadall'][0] or objects['unloadall'][0]
        Y2 += 100

        #TODO - fix double snapshot
        screen = ScreenScanner.grab_screen()
        textboxes = self.textreader.get_text_boxes(screen)

        # hint - 6 scrolls to the same position

        pl_boxes = []
        for coords, text in textboxes:
            if text in PLANETS or text in TRADE_STATIONS: pl_boxes.append(coords)

        # find top side and left side from menu heading
        for y1, x1, y2, x2 in pl_boxes:
            if x2 < X1: X1 = x2
            if y1 < Y1: Y1 = y1
        Y1 -= 50  # shift left a bit

        ##DEBUG###

        # plt.imshow(screen[X1:X2, Y1:Y2])
        # plt.show()

        self.cargolist_box = [X1, Y1, X2, Y2]
