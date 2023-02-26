import re

import requests
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup

import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from tkinter import messagebox

root = tk.Tk()
root.title("GUC Schedule")
root.configure(bg="#eeeeee")
root.geometry("3000x600")

username_label = tk.Label(root, text="username:", fg="black", bg="#eeeeee")
username_label.grid(row=0, column=0)
username = tk.Entry(root)
username.grid(row=0, column=1)

password_label = tk.Label(root, text="password:", fg="black", bg="#eeeeee")
password_label.grid(row=1, column=0)
password = tk.Entry(root, show="*")
password.grid(row=1, column=1)

# Create a list of column headers
column_headers = ["First Slot", "Second Slot", "Third Slot", "Fourth Slot", "Fifth Slot"]

# Create a list of row headers
row_headers = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]

# Create a table using a nested for loop
for i in range(1, 8):
    for j in range(1, 7):
        # Skip the first cell
        if i == 1 and j == 1:
            continue
        # Create the column headers in the first row
        elif i == 1:
            label = tk.Label(root, text=column_headers[j-2], padx=10, pady=10, relief=tk.RIDGE)
            label.grid(row=i+5, column=j, sticky=tk.NSEW)
        # Create the row headers in the first column
        elif j == 1:
            label = tk.Label(root, text=row_headers[i-2], padx=10, pady=10, relief=tk.RIDGE)
            label.grid(row=i+5, column=j, sticky=tk.NSEW)
        # Create the empty cells
        else:
            label = tk.Label(root, text="", padx=10, pady=10, relief=tk.RIDGE)
            label.grid(row=i+5, column=j, sticky=tk.NSEW)

# username = input("Enter your username: ")
# password = input("Enter your password: ")

###################### COURSES #####################
# resp = requests.get('https://cms.guc.edu.eg', auth=HttpNtlmAuth(username, password))
# if resp.status_code != 200:
#     print("An Error Occurred. Check Credentials And Try Again.")
# else:
#     courseSoup = BeautifulSoup(resp.text, 'html.parser')
#     myCourses = courseSoup.find_all(id='ContentPlaceHolderright_ContentPlaceHoldercontent_GridViewdiss')

########################### DISPLAYING THE COURSES ###########################
# for i in myCourses[0].select('td:first-child'):
#     print(i.text)


###################### SCHEDULES #####################


def get_schedule():
    schedResp = requests.get('https://student.guc.edu.eg/Web/Student/Schedule/GroupSchedule.aspx',
                            auth=HttpNtlmAuth(username.get(), password.get()))
    if schedResp.status_code != 200:
        print("An Error Occurred. Check Credentials And Try Again.")
    else:
        schedSoup = BeautifulSoup(schedResp.text, 'html.parser')

        def removeBlanks(string):
            return string != ''


        def removeUnwanted(string):
            return string.replace("\t", "").replace("\r", "")


        ########################### EXTRACTING ROW DATA (EACH DAY) ###########################
        sched = schedSoup.find_all(id='scdTbl')
        schedArrayTemp = []

        for i in sched[0].find_all('tr', {"id": re.compile('^Xrw')}):
            dayTemp = list(filter(removeBlanks, i.text.split('\n')))
            dayTemp2 = list(map(removeUnwanted, dayTemp))
            day = list(filter(removeBlanks, dayTemp2))
            schedArrayTemp.append(day)

        ########################### GROUPING TUTS/LABS AS ONE SLOT ###########################
        schedArray = []
        for day in schedArrayTemp:
            current = []
            counter = 0
            while counter < len(day):
                myString = day[counter]
                if myString[0].isnumeric():
                    current.append([day[counter], day[counter+1], day[counter+2], day[counter+3]])
                    counter += 4
                else:
                    current.append(myString)
                    counter += 1
            schedArray.append(current)

        ########################### DISPlAYING THE RESULT ###########################
        temp_list= []
        new = []
        newSched = []
        for i in schedArray:
            #print(i)
            for j in i:
                temp_list.append(str(j).replace("[", "").replace("]", "").replace("'", "").replace(",", ""))
                #print(str(j).replace("[", "").replace("]", "").replace("'", "").replace(",", ""))
            new.append(temp_list)
            temp_list = []
        i=0
        if(new[i]).count("Saturday") == 0:
            newSched.append(["Saturday", "Free", "Free", "Free", "Free", "Free"])
        else:
            newSched.append(new[i])
            i+=1
        if(new[i]).count("Sunday") == 0:
            newSched.append(["Sunday", "Free", "Free", "Free", "Free", "Free"])
        else:
            newSched.append(new[i])
            i+=1
        if(new[i]).count("Monday") == 0:
            newSched.append(["Monday", "Free", "Free", "Free", "Free", "Free"])
        else:
            newSched.append(new[i])
            i+=1
        if(new[i]).count("Tuesday") == 0:   
            newSched.append(["Tuesday", "Free", "Free", "Free", "Free", "Free"])
        else:
            newSched.append(new[i])
            i+=1
        if(new[i]).count("Wednesday") == 0:
            newSched.append(["Wednesday", "Free", "Free", "Free", "Free", "Free"])
        else:
            newSched.append(new[i])
            i+=1
        try:
            if(new[i]).count("Thursday") == 0:
                newSched.append(["Thursday", "Free", "Free", "Free", "Free", "Free"])
            else:
                newSched.append(new[i])
                i+=1
        except:
            newSched.append(["Thursday", "Free", "Free", "Free", "Free", "Free"])
        print(newSched)
 
    try:

        for i in range(1, 8):
            for j in range(1, 7):
                # Skip the first cell
                if i == 1 and j == 1:
                    continue
                # Create the column headers in the first row
                elif i == 1:
                    label = tk.Label(root, text=column_headers[j-2], padx=10, pady=10, relief=tk.RIDGE)
                    label.grid(row=i+5, column=j, sticky=tk.NSEW)
                # Create the row headers in the first column
                elif j == 1:
                    label = tk.Label(root, text=row_headers[i-2], padx=10, pady=10, relief=tk.RIDGE)
                    label.grid(row=i+5, column=j, sticky=tk.NSEW)
                # Create the empty cells
                else:
                    label = tk.Label(root, text=newSched[i-2][j-2], padx=10, pady=10, relief=tk.RIDGE)
                    label.grid(row=i+5, column=j, sticky=tk.NSEW)
                    
    except:
        
        messagebox.showerror("Error", "Something went wrong. Please check your credentials and try again.")
    
submit = tk.Button(root, text="Get schedule", command=get_schedule)
submit.grid(row=3, column=1)
        
root.mainloop()