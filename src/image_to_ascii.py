import numpy as np
import math
import requests
  
from PIL import Image
  
# gray scale level values from: 
# http://paulbourke.net/dataformats/asciiart/

# stealing code from 
#https://www.geeksforgeeks.org/converting-image-ascii-image-python/
  
gscale2 = "@%#*+=-:. "

def getAverageL(image):
  
    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)
  
    # get shape
    w,h = im.shape
  
    # get average
    return np.average(im.reshape(w*h))

def url_to_ascii(url, cols): 
    im = Image.open(requests.get(url, stream=True).raw).convert('L')
    return image_to_ascii(im, cols)

def image_to_ascii(image, cols, scale = .43):
    # declare globals
    global gscale2
  
    # store dimensions
    W, H = image.size[0], image.size[1]
  
    # compute width of tile
    w = W/cols
  
    # compute tile height based on aspect ratio and scale
    h = w/scale
  
    # compute number of rows
    rows = int(H/h)
      
  
    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)
  
    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)
  
        # correct last tile
        if j == rows-1:
            y2 = H
  
        # append an empty string
        aimg.append("")
  
        for i in range(cols):
  
            # crop image to tile
            x1 = int(i*w)
            x2 = int((i+1)*w)
  
            # correct last tile
            if i == cols-1:
                x2 = W
  
            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))
  
            # get average luminance
            avg = int(getAverageL(img))
  
            # look up ascii char
            gsval = gscale2[int((avg*9)/255)]
  
            # append ascii char to string
            aimg[j] += gsval
      
    # return txt image
    return aimg