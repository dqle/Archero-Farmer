from ppadb.client import Client
from PIL import Image
import numpy as np
import cv2

def crop_image(image_name_input, image_name_output, x,y,w,h):
    img = Image.open(image_name_input)
    cropped_image = img.crop((x,y,w,h))
    cropped_image.save(image_name_output)

def crop_and_compare_image(compare_image_name, crop_image_name, x,y,w,h):
    #Crop Image
    crop_image("images/main_screen.png",crop_image_name,x,y,w,h)

    #load Image
    imageA = cv2.imread(compare_image_name)
    imageB = cv2.imread(crop_image_name)

    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    #Match result
    result = cv2.matchTemplate(grayA, grayB, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    isMatch = False

    #num_result = np.amax(result)
    #print("RESULT =" + str(num_result))
    if np.amax(result) > threshold:
        isMatch = True

    return isMatch;

def take_screenshot(device):
    image = device.screencap()
    with open('images/main_screen.png', 'wb') as f:
        f.write(image)

def get_energy():
    main_screen = Image.open("images/main_screen.png")
    main_screen_rgb = main_screen.convert("RGB")
    energy_pixel_value = main_screen_rgb.getpixel((370,64))
    print("Energy Pixel RGB value is: " + str(energy_pixel_value))
    return energy_pixel_value