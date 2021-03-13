from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
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
from firebase import Firebase
load_dotenv()

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
        # Mike addition to get the latest version of chrome driver for you even if you have different chrome version
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
        #wait is set to 60 seconds
        self.wait = WebDriverWait(self.driver, 60)

        self.username = username
        self.password = password
        self.checkbox = None

    #This method will go through the process of going to the survey and filling it out
    def main(self, passcode, logInNeeded = True):
        print("Starting the main survey process")

        self.driver.get("https://return.umd.edu/covid/survey/")
        self.duoLogin(passcode)
        
        time.sleep(3)
        
        # Mike fix - have to use the input and check if it is already checked as that data can be cached
        self.checkbox = self.driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/form/div/div[4]/div/div[3]/div/div[1]/div/input")
        if self.checkbox.is_selected() == False:
            self.driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/form/div/div[4]/div/div[3]/div/div[1]/div/div").click()
            
        time.sleep(3)
        self.driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[3]/div/div/button").click()
        
        time.sleep(10)
        self.driver.close()
        
        
        
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


if __name__ == '__main__':

    firebase = Firebase()
    
    listOfUsers = firebase.getListOfUsers()
    #There is only one user (Mike) so it is just the first entry. If you scale this, you can iterate over the users
    currUser = listOfUsers[0]
    username, password, passcodes = firebase.getValues(currUser)

    print(username, password, passcodes)

    #Logic to get the latest code and see if you need to generate new passcodes
    passcode = 0
    needToGetnewPasscodes = False
    for i in range(len(passcodes)):
        if passcodes[i] != '0': 
            passcode = passcodes[i]
            passcodes[i] = '0'
            if i == 9: needToGetnewPasscodes = True
            break

    if needToGetnewPasscodes:
        print(username, ": Getting new passcodes")
        bot = Bot(username, password)
        passcodes = bot.getMorePasscodes(passcode)  #Selenium doing stuff
        passcode = passcodes[0] #Get the newest code
        passcodes[0] ='0'

    firebase.setPasscodes(currUser, passcodes)

    bot = Bot(username, password)
    bot.main(passcode) #Selenium doing stuff