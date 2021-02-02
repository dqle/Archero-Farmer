from ppadb.client import Client

def move_strategy(stage,device):
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