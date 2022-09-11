import sys

from PIL import Image

from config import config
from file_ops import readfile, saveimage
from math_ops import getpercent


def embedd_image(path1, path2):
    img1 = readfile(path1)
    img2 = readfile(path2)
    img2 =img2.convert("RGB")
    img1 =img1.convert("RGB")
    validate_image(img1, img2)
    embedd(img1, img2)


def validate_image(img1, img2):
    c1 = pixel_count(img1)[0]
    c2 = pixel_count(img2)[0]
    
    if c2 > config.BASE_RES:
        print(f'Please make the count of the pixels of second image to 1920x1080. You can use https://www.resizepixel.com/')
        quit()
    if pixel_count(img1)[0] < pixel_count(img2)[0]+8:
        print("Size of Primary image should greater than second image!")
        quit()


def pixel_count(img):
    r, c = img.size
    return r*c, r, c


def addsize(px, start, r):
    b = bin(r)[2:]
    b = ((config.NO_OF_IMG_PIXELS*3)-len(b))*"0"+b
    ind = 0
    for i in range(start, config.NO_OF_IMG_PIXELS+start):
        p = list(px[0, i])
        for j in range(3):
            if b[ind] == '0':
                if p[j] % 2 != 0:
                    p[j] -= 1
            else:
                if p[j] % 2 != 1:
                    p[j] += 1
            ind += 1
        px[0, i] = tuple(p)


def embedd(im1, im2):
    im1_pixel_count, r1, c1 = pixel_count(im1)
    im2_pixel_count, r2, c2 = pixel_count(im2)
    px1 = im1.load()
    px2 = im2.load()
    addsize(px1, 0, r2)
    addsize(px1, 4, c2)
    
    for ind in range(8, im2_pixel_count+8):
        sys.stdout.write("\rEmbedding image " +
                         str(getpercent(ind, im2_pixel_count))+"% done")
        sys.stdout.flush()
        i1 = ind//c1
        j1 = ind % c1
        i2 = (ind-8)//c2
        j2 = (ind-8) % c2
        pix1 = list(px1[i1, j1])
        pix2 = list(px2[i2, j2])
        # for k in range(3):
        #     pix1[k] = insert_num(pix1[k], pix2[k])
        px1[i1, j1] = _merge_rgb(pix1,pix2)
    sys.stdout.flush()
    saveimage(im1)


def extractsize(px, start, n):
    b = ""
    for i in range(start, n+start):
        p = px[0, i]
        for j in range(3):
            b += bin(p[j])[-1]

    return int(b, 2)


def extract_image(path1):
    img = readfile(path1)
    r1, c1 = img.size
    px = img.load()
    r2 = extractsize(px, 0, config.NO_OF_IMG_PIXELS)
    c2 = extractsize(px, 4, config.NO_OF_IMG_PIXELS)
    newimg = Image.new(img.mode, (r2, c2))
    px2 = newimg.load()
    for ind in range(8, (r2*c2)+8):
        sys.stdout.write("\rExtracting image " +
                         str(getpercent(ind, (r2*c2)))+"% done")
        sys.stdout.flush()
        i1 = ind//c1
        j1 = ind % c1
        i2 = (ind-8)//c2
        j2 = (ind-8) % c2
        pix1 = px[i1, j1]
        pix2 = list(px2[i2, j2])
        # for k in range(3):
        #     pix2[k] = extract_num(pix1[k])
        px2[i2, j2] = _unmerge_rgb(pix1)
    sys.stdout.flush()
    saveimage(newimg)

def _int_to_bin(rgb):
    """Convert an integer tuple to a binary (string) tuple.

    :param rgb: An integer tuple like (220, 110, 96)
    :return: A string tuple like ("00101010", "11101011", "00010110")
    """
    r, g, b = rgb
    return f'{r:08b}', f'{g:08b}', f'{b:08b}'

def _bin_to_int(rgb):
    """Convert a binary (string) tuple to an integer tuple.

    :param rgb: A string tuple like ("00101010", "11101011", "00010110")
    :return: Return an int tuple like (220, 110, 96)
    """
    r, g, b = rgb
    return int(r, 2), int(g, 2), int(b, 2)

def _merge_rgb(rgb1, rgb2):
    """Merge two RGB tuples.

    :param rgb1: An integer tuple like (220, 110, 96)
    :param rgb2: An integer tuple like (240, 95, 105)
    :return: An integer tuple with the two RGB values merged.
    """
    r1, g1, b1 = _int_to_bin(rgb1)
    r2, g2, b2 = _int_to_bin(rgb2)
    rgb = r1[:4] + r2[:4], g1[:4] + g2[:4], b1[:4] + b2[:4]
    return _bin_to_int(rgb)

def _unmerge_rgb(rgb):
    """Unmerge RGB.

    :param rgb: An integer tuple like (220, 110, 96)
    :return: An integer tuple with the two RGB values merged.
    """
    r, g, b = _int_to_bin(rgb)
    # Extract the last 4 bits (corresponding to the hidden image)
    # Concatenate 4 zero bits because we are working with 8 bit
    new_rgb = r[4:] + '0000', g[4:] + '0000', b[4:] + '0000'
    return _bin_to_int(new_rgb)
