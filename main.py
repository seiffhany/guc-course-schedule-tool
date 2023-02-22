import re

import requests
from requests_ntlm import HttpNtlmAuth
from bs4 import BeautifulSoup

username = "your_username"
password = "your_password"
###################### COURSES #####################
resp = requests.get('https://cms.guc.edu.eg', auth=HttpNtlmAuth(username, password))
courseSoup = BeautifulSoup(resp.text, 'html.parser')

myCourses = courseSoup.find_all(id='ContentPlaceHolderright_ContentPlaceHoldercontent_GridViewdiss')

########################### DISPLAYING THE COURSES ###########################
# for i in myCourses[0].select('td:first-child'):
#     print(i.text)


###################### SCHEDULES #####################
schedResp = requests.get('https://student.guc.edu.eg/Web/Student/Schedule/GroupSchedule.aspx',
                         auth=HttpNtlmAuth(username, password))
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
for i in schedArray:
    print(i)


