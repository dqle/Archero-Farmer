from ppadb.client import Client
from image_manipulation import take_screenshot, crop_and_compare_image

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
    elif stage == 3 and \
        (crop_and_compare_image("images/stage3_unique_start1.png", "tmp/check_start.png",0,800,1080,1300) or \
         crop_and_compare_image("images/stage3_unique_start2.png", "tmp/check_start.png",0,800,1080,1300) or \
         crop_and_compare_image("images/stage3_unique_start3.png", "tmp/check_start.png",0,800,1080,1300) or \
         crop_and_compare_image("images/stage3_unique_start4.png", "tmp/check_start.png",0,800,1080,1300) or \
         crop_and_compare_image("images/stage3_unique_start5.png", "tmp/check_start.png",0,800,1080,1300) or \
         crop_and_compare_image("images/stage3_unique_start6.png", "tmp/check_start.png",0,800,1080,1300) or \
         crop_and_compare_image("images/stage3_unique_start7.png", "tmp/check_start.png",0,800,1080,1300) or \
         crop_and_compare_image("images/stage3_unique_start8.png", "tmp/check_start.png",0,800,1080,1300)):
        print("New Floor")
        status = "NewFloor"
        pass

    elif stage == 3 and crop_and_compare_image("images/stage3_door.png", "tmp/check_door.png",220,580,880,1065):
        print("Door (Stage 3) is not open - Auto-Attacking")
        status = "Auto-Attack"
        pass

    elif stage == 3 and not crop_and_compare_image("images/stage3_door.png", "tmp/check_door.png",8,288,1073,1137) and \
         (crop_and_compare_image("images/stage3_unique_end1.png", "tmp/check_stage3end.png",8,288,1073,1137) or \
          crop_and_compare_image("images/stage3_unique_end2.png", "tmp/check_stage3end.png",8,288,1073,1137) or \
          crop_and_compare_image("images/stage3_unique_end3.png", "tmp/check_stage3end.png",8,288,1073,1137)):
        print("Door (Stage 3) is open")
        status = "MoveNextStage"
        pass

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