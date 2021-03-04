import os, sys
from PIL import Image

class ImageData:
    def __init__(self, size_x, size_y, pixel_values):
        self.size_x = size_x
        self.size_y = size_y
        self.pixel_values = pixel_values

class PixelartCreator:
    def __init__(self, pixelization_ratio: int, path: str):
        self.multiplier = pixelization_ratio
        self.path = path
        self.result_path = 'output.png'

    def pack_horizontally(self) -> list:
        new_pixels_array = []
        packer, avg_r, avg_g, avg_b = 0, 0, 0, 0
        for index, pixel in enumerate(self.image.pixel_values):       # horizontal packing
            avg_r += pixel[0]
            avg_g += pixel[1]
            avg_b += pixel[2]
            packer += 1
            if packer == self.multiplier or (index+1) % self.image.size_x == 0:
                for i in range(0, packer):
                    new_pixels_array.append([avg_r//packer, avg_g//packer, avg_b//packer])
                avg_r, avg_g, avg_b, packer = 0, 0, 0, 0
        return new_pixels_array

    def pack_vertically(self, pixel_values: list) -> list:
        new_pixels_array = list(pixel_values)
        avg_r, avg_g, avg_b = 0, 0, 0
        for i in range(0, self.image.size_x):      # vertical packing
            for h in range(0, self.image.size_y-1, self.multiplier):
                for j in range(0, self.multiplier):
                    if h+j >= self.image.size_y:
                        break
                    avg_r += new_pixels_array[(h+j)*self.image.size_x + i][0]
                    avg_g += new_pixels_array[(h+j)*self.image.size_x + i][1]
                    avg_b += new_pixels_array[(h+j)*self.image.size_x + i][2]
                for m in range(0, self.multiplier):
                    if h+m >= self.image.size_y:
                        break
                    new_pixels_array[(h+m)*self.image.size_x + i] = [avg_r//self.multiplier, avg_g//self.multiplier, avg_b//self.multiplier]
                avg_r = 0
                avg_g = 0
                avg_b = 0
        return new_pixels_array

    def get_result(self) -> int:
        extension = self.path.split(".")[-1]
        if not extension == "jpg" and not extension == "jpeg":
            print("Wrong input specified. (Image must be a jpg or jpeg)")
            return -1
        self.multiplier = 8          # 'pixelization' ratio (higher resolution => higher ratio should be set)
        try:
            im = Image.open(path, 'r')
        except:
            print("No input specified.")
            return -2
        self.image = ImageData(im.size[0], im.size[1], list(im.getdata()))
        if self.multiplier > min(self.image.size_x, self.image.size_y)//8 or self.multiplier < 1:
            print("Incorrect multiplier")
            return -3
        new_pixels_array = self.pack_vertically(self.pack_horizontally())
        list_of_pixels = [tuple(x) for x in new_pixels_array]
        im_f = Image.new(im.mode, (self.image.size_x, self.image.size_y))
        im_f.putdata(list_of_pixels)
        try:
            im_f.save(self.result_path)
        except:
            print("An error occured while saving.")
            return -4
        return 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "input.jpeg"
    pix_creator = PixelartCreator(8, path)
    err = pix_creator.get_result()
    if err < 0:
        print("Conversion failed.")