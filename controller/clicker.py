import pyautogui

def leftclick(coords):
    pyautogui.click(coords)

def rightclick():
    pass

def scroll(position):
    pyautogui.scroll(-5, x=position[0], y=position[1])
    # pyautogui.scroll(-5)
