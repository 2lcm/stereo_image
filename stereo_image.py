import os
from PIL import Image
from PIL import ImageFilter
from utilities import *
import numpy as np

# It needs '.'
org_dir = "./All-2views"
res_dir = "./my_result"
window_width = 5

all_filters = [
    ImageFilter.BLUR,
    ImageFilter.CONTOUR,
    ImageFilter.DETAIL,
    ImageFilter.EDGE_ENHANCE,
    ImageFilter.EDGE_ENHANCE_MORE,
    ImageFilter.EMBOSS,
    ImageFilter.FIND_EDGES,
    ImageFilter.SHARPEN,
    ImageFilter.SMOOTH,
    ImageFilter.SMOOTH_MORE,
]


def myfunc(img1, img2, threshold):
    # img1 - left view, img2 - right view
    w, h = img1.size
    pw = window_width // 2
    res_img = Image.new(mode='L', size=img1.size)
    arr = np.full(shape=(h, w, w), fill_value=np.inf)
    for j in range(h-window_width):  # height
        if j % 10 == 0:
            print("j=", j)
        # hit = 0
        # miss = 0
        for i in range(w-window_width):  # width
            max_d = None
            val = 0
            for t in range(i+1):  # along X-axis
                # calculate sum of difference in window
                d = 0
                for a in range(window_width):
                    for b in range(window_width):
                        if arr[j+b][i+a][t+a] == np.inf:
                            px1 = img1.getpixel((i+a, j+b))
                            px2 = img2.getpixel((t+a, j+b))
                            tmp = 0
                            for index in range(len(px1)):
                                tmp += abs((px1[index] - px2[index]))
                                # tmp += (px1[index] - px2[index])**2
                            arr[j+b][i+a][t+a] = tmp
                            # miss += 1
                        # else:
                        #     hit += 1
                        d += arr[j+b][i+a][t+a]

                if max_d is None or max_d > d:
                    max_d = d
                    val = i-t
            val = 4*(val // 4)
            # if i-1 >= 0 and res_img.getpixel((i-1, j)) - (64+2*val) < threshold:
            #     res_img.putpixel((i-1, j), 64 + val)
            res_img.putpixel((i, j), 64+val)
        # print("hit:", hit)
        # print("miss:", miss)
    return res_img


if __name__ == "__main__":
    make_dir(res_dir)
    for cur in os.listdir(org_dir):
        make_dir(res_dir + "/" + cur)
        image1 = Image.open(org_dir + "/" + cur + "/view1.png")
        image2 = Image.open(org_dir + "/" + cur + "/view5.png")

        img1 = pad_image(image1, window_width // 2)  # reflective padding
        img2 = pad_image(image2, window_width // 2)

        # for itr in range(0,101,2):
        #     res_image = myfunc(img1, img2, itr)
        #     # res_image.show()
        #     res_image.save(res_dir + "/" + cur + "/res_"+str(itr)+".png")

        res_image = myfunc(img1, img2, 0)
        res_image.save(res_dir + "/" + cur + "/res_abs.png")

        for flt in all_filters:
            img1_filter = img1.filter(flt)
            img2_filter = img2.filter(flt)
            file_name = str(flt).split(".")[2].split("'")[0]
            res_image_filter = myfunc(img1_filter, img2_filter, None)
            res_image_filter.save(res_dir + "/" + cur + "/" + file_name + ".png")

        # one_color_image = Image.new('L', image1.size, 64)
        # one_color_image.save('64.png')

        # image1.save(res_dir + "/" + cur + "/view1.png")
        # image2.save(res_dir + "/" + cur + "/view5.png")
        break

