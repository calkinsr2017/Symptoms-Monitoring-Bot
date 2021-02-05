import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from dotenv import load_dotenv
import datetime
load_dotenv()

databaseUrl = os.getenv('DATABASEURL')

#This file is to help create and manage the firebase database.
#In a .env file have a variable named DATABASEURL set to the url given in the realtime database.
 

class Firebase:
    def __init__(self):
        # Fetch the service account key JSON file contents

        #download firebase-sdk.json by going to the firebase project console and following these steps:
        # 1) Project settings -> Service accounts
        # 2) Click on the python tab to see the following code.
        # 3) click download new private key
        # 4) put in this directory and rename to firebase-sdk.json
        #It is in the gitignore because it is sensitive info
        self.cred = credentials.Certificate('firebase-sdk.json')
        
        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(self.cred, {
            'databaseURL': databaseUrl
        })

    
    #Dont use unless you have a fresh database. not a true representative of database.
    def setDataBase(self):
        ref = db.reference('/')
        ref.set({
                'users':
                    {
                        'Mike': {
                            'username': 'SET',
                            'password': "SET",
                            'passcodes': {
                                    0: '0',
                                    1: '0',
                                    2: '0',
                                    3: '0',
                                    4: '0',
                                    5: '0',
                                    6: '0',
                                    7: '0',
                                    8: '0',
                                    9: '0'
                                }

                        }

                    }
                })
    

    def getValues(self, user):
        ref = db.reference('users')
        username = ref.child(user).get()['username']
        password = ref.child(user).get()['password']
        
        passcodes = ref.child(user).get()['passcodes']
        return username, password, passcodes
        
    def setPasscodes(self, user:str, passcodes: list):
        ref = db.reference('users')
        currUser = ref.child(user)
        currUser.update({
            'passcodes' : passcodes
        })

if __name__ == '__main__':

    firebase = Firebase()

    #Dont call ever again
    #firebase.setDataBase()
