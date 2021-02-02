from ppadb.client import Client
from image_manipulation import take_screenshot, crop_image
import cv2
import pytesseract

#Point to OCR Library
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_energy(device):
    #Get Current Screen
    take_screenshot(device)

    #Get Energy Bar Image
    crop_image("images/main_screen.png","images/energy.png",379,38,489,78)

    #Get Current Energy
    text = get_text("images/energy.png")
    text = text.split("/")[0]

    print("Current Energy is: " + text)
    
    try:
        current_energy = int(''.join(list(filter(str.isdigit, text))))
    except ValueError:
        print("Not an integer Energy Value. Might be a bug with OCR. Waiting and Trying again.")
        current_energy = 0

    return current_energy

def get_text(image_name_input):
    #Convert image to binarized grayscale
    image = cv2.imread(image_name_input)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #Tesseract OCR
    text = pytesseract.image_to_string(binary, lang="eng", config="--psm 13")
    text = text.strip()

    #Print Read Energy
    print("Tesseract OCR reports energy is: " + text)

    return text;