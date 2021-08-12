# Author: Dylan Smith
# Class: CS 361
# Description: This software is a microservice image transformer with the capabilities of resizing images and adding
#               transparent backgrounds.

from PIL import Image, ImageDraw

def image_resize(image):
    """
    Resizes image to 800x300 and applies two transparent cutouts of 200x100 to the top and bottom of the image at x=200
    :param image: The file name of the image to be transformed.
    :return: The resized, transparent image, saved as 'resized_image.png'.
    """
    img = Image.open(image)
    newsize = (800, 300)
    resized_img = img.resize(newsize)
    draw = ImageDraw.Draw(resized_img)
    # Apply transparent cutouts to top and bottom of image
    draw.rectangle((200, 0, 500, 100), fill=(255, 255, 255, 0), outline=(255, 255, 255, 0))
    draw.rectangle((200, 200, 500, 300), fill=(255, 255, 255, 0), outline=(255, 255, 255, 0))
    resized_img.save('new_image.png')
    return resized_img
