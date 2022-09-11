import os

from PIL import Image, UnidentifiedImageError

from config import config


def readfile(path):
    path = os.path.abspath(path)
    try:
        img = Image.open(path)
        return img
    except UnidentifiedImageError as error:
        print("Image not found! at path "+path)
        quit()
    except FileNotFoundError as er:
        print("Image not found! at path "+path)
        quit()


def write_to_file(path, msg):
    try:
        path = os.path.abspath(path)
        file = open(path, 'w')
        file.write(msg)
        return True
    except FileNotFoundError:
        print("Path not found error")
        return False


def readtext(path):
    try:
        path = os.path.abspath(path)
        file = open(path, 'r')
        content = file.read()
        return content
    except FileNotFoundError as error:
        print("Input text file not found!")
        quit()


def saveimage(img):
    if config.outputpath.endswith('/'):
        p = config.outputpath+"stegoimage.png"
    else:
        p = config.outputpath+".png"
    img.save(p)
    print("\nStego Image saved at "+p)
