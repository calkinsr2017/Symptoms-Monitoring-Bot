# Symptoms-Monitoring-Bot

This is a working prototype.

NOTE: This assumes that you have your own firebase realtime database server. They are easy and free to set up. 

On your personal firebase server, go enter your username, password and one duo code in the last spot. When you run main.py it will generate 10 more for you and keep generating them when firebase doesn't detect anymore. 

In firebase.py, either fetch it from conda or just hardcode it to the URL of your firebase server:

`databaseUrl = INSERT_YOUR_URL_HERE`

run `python3 main.py` from the conda enviornment. What I recommend doing is creating a conda envirnment and pip installing everything in the requrements.txt, and configuring the main.bat file to point to the environment. Look at my main.bat I have configured for my computer to know what to do. Then every day you just double click the main.bat file and life is good!

I can clear up whatever is confusing. 
