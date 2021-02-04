from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
import getpass
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import threading
from dotenv import load_dotenv
import datetime
load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

#So here is the dealio. I did most of this code for my eppley bot where I had to bypass duo. I am trying to copy and paste as much as possible.

class Bot:

    def __init__(self, username, password):
        #No idea what most of this does... Just leave it
        option = Options()
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument("--disable-infobars")
        #IF YOU WANT TO SEE THE CHROMEDRIVER DO ITS THING MAKE THIS FALSE. MAKE IT TRUE TO HAVE IT GO WITH NO GUI
        option.headless = False
        option.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", { 
            "profile.default_content_setting_values.notifications": 1 
        })

        #Main selenium driver
        self.driver = webdriver.Chrome(options=option)
        #wait is set to 60 seconds
        self.wait = WebDriverWait(self.driver, 60)

        self.username = username
        self.password = password

    #This method will go through the process of going to the survey and filling it out
    def main(self, link, passcode, logInNeeded = True):
        #do stuff

        #Mike here are the questions I need answered in order to finish this method.

        #1) How do you want this to run? Manually run this file once you wake up in the morning with everything downloaded on your computer?
            #If you keep your desktop on overnight you can schedule a job to run this file
            #I think I might be able to make an executable that you just double click and go brush your teeth. 
            #I can put it on docker and put it in a google cloud instance for you ($7 bucks a month ish)
            #Somehow get it on AWS, its free but I have never done it. 
        #2) DUO codes need to be used in order to have it login, I can have those stored in a file and keep them local or 
            #Put them in a firebase realtime database. I dont know how complicated you want this

        #Let me know what your imagining when you want the survey to be done automatically. 

    

        
    #This method is responsible for getting past duo. Now in order to not have to get a push notification to your phone
    #I am using the duocodes that can be generated. You can get 10 at a time. I used firebase to store the 10 codes and then
    #when i get to the last one the generate passcode function gets called. This uses the chromedriver to scrape 10 more.
    def duoLogin(self, passcode):
        print("Duo login initiated")
        userName = self.wait.until(EC.presence_of_element_located((By.ID, 'username')))
        userName.send_keys(self.username)

        password = self.driver.find_element_by_id('password')
        password.send_keys(self.password)
        password.send_keys(Keys.ENTER)

        self.driver.switch_to.frame(self.wait.until(EC.presence_of_element_located((By.ID, 'duo_iframe'))))
        passCodeBtn = self.driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/form/div[1]/fieldset[1]/div[3]/button')
        ActionChains(self.driver).click(passCodeBtn).perform()
        time.sleep(1)
        passCodeInput = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'passcode-input')))
        passCodeInput.send_keys(passcode)
        passCodeInput.send_keys(Keys.ENTER)

        self.driver.switch_to.default_content()
        print("Logged in successfully")

    #This is probably the best part of the code. It automatically goes and generates 10 more and returns them as a list
    #IMPORTANT: it needs 1 code to login and generate 10 more!!!
    def getMorePasscodes(self, passcode):
        self.driver.get("https://identity.umd.edu/mfaprofile")
        time.sleep(2)
        self.duoLogin(passcode)
        generateCodeBtn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[3]/div[1]/div/div[2]/form/div/div[3]/input')))
        ActionChains(self.driver).click(generateCodeBtn).perform()
        
        self.driver.switch_to_alert().accept()

        self.driver.switch_to.default_content()
        passCodeList = []
        for i in range(1, 11):
            passCodeList.append(self.driver.find_element_by_xpath('/html/body/div/div[3]/div[1]/div/div[{}]'.format(i)).text)

        self.driver.close()
        return passCodeList