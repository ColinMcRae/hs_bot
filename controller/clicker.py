import pyautogui
import time

def leftclick(coords):
    pyautogui.click(coords)

def rightclick(coords):
    pyautogui.rightClick(coords)

def send(coords):
    pyautogui.rightClick(coords)
    time.sleep(0.2)
    pyautogui.typewrite('f2')

def scroll(position):
    pyautogui.moveTo(position)
    pyautogui.scroll(-5, x=position[0], y=position[1])
    pyautogui.scroll(-5, x=position[0], y=position[1])
    pyautogui.scroll(-5, x=position[0], y=position[1])
    # pyautogui.scroll(-5)
