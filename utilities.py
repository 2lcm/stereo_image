import os
from PIL import Image


def make_dir(dir_name):
    directory = os.path.dirname(dir_name)
    if not os.path.exists(directory):
        os.mkdir(dir_name)
        return True
    return False


def pad_image(image, pw):
    a, b = image.size
    pad_image = Image.new(mode=image.mode, size=(a+2*pw, b+2*pw), color=(255, 255, 255))

    flip_y = True
    for start_y in range(-b, b+1, b):
        flip_x = True
        for start_x in range(-a, a+1, a):
            for j in range(b):
                for i in range(a):
                    if -pw <= start_x + i < a+pw and -pw <= start_y + j < b+pw:
                        if flip_x:
                            p1 = a-1-i
                        else:
                            p1 = i
                        if flip_y:
                            p2 = b-1-j
                        else:
                            p2 = j
                        pad_image.putpixel((start_x + i+pw, start_y + j+pw), image.getpixel((p1, p2)))
            flip_x = not flip_x
        flip_y = not flip_y

    return pad_image