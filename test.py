from ppadb.client import Client
from PIL import Image
import numpy as np
import pytesseract
import time
import cv2

def connect_device():
    adb = Client(host='127.0.0.1',port=5037)
    devices = adb.devices()
    if len(devices) == 0:
        print("No Devices Attached")
        quit()
    return devices[0]

def take_screenshot(device):
    image = device.screencap()
    with open('images/main_screen.png', 'wb') as f:
        f.write(image)

def crop_image(image_name_input, image_name_output, x,y,w,h):
    img = Image.open(image_name_input)
    cropped_image = img.crop((x,y,w,h))
    cropped_image.save(image_name_output)

def get_text(image_name_input):
    #Convert image to binarized grayscale
    image = cv2.imread(image_name_input)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #Tesseract OCR
    text = pytesseract.image_to_string(binary, lang="eng", config="--psm 13")
    return text;

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
    threshold = 0.5
    isMatch = False

    num_result = np.amax(result)
    #print("RESULT =" + str(num_result))
    if np.amax(result) > threshold:
        isMatch = True

    return isMatch, num_result;

def current_energy():
    #Get Current Screen
    take_screenshot(device)

    #Get Energy Bar Image
    crop_image("images/main_screen.png","images/energy.png",379,38,489,78)

    #Get Current Energy
    text = get_text("images/energy.png")
    text = text.split("/")[0]
    current_energy = int(''.join(list(filter(str.isdigit, text))))

    return current_energy;

def move_strategy(stage,device):
    if stage == 6:
        print ('Move Up for 1.5s')
        device.shell("input swipe 530 1635 530 1212 1500") 
        print ('Move Left for 0.32s')
        device.shell("input swipe 530 1635 100 1635 320")  
        print ('Move Up for 0.5s')
        device.shell("input swipe 530 1635 530 1212 500")  
        print ('Move Right for 0.64s')
        device.shell("input swipe 530 1635 920 1635 320") 
        print ('Move Up for 0.7s')
        device.shell("input swipe 530 1635 530 1212 700")
        print ('Move Left for 0.625s')
        device.shell("input swipe 530 1635 100 1635 625")
        print ('Move Up for 0.6s')
        device.shell("input swipe 530 1635 530 1212 600") 
        print ('Move Right for 0.7s')
        device.shell("input swipe 530 1635 920 1635 700") 
        print ('Move Up for 1.5s')
        device.shell("input swipe 530 1635 530 1212 1000")

def move_strategy2(stage,device):
    if stage == 6:
        print ('Move Up for 1.5s')
        device.shell("input swipe 530 1635 530 1212 1500") 
        print ('Move Left for 0.32s')
        device.shell("input swipe 530 1635 100 1635 320")  
        print ('Move Up for 2.0s')
        device.shell("input swipe 530 1635 530 1212 2000")  
        print ('Move Right for 0.32s')
        device.shell("input swipe 530 1635 920 1635 320") 
        print ('Move Up for 2.0s')
        device.shell("input swipe 530 1635 530 1212 2000")
    elif stage == 3:
        print ('Move Up for 1.6s')
        device.shell("input swipe 530 1635 530 1212 1600") 
        print ('Move Left for 0.32s')
        device.shell("input swipe 530 1635 100 1635 320")
        print ('Move Up for 0.5s')
        device.shell("input swipe 530 1635 530 1212 500")  
        print ('Move Right for 0.32')
        device.shell("input swipe 530 1635 920 1635 320") 
        print ('Move Up for 0.9s')
        device.shell("input swipe 530 1635 530 1212 900")
        print ('Move Right for 1.0s')
        device.shell("input swipe 530 1635 920 1635 1000") 
        print ('Move Up for 2s')
        device.shell("input swipe 530 1635 530 1212 2000")
        print ('Move Left for 0.5s')
        device.shell("input swipe 530 1635 100 1635 500")
        print ('Move Down for 1.0s')
        device.shell("input swipe 530 1600 530 1900 1000")
        print ('Move Left for 0.5s')
        device.shell("input swipe 530 1635 100 1635 500")
        print ('Move Up for 1.0s')
        device.shell("input swipe 530 1635 530 1212 1000")
        print ('Move Right for 0.5s')
        device.shell("input swipe 530 1635 920 1635 500") 
        print ('Move Up for 1.0s')
        device.shell("input swipe 530 1635 530 1212 1000")

def get_energy():
    main_screen = Image.open("images/main_screen.png")
    main_screen_rgb = main_screen.convert("RGB")
    energy_pixel_value = main_screen_rgb.getpixel((374,65))
    return energy_pixel_value
    

#def what_screen(image_name_input):
    

#Connect To Device
device = connect_device()

#Get Current Screen
take_screenshot(device)


#Crop
#crop_image("images/main_screen.png","images/ability.png",640,800,850,885)

#boo, value = crop_and_compare_image("images/stage6_unique_end3.png", "tmp/check_stage6end.png",527,300,780,860)
#print(value)

move_strategy2(6,device)

#Get Text
#text = get_text("images/ability.png")
#print(text.strip())