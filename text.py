from config import config
from file_ops import saveimage
from math_ops import getbinarys, getstr, insertbit


def embedd(img, text):
    maxr, maxc = img.size
    bins = getbinarys(text)
    px = img.load()
    addsize(px, len(bins))
    r, c = 0, config.NO_OF_SIZE_PIXELS
    colorind = 0
    print("\nEmbedding the text in the image...")
    for i in bins:
        for k in i:
            if colorind == 3:
                colorind = 0
                c += 1
                if c == maxc:
                    c = 0
                    r += 1
                    if r == maxr:
                        print("Text size is greater than image size!")
            cur = list(px[r, c])
            cur[colorind] = insertbit(cur[colorind], k)
            px[r, c] = tuple(cur)
            colorind += 1
    # p = ""
    saveimage(img)


def addsize(px, s):
    s = bin(s)[2:]
    s = (config.NO_OF_SIZE_BITS-len(s))*"0"+s
    k = 0
    for i in range(config.NO_OF_SIZE_PIXELS):
        p = list(px[0, i])
        for j in range(3):
            p[j] = insertbit(p[j], s[k])
            k += 1
        px[0, i] = tuple(p)


def extractsize(px):
    b = ""
    for i in range(config.NO_OF_SIZE_PIXELS):
        p = px[0, i]
        for j in range(3):
            b += bin(p[j])[-1]

    return int(b, 2)


def extract_message(img):
    px = img.load()
    maxr, maxc = img.size
    s = extractsize(px)
    r, c = 0, config.NO_OF_SIZE_PIXELS
    colorind = 0
    arr = []
    print("\nExtracting the text from the image...")
    for i in range(s):
        b = ""
        for k in range(config.NO_OF_BITS):
            if colorind == 3:
                colorind = 0
                c += 1
                if c == maxc:
                    c = 0
                    r += 1
                    if r == maxr:
                        print("Text size is greater than image size!")
            cur = list(px[r, c])
            b += bin(cur[colorind])[-1]
            colorind += 1
        arr.append(int(b, 2))
    return getstr(arr)


def extract(img):
    msg = extract_message(img)
    return msg
