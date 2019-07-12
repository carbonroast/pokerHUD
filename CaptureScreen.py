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

def image_compare(img1, img2):
    arr1 = numpy.array(img1)
    arr2 = numpy.array(img2)
    if arr1.shape != arr2.shape:
        return False
    maxdiff = numpy.max(numpy.abs(arr1-arr2))
    return maxdiff == 0


def CreateBox(x,y,x2,y2):
    width = abs(x2-x)
    height = abs(y2-y)
    return {"top": min(y, y2), "left": min(x, x2), "width": width, "height": height}

def main():
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": 800, "height": 640}
        while "Screen capturing":
            img = numpy.array(sct.grab(monitor))
            cv2.imshow("OpenCV/Numpy normal", img)
            print("Screenshot 1 Taken")
            time.sleep(3)
            img2 = numpy.array(sct.grab(monitor))
            print("Screenshot 2 Taken")
            if image_compare(img,img2):
                print("SAME")
            else:
                print("DIFF")
            # Press q to quit
            if cv2.waitKey(25) & 0xff == ord("q"):
                cv2.destroyAllWindows()
                break


def TakeScreenshot(box):
    with mss.mss() as sct:
        while "Screen capturing":

            img = numpy.array(sct.grab(box))
            cv2.imshow("OpenCV/Numpy normal", img)

            # Press q to quit
            if cv2.waitKey(25) & 0xff == ord("q"):
                cv2.destroyAllWindows()
                break


def ReadScreenShot(image):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    print(pytesseract.image_to_string(Image.open(image)))


def DrawBox():
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
            box = CreateBox(x, y, x2, y2)
            print(box)
            TakeScreenshot(box)

        time.sleep(0.01)

if __name__ == "__main__":
    print("Start")
    DrawBox()