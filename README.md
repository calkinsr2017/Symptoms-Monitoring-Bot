# Symptoms-Monitoring-Bot

This is a working prototype.

NOTE: This assumes that you have your own firebase realtime database server. They are easy and free to set up. 

On your personal firebase server, go enter your username, password and one duo code in the last spot - index 9. When you run main.py it will generate 10 more for you and keep generating them when firebase doesn't detect anymore. 

Make a txt file called "secreturl.txt" and input your firebase url in there. Download the JSON file, which includes the following steps:

        #download firebase-sdk.json by going to the firebase project console and following these steps:
        # 1) Project settings -> Service accounts
        # 2) Click on the python tab to see the following code.
        # 3) click download new private key
        # 4) put in this directory and rename to firebase-sdk.json
        #It is in the gitignore because it is sensitive info

In order to use this projects full functionality you need to go through a few first steps when using on a new computer.

Download LATEST python from: https://www.python.org/downloads/ if using Windows.
Download the ChromeDriver and stick chromedriver.exe into your users bin folder. Make sure bin is in the environment variables path.
Example C:\Users\MPLEX\bin contains chromedriver.exe
Search for environment variables and click on "edit the system environment variables"
Click "Environment variables" and under System variables make sure C:\Users\MPLEX\bin is in PATH (Could be Path). Click edit to add or see if it exists.
Within the cloned repository open command prompt

Install the following modules with pip (part of python):
- run `pip install selenium` 
- run `pip install webdriver_manager` 
- run `pip install firebase_auth`
- run `pip install python-dotenv`

Run main.bat
