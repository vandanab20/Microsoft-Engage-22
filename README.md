# Tracking Attendance by Face Recognition

 This is a project that I made for Microsoft Engage 2022. This project aims to digitalize Attendance Tracking via Face Recognition in order to increase efficiency and to reduce manual work.

## Instructions and Build
In the development of this project, I have used Flask, dlib, Face_recognition, javascript. 
- The user will have to create a images folder that contains train and test folder
- Then in train folder create folders named YOUR_NAME.jpg and in that folders upload images as YOUR_NAME_1.jpg,YOUR_NAME_2.jpg,YOUR_NAME_3.jpg.....
- Name in MARKED_ATTENDANCE.csv is saved as YOUR_NAME.jpg
- Create a MARKED_ATTENDANCE.csv file to get the marked attendance and copy its path in lmao.py
- In the app go to Attendance page and capture the image.
- In f_recognize function call, copy the path of test and train directory in lmao.py.
Run the following commads to clone the repo: 
```shell
git clone https://github.com/vandanab20/Microsoft-Engage-22
cd Microsoft-Engage-22
flask run
```
Link for MARKED_ATTENDANCE.csv file
<a href= "https://drive.google.com/file/d/1Y-wweisH5ww1xl5_8mxxKkhF5t_wEYHd/view?usp=sharing">https://drive.google.com/file/d/1Y-wweisH5ww1xl5_8mxxKkhF5t_wEYHd/view?usp=sharing</a> 
