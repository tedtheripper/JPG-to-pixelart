import os, sys
from PIL import Image

path = 'input.jpg'
path_final = 'output.png'
multiplier = 8          # 'pixelization' ratio (higher resolution => higher ratio)
try:
    im = Image.open(path, 'r')
except:
    print("No input specified.")
    quit()
pix_val = list(im.getdata())
size_x = im.size[0]
size_y = im.size[1]
im_f = Image.new(im.mode, (size_x, size_y))

pix_n = []
packer = 0
avg_r = 0
avg_g = 0
avg_b = 0
index = 0
for p in pix_val:       # horizontal packing
    index += 1
    avg_r += p[0]
    avg_g += p[1]
    avg_b += p[2]
    packer += 1
    if packer == multiplier or index % size_x == 0:
        for i in range(0, packer):
            pix_n.append([avg_r//packer, avg_g//packer, avg_b//packer])
        avg_r = 0
        avg_g = 0
        avg_b = 0
        packer = 0
avg_r = 0
avg_g = 0
avg_b = 0
index = 0
for i in range(0, size_x):      # vertical packing
    for h in range(0, size_y-1, multiplier):
        for j in range(0, multiplier):
            if h+j >= size_y:
                break
            avg_r += pix_n[(h+j)*size_x + i][0]
            avg_g += pix_n[(h+j)*size_x + i][1]
            avg_b += pix_n[(h+j)*size_x + i][2]
        for m in range(0, multiplier):
            if h+m >= size_y:
                break
            pix_n[(h+m)*size_x + i] = [avg_r//multiplier, avg_g//multiplier, avg_b//multiplier]
        avg_r = 0
        avg_g = 0
        avg_b = 0

list_of_pixels = []
for x in pix_n:
    list_of_pixels.append(tuple(x))
im_f.putdata(list_of_pixels)
try:
    im_f.save(path_final)
except:
    print("An error occured (saving).")
    quit()