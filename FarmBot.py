from ppadb.client import Client
from PIL import Image
import numpy as np
import pytesseract
import time
import cv2

#Point to OCR Library
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Coordinate List - Update this if the game changes UI Layout
# (389,38,135,46) = Energy Bar
# (735,340,927,425) = The word "ability" for first skill selection when joined a stage
# (585,339,896,429) = The word "adventure" when level up past initial level up
# (360,170,720,270) = The word "Lucky" for Lucky Wheel!
# (615,195,785,245) = The word "Master" for Master
# (265,170,830,270) = Angel Region
# (440,610,650,750) = Door Location
# (940,655,1070,790) = Stage 6 Region to check for Unique End of Floor ID
# (12,930,1045,1320) = Stage 6 Region to check for Unique Start of floor ID
# (90, 1820) = Exit Met a Master and Mysterious Vendor
# (545, 1515) = Start Wheel Button
# (525, 1425) = Start Stage Button
# (215, 1280) = Left Skill to press
# (535, 1280) = Middle Skill to Press
# (875, 1280) = Right Skill to press

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
    text = text.strip()

    #Print Read Energy
    print("Tesseract OCR reports energy is: " + text)

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
    threshold = 0.9
    isMatch = False

    #num_result = np.amax(result)
    #print("RESULT =" + str(num_result))
    if np.amax(result) > threshold:
        isMatch = True

    return isMatch;

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

def what_screen(stage,device):
    #Get current screen
    take_screenshot(device)

    #check main menu
    if crop_and_compare_image("images/world.png", "tmp/check_world.png",360,1635,715,1915):
        print("At Main Menu - Check Current Energy")
        status = "MainMenu"
        pass

    #check ability page (first time joined dungeon)
    elif crop_and_compare_image("images/ability.png", "tmp/check_ability.png",90,320,1020,430):
        print("Picking Initial Skill")
        status = "StartedStage"
        pass

    #check if level up
    elif crop_and_compare_image("images/lvlup_adventure.png", "tmp/check_lvlup.png",140,340,980,430):
        print("Level up - Picking Skill")
        status = "LevelUp"
        pass

    #check Lucky Wheel!
    elif crop_and_compare_image("images/lucky_wheel.png", "tmp/check_luckywheel.png",360,170,720,270):
        print("Starting Lucky Wheel")
        status = "LuckyWheel"
        pass

    #check Special Wheel!
    elif crop_and_compare_image("images/reward.png", "tmp/check_specialwheel.png",320,170,750,260):
        print("Exiting Special Wheel")
        status = "SpecialWheel"
        pass

    #check Master
    elif crop_and_compare_image("images/master.png", "tmp/check_master.png",255,170,845,270):
        print("Met a Master")
        status = "Master"
        pass

    #check Mysterious Vendor
    elif crop_and_compare_image("images/vendor.png", "tmp/check_vendor.png",580,180,790,260):
        print("Mysterious Vendor")
        status = "Vendor"
        pass

    #check Angel
    elif crop_and_compare_image("images/angel.png", "tmp/check_angel.png",265,170,830,270):
        print("Found an Angel!")
        status = "Angel"
        pass

    #check Devil
    elif crop_and_compare_image("images/Devil.png", "tmp/check_devil.png",280,165,810,260):
        print("Met a Devil!")
        status = "Devil"
        pass

    #check New Skill
    elif crop_and_compare_image("images/new_skill.png", "tmp/check_newskill.png",325,330,750,430):
        print("Got a New Skill")
        status = "NewSkill"
        pass

    elif crop_and_compare_image("images/over.png", "tmp/check_gameover.png",333,390,750,500):
        print("Game Over - Going Back to Main Menu")
        status = "GameOver"
        pass

    #Stage Specific 
    elif stage == 6 and \
         (crop_and_compare_image("images/stage6_unique_start1.png", "tmp/check_start.png",12,930,1045,1820) or \
          crop_and_compare_image("images/stage6_unique_start2.png", "tmp/check_start.png",12,930,1045,1820) or \
          crop_and_compare_image("images/stage6_unique_start3.png", "tmp/check_start.png",12,930,1045,1820) or \
          crop_and_compare_image("images/stage6_unique_start4.png", "tmp/check_start.png",12,930,1045,1820)):
        print("New Floor")
        status = "NewFloor"
        pass

    elif stage == 6 and crop_and_compare_image("images/stage6_door.png", "tmp/check_door.png",220,580,880,1065):
        print("Door (Stage 6) is not open - Auto-Attacking")
        status = "Auto-Attack"
        pass

    elif stage == 6 and not crop_and_compare_image("images/stage6_door.png", "tmp/check_door.png",440,610,650,750) and \
         (crop_and_compare_image("images/stage6_unique_end1.png", "tmp/check_stage6end.png",527,300,780,860) or \
          crop_and_compare_image("images/stage6_unique_end2.png", "tmp/check_stage6end.png",527,300,780,860) or \
          crop_and_compare_image("images/stage6_unique_end3.png", "tmp/check_stage6end.png",527,300,780,860)):
        print("Door (Stage 6) is open")
        status = "MoveNextStage"
        pass

    #check dungeon completion
    elif crop_and_compare_image("images/surviving.png", "tmp/check_completion.png",135,370,955,525):
        print("Dungeon Completed")
        status = "Completed"
        pass

    #check door
    else:
        status = "Unknown"

    return status


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

#Connect To Device
device = connect_device()

#Prompt
stage = int(input("Select Stage (Available: 6): "))
stage_strat = int(input("Select Stage Strategy (1 - All Power; 2 - All Heal): "))
current_floor = int(input("What's the current floor? (Put 0 if in main menu): "))

#Quit if not valid state
if not stage in [3, 6]:
    print("Invalid Stage: " + stage)
    time.sleep(3)
    quit()

#Set next stag flag to unstuck
nextStage = 0
unknown_count = 0

#Start Farm Loop
while True:
    #Get current status
    current_status = what_screen(stage,device)

    if current_status == "MainMenu":
        #Get Current Energy
        current_energy = get_energy(device)

        #Start Stage if have enough energy
        if current_energy >= 5:
            print("Staring Level")
            device.shell("input tap 525 1425")
            #Initialize floor
            current_floor = 1
            max_floor = 20
            time.sleep(5)
        else:
            print("Not Enough Energy. Waiting 1 Minute")
            time.sleep(60)

    elif current_status == "StartedStage":
        device.shell("input tap 535 1280")
        time.sleep(1)
        device.shell("input swipe 530 1635 530 1212 1500")

    elif current_status == "NewFloor":
        print("Current Floor:" + str(current_floor))
        if current_floor in [1,3,5,6,8,10,11,13,15,16,17,18]:
            print("Start Move Strategy for Stage " + str(stage))
            move_strategy(stage,device)
        else:
            device.shell("input swipe 530 1635 530 1212 4000")
        current_floor += 1

    elif current_status == "LuckyWheel":
        time.sleep(2)
        device.shell("input tap 545 1515")
        time.sleep(8)
        device.shell("input swipe 530 1635 530 1212 1000")

    elif current_status == "Master" or current_status == "SpecialWheel" or current_status == "Vendor":
        time.sleep(3)
        device.shell("input tap 90 1820")
        time.sleep(1)
        device.shell("input swipe 530 1635 530 1212 1000")

    elif current_status == "Angel":
        if stage_strat == 1:
            device.shell("input tap 270 1410")
        elif stage_strat == 2:
            device.shell("input tap 780 1410")
        device.shell("input swipe 530 1635 530 1212 1000")
        time.sleep(3)

    elif current_status == "Devil":
        time.sleep(3)
        device.shell("input tap 300 1590")
        time.sleep(1)
        device.shell("input swipe 530 1635 530 1212 1000")

    elif current_status == "LevelUp":
        time.sleep(2)
        device.shell("input tap 535 1280")

    elif current_status == "NewSkill":
        device.shell("input tap 540 1280")

    elif current_status == "GameOver":
        device.shell("input tap 535 1880")
        device.shell("input tap 535 1280")
        time.sleep(5)

    elif current_status == "MoveNextStage":
        # Sleep 5 sec in case this triggers level up
        time.sleep(5)
        if nextStage == 0:
            #move up - right
            device.shell("input swipe 530 1635 950 1300 1000")
            nextStage = 1
        else:
            #move up - left
            device.shell("input swipe 530 1635 35 1300 1000")
            nextStage = 0
        time.sleep(2)

    elif current_status == "Auto-Attack":
        time.sleep(5)

    elif current_status == "Completed":
        time.sleep(5)
        device.shell("input tap 535 830")
        time.sleep(5)

    else:
        print("Unknown State. Trying screengrab again")
#        if unknown_count == 0:
#            print("Unknown State. Move left. Trying screengrab again")
#            device.shell("input swipe 530 1635 230 1635 1500")
#            unknown_count = 1
#        elif unknown_count == 1:
#            print("Unknown State. Move right. Trying screengrab again")
#            device.shell("input swipe 530 1635 830 1635 1500")
#            unknown_count = 2
#        else:
#            print("Unknown State. Moving Up. Trying screengrab again")
#            device.shell("input swipe 530 1635 530 1212 4000")
#            unknown_count = 0
        time.sleep(2)