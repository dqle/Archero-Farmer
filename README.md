# Archero-Farmer

![Archero Farmer Icon](https://github.com/dqle/Archero-Farmer/blob/master/repo_images/archero-farmer.png)

Tired of "wasting" Stamina while you're sleeping? Want to min-max your gameplay? Too busy to be able to play Archero? Archero-Farmer got your back!

## Introduction
Archero-Farmer is an Archero bot that work on NOX emulator. Its function is to continuously start a stage and play it based on available energy. The bot is based on Python and is using OpenCV to achieve this feat.

- Supported Emulator Settings
    - NOX Emulator Version 7.0.0.8 
        - Resolution: Mobile Phone Resolution 1080 x 1920
        - Performance: High (4 Core CPU, 4096 MB Memory)
  
- Supported Stage
    - 3\. Abandoned Dungeon : SEMI-STABLE - 18/20 run completion rate
    - 6\. Cave of Bones : STABLE - 20/20 run completion
  
- Equipment
    - Does **NOT** support **Enlightenment** book
    - Recommended equipment for farming:
        - Dodge Equipment
        - Lifesteal Equipment
        - Pets that can attack through wall
        - Auto activate ult book
    
- Hero
    - Does **NOT** support **Ayana**

## Installation (Windows)

- Install latest Python 3: https://www.python.org/downloads/
    - When installing, select **Add to PATH**
- Install Python Package:
    - Open a Command Line (CMD) and copy paste below:
      > pip install opencv-python pillow numpy pure-python-adb
    - If this doesn't work, you need to reinstall python and select **Add to PATH** option during installation
- Install ADB:
    - Download here: https://developer.android.com/studio/releases/platform-tools
        - Direct Link for Windows:  https://dl.google.com/android/repository/platform-tools-latest-windows.zip
    - Extract the contents of this zip file into C:\ drive
        - You should have a folder in C:\ called **platform-tools** - e.g. C:\platform-tools
    - Type WIN + R to bring up the Run command and put in **SystemPropertiesAdvanced**
    - Click on **Environment Variables**
        - Under **System Variables** list > Find **Path** > Click on it and click **Edit** > Click **New** on the **Edit environment variable** windows > Put in **C:\platform-tools** > OK > OK
- Install NOX:
    - Download here: https://www.bignox.com/
        - Version 7.0.0.8 Direct Link: https://drive.google.com/file/d/1RKVNUsXVZFTZI-SJP8CZvLZcDqU2Ujzz/view
    - Settings:
        - Resolution Type: Mobile Phone 
        - Resolution: 1080 x 1920
        - Performance: High (4 Core CPU, 4096 MB Memory)
    - Archero Settings:
        - Graphics: High

## Usage

- Download the latest release build on the release page: https://github.com/dqle/Archero-Farmer/releases
- Open NOX Android Emulator and start up Archero
- Select stage on the main menu and then run **Archero-Farmer.py** to start the bot
- Fill out the survey prompted on the bot
![Survey](https://github.com/dqle/Archero-Farmer/blob/master/repo_images/program-output-1.PNG)
