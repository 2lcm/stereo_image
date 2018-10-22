import os
from PIL import Image
from PIL import ImageFilter
from utilities import *
# It needs '.'
org_dir = "./All-2views"
res_dir = "./my_result"
window_width = 3


def myfunc(img1, img2):
    w, h = img1.size
    pw = window_width // 2
    res_img = Image.new(mode='L', size=img1.size)
    for j in range(h-window_width):  # height
        if j % 10 == 0:
            print("j=", j)
        for i in range(w-window_width):  # width
            max_d = None
            val = 0
            arr = [[None]*3]*3
            for t in range(i+1):  # along X-axis
                # calculate sum of difference in window
                d = 0
                for a in range(window_width):
                    for b in range(window_width):
                        if arr[b][a] is None:
                            px1 = img1.getpixel((i+a, j+b))
                            px2 = img2.getpixel((t+a, j+b))
                            tmp = 0
                            for index in range(len(px1)):
                                tmp += (px1[index] - px2[index]) ** 2
                            arr[b][a] = tmp
                        d += arr[b][a]
                for b in range(window_width):
                    arr[b] = arr[b][1:window_width]
                    arr[b].append(None)

                if max_d is None or max_d > d:
                    max_d = d
                    val = t-i

                res_img.putpixel((i, j), 64-int(val/w*255))
    return res_img


if __name__ == "__main__":
    make_dir(res_dir)
    for cur in os.listdir(org_dir):
        make_dir(res_dir + "/" + cur)
        image1 = Image.open(org_dir + "/" + cur + "/view1.png")
        image2 = Image.open(org_dir + "/" + cur + "/view5.png")

        img1 = pad_image(image1, window_width // 2)  # reflective padding
        img2 = pad_image(image2, window_width // 2)
        # img1_blur = img1.filter(ImageFilter.BLUR)
        # img2_blur = img2.filter(ImageFilter.BLUR)

        res_image = myfunc(img1, img2)
        # res_image.show()
        # res_image_blur = myfunc(img1_blur, img2_blur)
        one_color_image = Image.new('L', image1.size, 64)
        one_color_image.save('64.png')

        # image1.save(res_dir + "/" + cur + "/view1.png")
        # image2.save(res_dir + "/" + cur + "/view5.png")
        res_image.save(res_dir + "/" + cur + "/res.png")

        # res_image_blur.save(res_dir + "/" + cur + "/res_blur.png")
        break

