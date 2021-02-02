## Python Package Import
import time

## Helper Function Import
from check_screen import what_screen
from adb_device import connect_device
from image_manipulation import get_energy
from stage_strategy import move_strategy

#Connect To Device
device = connect_device()

#Prompt
stage = int(input("Select Stage (Available: 6): "))
stage_strat = int(input("Select Stage Strategy (1 - All Power; 2 - All Heal): "))
print("To continue a floor, move your character to the bottom-middle of the stage and enter floor number. Otherwise, put 0 if at main menu.")
current_floor = int(input("What's the current floor?: "))

#Quit if not valid state
if not stage in [3, 6]:
    print("Invalid Stage: " + stage)
    time.sleep(3)
    quit()

#Set next stag flag to unstuck
nextStage = 0

#Start Farm Loop
while True:
    #Get current status
    current_status = what_screen(stage,device)

    if current_status == "MainMenu":
        #Wait 5 seconds since sometime the energy bar hasn't adjust proeprly yet
        time.sleep(5)

        #Get Current Energy
        energy_r, energy_g, energy_b = get_energy()

        #Start Stage if have enough energy
        if 34 < energy_r < 44 and \
           173 < energy_g < 183 and \
           33 < energy_b < 43:
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
        elif current_floor == 20:
            print("Fighting Last Boss. Wait 10 Seconds.")
            time.sleep(10)
            device.shell("input swipe 530 1635 530 1212 4000")
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
        time.sleep(2)