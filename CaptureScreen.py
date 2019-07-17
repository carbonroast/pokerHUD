import time
import cv2
import mss
import numpy
import mss.tools
from PIL import Image
import pytesseract
from tkinter import *
import pywinauto
import win32api
import win32con
from datetime import datetime
import threading
import os
import keyboard
from Utils import *
from matplotlib import pyplot as plt

string = ""
boundary = None
programState = None
# Compares pixels to see if the image has changed
def image_compare(img1, img2):
    arr1 = numpy.array(img1)
    arr2 = numpy.array(img2)
    if arr1.shape != arr2.shape:
        return False
    maxdiff = numpy.max(numpy.abs(arr1-arr2))
    return maxdiff == 0


def TakeScreenshots(box):
    with mss.mss() as sct:
        while "Screen capturing":

            img = numpy.array(sct.grab(box))
            cv2.imshow("OpenCV/Numpy normal", img)
            time.sleep(0.4)
            img2 = numpy.array(sct.grab(box))
            if image_compare(img, img2):
                print("Same Picture")
            else:
                print("Different Picture")
                name = str(datetime.now()).replace(".","").replace(":","-") + ".png"
                cv2.imwrite(name, img2)
                ReadScreenShot(name)
                os.remove(name)
            # Press q to quit
            if cv2.waitKey(25) & 0xff == ord("q"):
                cv2.destroyAllWindows()
                break

def TakeAndRead(box):
    with mss.mss() as sct:
        while "Screen capturing":
            img = numpy.array(sct.grab(box))
            #cv2.imshow("OpenCV/Numpy normal", img)
            name = str(datetime.now()).replace(".","").replace(":","-") + ".png"
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            (thresh, bwimage) = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
            cv2.imshow("OpenCV/Numpy normal", bwimage)
            cv2.imwrite(name, bwimage)
            ReadScreenShot(name)
            os.remove(name)
            # Press q to quit
            if cv2.waitKey(25) & 0xff == ord("q"):
                cv2.destroyAllWindows()
                break


def ReadScreenShot(image):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    global string
    string = pytesseract.image_to_string(image)
    print(string)


# Creates the boundaries for the bounding box
def DrawBox():
    global programState
    global boundary
    while True:
        click = False
        key_code = win32con.VK_LBUTTON
        state = win32api.GetAsyncKeyState(key_code)

        x, y = win32api.GetCursorPos()
        if state != 0 and state != 1:
            print("CLICK")
            while state != 0 and state != 1:
                state = win32api.GetAsyncKeyState(key_code)
            click = True
            print("END CLICK")
        x2, y2 = win32api.GetCursorPos()
        if click:
            print(x, y)
            print(x2, y2)
            width = abs(x2 - x)
            height = abs(y2 - y)
            programState = ProgramState.Screenshotting
            return {"top": min(y, y2), "left": min(x, x2), "width": width, "height": height}

        time.sleep(0.01)


if __name__ == "__main__":
    print("Start")

    programState = ProgramState.Boundaries
    while True:
        if programState == ProgramState.Boundaries:
            boundary = DrawBox()
        if programState == ProgramState.Screenshotting:
            if keyboard.is_pressed('f'):
                TakeScreenshots(boundary)
            if keyboard.is_pressed('t'):
                TakeAndRead(boundary)

    """
    img_rgb = cv2.imread('playersattable.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('pokergray.jpg', img_gray)

    template = cv2.imread('playerseated.png')
    template_iogray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    h, w = template.shape[:-1]

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.40

    loc = numpy.where(res >= threshold)
    print(loc)
    for pt in zip(*loc[::-1]):
        #print(pt, (pt[0] + w, pt[1] + h))
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    cv2.imwrite('pokerres.png', img_rgb)
    """