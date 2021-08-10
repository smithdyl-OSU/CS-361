# Author: Dylan Smith
# Class: CS 361
# Description: This software is a microservice image transformer with the capabilities of resizing images and adding
#               transparent backgrounds.

from PIL import Image

def image_resize(param):
    """
    Resizes Image in the specified Dimension to the requested number of pixels, Base.
    Maintains the image ratio of height and width.
    :param base: The new dimension in pixels that the image should be.
    :param dimension: Either 'width' or 'height', the dimension that base refers to.
    :param image: The file name of the image to be transformed.
    :return: The resized image, saved as 'resized_image.jpg'.
    """

    dimension = param['dimension']
    base = param['base']
    img = Image.open(param["image"])
    if dimension == 'width':
        # Resizes to Base pixels in width dimension, keeping appropriate ratio
        wpercent = (base / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((base, hsize), Image.ANTIALIAS)
    elif dimension == 'height':
        # Resizes to Base pixels in height dimension, keeping appropriate ratio
        hpercent = (base / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, base), Image.ANTIALIAS)
    img.save('resized_image.jpg')

def image_trans(param):
    """
    Adds a transparent background to Image. The image should start with a white background.
    :param image: The file name of the image to be transformed.
    :return: The transformed image, saved as 'transparent_image.png'.
    """
    img = Image.open(param["image"])
    rgba = img.convert('RGBA')
    datas = rgba.getdata()
    newData = []  # Temporary storage space for new rgba data
    for item in datas:
        #Iterate through the data of the image
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            # White pixel found, replace with transparent pixel
            newData.append((255, 255, 255, 0))
        else:
            # Non-white pixel, append to newData
            newData.append(item)
    rgba.putdata(newData)  # Replace old rgba data with newData
    rgba.save('transparent_image.png', 'PNG')
