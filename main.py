import os, sys
from PIL import Image

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = "input.jpeg"
ext = path.split(".")
if not ext[-1] == "jpg" and not ext[-1] == "jpeg":
    print("Wrong input specified. (Image must be a jpg or jpeg)")
    exit()
path_final = 'output.png'
multiplier = 8          # 'pixelization' ratio (higher resolution => higher ratio should be set)
try:
    im = Image.open(path, 'r')
except:
    print("No input specified.")
    exit()
pix_val = list(im.getdata())
size_x, size_y = im.size[0], im.size[1]
if multiplier > min(size_x, size_y)//8 or multiplier < 1:
    print("Incorrect multiplier")
    exit()
im_f = Image.new(im.mode, (size_x, size_y))

new_pixels = []
packer, avg_r, avg_g, avg_b, index = 0, 0, 0, 0, 0
for p in pix_val:       # horizontal packing
    index += 1
    avg_r += p[0]
    avg_g += p[1]
    avg_b += p[2]
    packer += 1
    if packer == multiplier or index % size_x == 0:
        for i in range(0, packer):
            new_pixels.append([avg_r//packer, avg_g//packer, avg_b//packer])
        avg_r, avg_g, avg_b, packer = 0, 0, 0, 0

avg_r, avg_g, avg_b, index = 0, 0, 0, 0
for i in range(0, size_x):      # vertical packing
    for h in range(0, size_y-1, multiplier):
        for j in range(0, multiplier):
            if h+j >= size_y:
                break
            avg_r += new_pixels[(h+j)*size_x + i][0]
            avg_g += new_pixels[(h+j)*size_x + i][1]
            avg_b += new_pixels[(h+j)*size_x + i][2]
        for m in range(0, multiplier):
            if h+m >= size_y:
                break
            new_pixels[(h+m)*size_x + i] = [avg_r//multiplier, avg_g//multiplier, avg_b//multiplier]
        avg_r = 0
        avg_g = 0
        avg_b = 0

list_of_pixels = [tuple(x) for x in new_pixels]
im_f.putdata(list_of_pixels)
try:
    im_f.save(path_final)
except:
    print("An error occured while saving.")
    quit()