import pyautogui
import schedule
import signal
import time
import os
import subprocess
import psutil
import datetime
import ctypes
import io
import ast
import sqlite3


def createDatabase():
#only used for first time setup
    conn = sqlite3.connect('lessonManager.db')
    c = conn.cursor()
    c.execute("""
                CREATE TABLE IF NOT EXISTS lessonRooms (
                lName text,
                lRoomCode integer,
                UNIQUE(lName)
                )""")
    c.execute("""
                CREATE TABLE IF NOT EXISTS lessonProgrammee (
                lName text,
                lDay text,
                lOrder integer
                )""")
    c.execute("""
                CREATE TABLE IF NOT EXISTS lessonTimes (
                lessonTime integer,
                lDay text,
                lOrder integer
                )""")
    conn.commit()
    conn.close()

def addNewRoom(lessonName,lessonCode):
    conn = sqlite3.connect('lessonManager.db')
    c = conn.cursor()
    try:
        c.execute(""" INSERT INTO lessonRooms VALUES (?, ?) """,(lessonName,lessonCode))
    except:
        print("This class already exists.")
    conn.commit()
    conn.close()

def viewLessonsCode(lessonName):
    conn = sqlite3.connect('lessonManager.db')
    c = conn.cursor()
    c.execute("SELECT * FROM lessonRooms WHERE lName=? ",(lessonName,))
    print(c.fetchall())
    conn.commit()
    conn.close()

def viewAllLessonCodes():
    conn = sqlite3.connect('lessonManager.db')
    c = conn.cursor()
    c.execute("SELECT * FROM lessonRooms")
    print(c.fetchall())
    conn.commit()
    conn.close()

def viewAllLessonTimes():
    conn = sqlite3.connect('lessonManager.db')
    c = conn.cursor()
    c.execute("SELECT * FROM lessonTimes")
    print(c.fetchall())
    conn.commit()
    conn.close()

def viewLessonsTime(lessonOrder,lessonDay):
    conn = sqlite3.connect('lessonManager.db')
    c = conn.cursor()
    c.execute("SELECT lessonTime FROM lessonTimes WHERE lOrder=? AND lDay=? ",(lessonOrder,lessonDay))
    for r in c.fetchall():
        print(r[0])
    conn.commit()
    conn.close()

def removeLessonCode(lessonName):
    conn = sqlite3.connect('lessonManager.db')
    c = conn.cursor()
    try:
        c.execute(""" DELETE FROM lessonRooms WHERE lName=? """,(lessonName,))
    except:
        print("This class does not exist.")
        pass
    conn.commit()
    conn.close()

def addNewLessonTime(lessonTime,lessonDay,lessonOrder):
    conn = sqlite3.connect('lessonManager.db')
    c = conn.cursor()
    try:
        c.execute(""" INSERT INTO lessonTimes VALUES (?, ?, ?) """,(lessonTime,lessonDay,lessonOrder))
    except:
        print("This lesson order already has a timeframe.")
    conn.commit()
    conn.close()

def removeLessonTime(lessonOrder):
    conn = sqlite3.connect('lessonManager.db')
    c = conn.cursor()
    try:
        c.execute(""" DELETE FROM lessonTimes WHERE lName=? """,(lessonOrder,))
    except:
        print("This lesson order does not have a time.")
        pass
    conn.commit()
    conn.close()

def retreiveByDay(lessonDay):
    conn = sqlite3.connect('lessonManager.db')
    c = conn.cursor()
    c.execute("SELECT lName,lOrder FROM lessonProgrammee WHERE lDay=? ",(lessonDay,))
    lessonCheck = []
    for r in c.fetchall():
        if(str(r[0]) not in lessonCheck):
            print(r[0])
            lessonCheck.append(r[0])
            retreiveOrderOf(r[0],lessonDay)
        elif(str(r[0]) in lessonCheck):
            pass
    conn.close()

def retreiveID(lessonDay):
    conn = sqlite3.connect('lessonManager.db')
    c = conn.cursor()
    c.execute("SELECT lName,lOrder FROM lessonProgrammee WHERE lDay=? ",(lessonDay,))
    first = c.fetchall()
    lessonOrder = {}
    for r in first:
        c.execute("SELECT lRoomCode FROM lessonRooms WHERE lName=? ",(r[0],))
        second = c.fetchall()
        for a in second:
            lessonOrder[r[1]] = a[0]
    conn.close()
    return lessonOrder



def lessonCount():
    todaysDate = datetime.datetime.today().weekday()
    if(todaysDate == 0):
        lessonDay = "monday"
    elif(todaysDate == 1):
        lessonDay = "tuesday"
    elif(todaysDate == 2):
        lessonDay = "wednesday"
    elif(todaysDate == 3):
        lessonDay = "thursday"
    elif(todaysDate == 4):
        lessonDay = "friday"
    elif(todaysDate == 5):
        lessonDay = "saturday"
    elif(todaysDate == 6):
        lessonDay = "sunday"
    conn = sqlite3.connect('lessonManager.db')
    c = conn.cursor()
    c.execute("SELECT lName,lOrder FROM lessonProgrammee WHERE lDay=? ",(lessonDay,))
    lessonCounter = []
    for r in c.fetchall():
        lessonCounter.append(r[0])
    return len(lessonCounter)

def retreiveTimeOf(lessonOrder,lessonDay,lessonID):
    conn = sqlite3.connect('lessonManager.db')
    c = conn.cursor()
    c.execute("SELECT lessonTime FROM lessonTimes WHERE lOrder=? AND lDay=? ",(lessonOrder,lessonDay))
    output = c.fetchall()
    conn.close()
    for r in output:
        schedule.every().day.at(str(r[0])).do(launchZoom,str(lessonID[0]))


def retreiveOrderOf(lessonName,lessonDay):
    conn = sqlite3.connect('lessonManager.db')
    c = conn.cursor()
    c.execute("SELECT lOrder FROM lessonProgrammee WHERE lName=? AND lDay=? ",(lessonName,lessonDay))
    output = c.fetchall()
    for r in output:
        c.execute("SELECT lRoomCode FROM lessonRooms WHERE lName=?",(lessonName,))
        output2 = c.fetchall()
        retreiveTimeOf(r[0],lessonDay,output2[0])
    conn.close()

def addNewLesson(lessonName,lessonDay,lessonOrder):
    conn = sqlite3.connect('lessonManager.db')
    c = conn.cursor()
    try:
        c.execute(""" INSERT INTO lessonProgrammee VALUES (?, ?, ?) """,(lessonName,lessonDay,lessonOrder))
    except Exception as e:
        print(e)
        print("This class already exists.")
    conn.commit()
    conn.close()

def mrScheduler():
    todaysDate = datetime.datetime.today().weekday()
    if(todaysDate == 0):
        retreiveByDay("monday")
    elif(todaysDate == 1):
        retreiveByDay("tuesday")
    elif(todaysDate == 2):
        retreiveByDay("wednesday")
    elif(todaysDate == 3):
        retreiveByDay("thursday")
    elif(todaysDate == 4):
        retreiveByDay("friday")
    elif(todaysDate == 5):
        retreiveByDay("saturday")
    elif(todaysDate == 6):
        retreiveByDay("sunday")

def launchZoom(roomID):
    pyautogui.hotkey("win","d")
    os.system("taskkill /im zoom.exe")
    time.sleep(2)
    try:
        zoom_path = os.getenv('APPDATA') + "\\Zoom\\bin\\Zoom.exe"
        subprocess.Popen(zoom_path)
    except FileNotFoundError:
        print("Project AutomateZoom Could Not Locate A Zoom Install In The Default Directory")
        print("Please Ensure That You Have Sucessfully Installed Zoom In Its Default Directory")
    time.sleep(5)
    enterLesson(roomID)

def enterLesson(roomID):
    for attempt in range(5):
        try:
            coordinates = pyautogui.locateOnScreen("zoom_join.PNG")
            clickingPoint = pyautogui.center(coordinates)
        except:
            print("Project AutomateZoom Could Not Locate The Zoom Window!")
            print("Retrying...")
            pyautogui.hotkey("win","d")
            os.system("taskkill /im zoom.exe")
            time.sleep(2)
            zoom_path = os.getenv('APPDATA') + "\\Zoom\\bin\\Zoom.exe"
            subprocess.Popen(zoom_path)
        else:
            break
    pyautogui.click(clickingPoint[0],clickingPoint[1])
    time.sleep(1)
    pyautogui.typewrite(str(roomID))
    time.sleep(2)
    pyautogui.press("tab", presses=4)
    pyautogui.press("enter")
    pyautogui.press("tab")
    pyautogui.press("enter")



def mainMenu(runArg):
    menu = {}
    if(runArg == 1):
        os.system('cls')
        print("Welcome to Project AutomateZoom v2.5, " + str(os.getenv('username')))
        date = datetime.datetime.now()
        print("Todays Date is: " + date.strftime("%x"))
    menu['1'] = "Schedule Lessons Of The Day"
    menu['2'] = "Room Related Options"
    menu['3'] = "Lesson Related Options"
    menu['4'] = "Time Related options"
    menu['5'] = "**Beta Features**"
    menu['6'] = "Exit"
    options = menu.keys()
    for entry in options:
        print(entry, menu[entry])
    menuAction = input("What would you like to do? ")
    return menuAction

def main():
    lessonNumber = 1
    try:
        createDatabase()
    except:
        pass
    while True:
            menuAction = mainMenu(1)
            if(menuAction == "1"):
                lessons = lessonCount()
                print("You have " + str(lessons) + " lessons today.")
                mrScheduler()
                print("Lessons have been scheduled, have a fun day!")
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            elif(menuAction == "2"):
                while True:
                    os.system('cls')
                    print("Room Related Options:")
                    menu = {}
                    menu['1'] = "Add New Room"
                    menu['2'] = "Remove Existing Room"
                    menu['3'] = "Print Existing Rooms"
                    menu['4'] = "Go Back To Main Menu"
                    options = menu.keys()
                    for entry in options:
                        print(entry, menu[entry])
                    subMenuAction = input("Please select one of the options. ")
                    if(subMenuAction == '1'):
                        lessonName = input("Please input the name of the lesson. ")
                        lessonCode = input("Please input the Zoom Meeting Code of the room of the lesson. ")
                        addNewRoom(lessonName,lessonCode)
                        print("New Room Code Has Been Added Successfully!")
                        time.sleep(1)
                    elif(subMenuAction == '2'):
                        print("The Following Rooms Can Be Removed: ")
                        viewAllLessonCodes()
                        lessonName = input("Please input the name of the lesson you want to remove. ")
                        removeLessonCode(lessonName)
                        print("The Room Has Been Removed Sucessfully!")
                        time.sleep(1)
                    elif(subMenuAction == '3'):
                        lessonName = input("Please input the name of the class you want to view room code of. ")
                        if lessonName.lower()=="all" :
                            viewAllLessonCodes()
                        else:
                            viewLessonsCode(lessonName)
                        noUse = input("Please press enter to continue...")
                    elif(subMenuAction == '4'):
                        break
                    continue
            elif(menuAction == "3"):
                while True:
                    os.system('cls')
                    print("Lesson Related Options:")
                    menu = {}
                    menu['1'] = "Add New Lesson"
                    menu['2'] = "Remove Existing Lesson"
                    menu['3'] = "Print Existing Lessons"
                    menu['4'] = "Go Back To Main Menu"
                    options = menu.keys()
                    for entry in options:
                        print(entry, menu[entry])
                    subMenuAction = input("Please select one of the options. ")
                    if(subMenuAction == "1"):
                        lessonDay = input("Which day do you want to add a lesson to? ").lower()
                        lessonName = input("What is the name of the lesson you want to add? ").lower()
                        lessonOrder = input("In which numerical order is this lesson in? (1 to 5) ")
                        addNewLesson(lessonName,lessonDay,lessonOrder)
                        print("New Lesson Has Been Added Successfully.")
                        noUse = input("Please press enter to continue...")
                    elif(subMenuAction == "2"):
                        lessonDay = input("Which day do you want to remove a lesson from? ").lower()
                        lessonOrder = input("What is the order of the lesson you want to remove? (1 to 5) ").lower()
                        realremovelesson(lessonDay,lessonOrder)
                        print("Existing Lesson Has Been Removed Successfully.")
                    elif(subMenuAction == "3"):
                        lessonDay = input("Which days lesson programme do you want to print? ").lower()
                        realviewlessons(lessonDay)
                        noUse = input("Please press enter to continue...")
                    elif(subMenuAction == "4"):
                        break
                    continue
            elif(menuAction == "4"):
                while True:
                    os.system('cls')
                    print("Time Related Options: ")
                    menu = {}
                    menu['1'] = "Add New Time For A Lesson"
                    menu['2'] = "Remove Existing Time For A Lesson"
                    menu['3'] = "Print Existing Times For Lessons"
                    menu['4'] = "Go Back To Main Menu"
                    options = menu.keys()
                    for entry in options:
                        print(entry, menu[entry])
                    subMenuAction = input("Please select one of the options. ")
                    if(subMenuAction == "1"):
                        lessonDay = input("Which day do you want to add a time for? ")
                        lessonOrder = input("Which lesson order do you want to add a time for? ")
                        lessonTime = input("What is the time for the desired lesson order? ")
                        addNewLessonTime(lessonTime,lessonDay,lessonOrder)
                    elif(subMenuAction == "2"):
                        print("The following times can be removed: ")
                        lessonOrder = input("What is the order of the lesson you want to remove the time for? ")
                        removeLessonTime(lessonOrder)
                        print("The Lesson Time Has Been Removed Sucessfully.")
                    elif(subMenuAction == "3"):
                        lessonDay = input("Please input the day you want to view times for. ")
                        lessonOrder = input("Please input the order of the class you want to view time of. ")
                        if lessonOrder.lower()=="all" :
                            viewAllLessonTimes()
                            noUse = input("Please press enter to continue...")
                        else:
                            viewLessonsTime(lessonOrder,lessonDay)
                            noUse = input("Please press enter to continue...")
                    elif(subMenuAction == "4"):
                        break
                    continue
            elif(menuAction == "6"):
                quit()
            elif(menuAction == "5"):
                lessonDay= input("Which day do you want to retreive the lessons of? ")
                retreiveByDay(lessonDay)
                while True:
                    schedule.run_pending()
                    time.sleep(1)
                noUse = input("Please press enter to continue...")
main()
