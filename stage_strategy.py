from ppadb.client import Client

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
        print ('Move Up for 1.5s')
        device.shell("input swipe 530 1635 530 1212 1500")  
        print ('Move Right for 0.64s')
        device.shell("input swipe 530 1635 920 1635 320") 
        print ('Move Up for 2.0s')
        device.shell("input swipe 530 1635 530 1212 2000")