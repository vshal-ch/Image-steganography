import sys

from config import config
from file_ops import readfile, readtext, write_to_file
from image_steg import embedd_image, extract_image
from text import embedd, extract


def showusage():
    name = sys.argv[0]

    print(f"""\nUsage:
    \t{name} -h --> Manual page
\t{name} -em-image -im1 <im1> -im2 <im2> -o <oim> --> to embedd the image(im2) in the given image(im1), size(im1)>size(im2)
\t{name} -em -i <im> -t <m> -o <oim> --> to embedd the given message in the given image
\t{name} -em -i <im> -f <itf> -o <oim> --> to embedd the content of the given textfile in the given image
\t{name} -ex-image -i <im> -o <otf> --> to extract the hidden image in the given image and saving it in a new image file
\t{name} -ex -i <im> -o <otf> --> to extract the hidden message in the given image and writing it to the output path file
\t{name} -ex -i <im> -pr --> to extract the hidden message in the given image and writing it to the terminal
\nTags:
\t-em: to embedd text into image
\t-ex: to extract the text from image
\t-i : input image
\t-o : output path
\t-t : input text from terminal
\t-f : input text from a file
\t-pr: print to the terminal
\nTerms:
\tim: input image
\tm: messge to be hidden
\titf: input textfile
\toim: output image
\top: output textfile
    """)
    quit()


def show_output(msg):
    if sys.argv[4] == '-pr':
        print("\nExtracted text: \n"+msg+"\n")
    else:
        if write_to_file(sys.argv[5], msg):
            print("Successfully written to file")


def startprocess(path, text, tag):
    if tag == '-em':
        img = readfile(path)
        embedd(img, text)
    elif tag == '-ex':
        img = readfile(path)
        msg = extract(img)
        show_output(msg)
    elif tag == '-em-image':
        embedd_image(path, text)
    elif tag == '-ex-image':
        extract_image(path)


def validateargs(args):
    if len(args) == 0 or args[0] == '-h' or (args[0] != '-ex' and args[0] != '-em' and args[0] != '-em-image' and args[0] != '-ex-image'):
        return False
    if args[0] == '-em-image':
        if args[1] != '-im1' or args[3] != "-im2" or args[5] != "-o":
            return False
        return True
    if args[0] == '-ex-image':
        if args[1] != '-i' or args[3] != "-o":
            return False
        return True
    if args[0] == '-ex':
        if len(args) == 4:
            if args[1] != '-i' or args[3] != '-pr':
                return False
            return True
        if len(args) < 5 or args[1] != '-i' or args[3] != '-o':
            return False
    if args[0] == '-em':
        if len(args) < 7 or args[1] != '-i' or (args[3] != '-t' and args[3] != '-f') or args[5] != '-o':
            return False
    return True


def main():
    args = sys.argv[1:]
    flag = validateargs(args)
    if not flag:
        showusage()
    text = ''
    if args[0] == '-em' or args[0] == '-em-image':
        config.setoutputpath(args[6])
        if args[3] == '-f':
            text = readtext(args[4])
        else:
            text = args[4]
    if args[0] == '-ex-image':
        config.setoutputpath(args[4])
    startprocess(args[2], text, args[0])


if __name__ == "__main__":
    main()
