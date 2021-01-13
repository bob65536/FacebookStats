# Make stats for Facebook
# f: the file (will be quickly closed anyway)
# content: variable storing f, line by line
# line: the variable content, but on one line
# j: JSON turned into dictionnary. Ready to be used!

# -*- coding: utf-8 -*-
from __future__ import division # For old dudes still with Python 2.7
import matplotlib
matplotlib.use('Agg') # When you use Python Shell 
try:
    import simplejson as json
except:
    print("/!\ For better results, you should install simplejson")
    import json
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as pltc
import time
import os
import re
import sys

#from random import sample
all_colors = [k for k,v in pltc.cnames.items()]
all_colors2=["steelblue","indianred","darkolivegreen","olive","darkseagreen","pink","tomato","orangered","greenyellow","burlywood","mediumspringgreen","chartreuse","dimgray","orange","darkslategray","brown","dodgerblue","peru","lawngreen","chocolate","springgreen","crimson","forestgreen","darkgrey","cyan","darkviolet","darkgray","mediumorchid","darkgreen","darkturquoise","red","deeppink","darkmagenta","gold","hotpink","firebrick","steelblue","indianred","mistyrose","darkolivegreen","olive","darkseagreen","pink","tomato","orangered","darkslategrey","greenyellow","burlywood","seashell","mediumspringgreen","chartreuse","dimgray","black","springgreen","orange","darkslategray","brown","dodgerblue","peru","lawngreen","chocolate","crimson","forestgreen","darkgrey","cyan","mediumorchid","darkviolet","darkgray","darkgreen","darkturquoise","red","deeppink","darkmagenta","gold","hotpink","firebrick"]
times = [time.time()] # For debug: how long each graph takes to load?

####################
# User-editable variables - What you can edit, without looking for ages in the code
nbBins = 96                             # Subdiv per day Useful for Fig3. MUST be a multiple of 24 and dividable by 1440
                                        # Choose between: 24, 48, 72, 96, 120, 144, 240, 288, 360, 480, 720, 1440.
startDate = dt.datetime(2000,1,1)       # When you want to start the stats. Good idea to take the last three months for example.
endDate = dt.datetime(2099,1,1)         # Format: dt.datetime(yyyy,m,d) - NO leading zeroes even if it is fancier with!
                                        # Not yet implemented
timeZoneStartTime = 1                   # 1 for UTC+01:00 (Winter time in France) (add 1 if DST)
timeZonePerMonth = \
    [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1]# Timezones (included DST) for each month
matplotlib.rcParams['font.size'] = 16   #
widthImg = 800                          # Width of the images on the HTML report. Soon, it will be set automatically ;)  
encoding = 'latin1'                     # If there are accents (for French people), this encoding works fine. 
decoding = 'utf-8'                      # To interpret accent words from json, use this: u'\xc3\x89'.encode('latin1').decode('utf-8')
pathRes = "resAnalysis"                 # In the end, we will have ~25 files: get them in a folder
customTitle=u"Stats of xxx"             # The title you want (add xxx for inserting name of the conversation)
endConvDelay = 86400                    # Delay before considering a conversation closed (in sec). 86400 s = 1 day
# Below this line: do NOT edit unless you know what you do!
####################
startTimeStamp = (startDate - dt.datetime(1970,1,1)).total_seconds()-timeZoneStartTime*3600
endTimeStamp = (endDate - dt.datetime(1970,1,1)).total_seconds()-timeZoneStartTime*3600
# Opening and using the JSON file(s)
#f = open("message.json",'r')
#content = f.readlines() # Content of the whole file (but w/ newlines)
#line = "".encode(encoding)
#f.close()
#for i in range(len(content)):
#  line += content[i]
#j = json.loads(line)    # Now, we have a great thing that can be used :)
#del content
#del line

print("Opening the message.json file")  
if sys.version_info[0] == 2:
    import io
    with io.open('message.json', 'r') as f:
        j = json.load(f)
else:
    with open('message.json', 'r', encoding=encoding) as f:
        j = json.load(f)

#%%
    
###### Functions ######
def addList(L1, L2):
    # Sums values of each member of a list
    if (len(L1)==len(L2)):
        N = len(L1)
        res = [0]*N
        for i in range(N):
            res[i] = L1[i]+L2[i]
        return res
    else:
        print("ERROR: arguments do not have same length!")
    
def prettyTxt(msg):
    # Correct the unicode text to interpret accents properly
    return msg.encode(encoding).decode(decoding)

def prettyAllTxt():
    # Returns nothing. Correct the encoding of the variables of interest
    global name
    global nameFirst
    global nameLast
    global listPeople
    try:
        global reacActor
        global reacSender
        reacActor = prettyTxt(reacActor)
        reacSender = prettyTxt(reacSender)
    except NameError:
        print("No reactions here.")
    name = prettyTxt(name)
    nameFirst = prettyTxt(nameFirst)
    nameLast = prettyTxt(nameLast)
    listPeople = list(listPeople)
    for i in range(len(listPeople)):
        listPeople[i] = prettyTxt(listPeople[i])
  
def makeSubplot(N):
    # How to do subplots like a boss (nb, position, etc) ?
    # Check it here!
    if (N<=30):
        if N==1:
            return (1,1)
        if N==2:
            return (1,2)
        if N==3:
            return (1,3)
        if N==4:
            return (2,2)
        if N==5:
            return (2,3)
        if N==6:
            return (2,3)
        if((N>= 7) and (N<=9)):
            return (3,3)
        if((N>= 10) and (N<=12)):
            return (3,4)
        if((N>= 13) and (N<=16)):
            return (4,4)
        if((N>= 17) and (N<=20)):
            return (4,5)
        if((N>= 21) and (N<=25)):
            return (5,5)
        if((N>= 26) and (N<=30)):
            return (5,6)

def getListPeople(data, numberPeople):
    ppl=[]
    for i in range(numberPeople):
        # print ppl
        ppl += [data['participants'][i]['name']]
    return ppl
 
def getTotalLenMsg(data, nbMsg):
    # Send the output of j['messages']
    l = 0
    for i in range(nbMsg):
        try:
            l += len(data[i]['content'])
        except:
            pass
    return l

def getLenMsg(data):
    # Ex: simply type m for the whole msg
    l = 0
    try:
        l = len(data['content'])
    except:
        # print("WARN: one blank message!")
        True
    return l

def decimize(var, nb):
    # Gives to var nb figures after the decimal point. (There is already a function for that, in fact...)
    #return 1.0*int(var*10**nb)/10**nb
    return round(var, nb)
 
def decimizeStr(var, nb):
    # Gives to var nb figures after the decimal point.
    return str(round(var, nb))

def decimizeList(L, nb):
    # Gives to all vars in L nb figures after the decimal point.
    return [decimize(var, nb) for var in L]

def pareto(nbMsgPerSender):
    # Returns three values: [0]the %age of biggest users, doing [1](=100-[0])%age of msg sent ([2]: true %age)
    N = len(nbMsgPerSender)
    S = sum(nbMsgPerSender)
    n = 0
    s = 0
    while(1.0*s/S+1.0*n/N < 1):
        s += nbMsgPerSender[n]
        n += 1
    #print ("Pareto: "+decimizeStr(100.*n/N,1)+"% of users posted more than "+decimizeStr(100.*(1-n/N)+.1,1)+"% of messages ("+decimizeStr(100.*s/S,1)+"%).")
    return (decimizeStr(100.*n/N,2), decimizeStr(100.*(1-n/N)+.1,1), decimizeStr(100.*s/S,1))

def daterange(date1, date2):
    x = []
    for n in range(int ((date2 - date1).days)+1):
        x.append(date1 + dt.timedelta(n))
    return x

def findQuarters(msgPerDayX, msgPerDayY):
    # Gives the dates where you reached 1/4, 1/2 and 3/4 of messages
    S = sum(msgPerDayY)
    N = len(msgPerDayY)
    s = 0
    Q1, Q2, Q3 = 0,0,0
    for i in range(N):
        s += msgPerDayY[i]
        if(1.0*s/S <= .25):
            Q1+= 1
        if(1.0*s/S <= .5):
            Q2+= 1
        if(1.0*s/S <= .75):
            Q3+= 1
    return (msgPerDayX[Q1], msgPerDayX[Q2], msgPerDayX[Q3])

def hourPost(hourMsg, nbBins):
    # When are messages posted?
    # hourMsg are dates under the form datetime.datetime(2001,2,23,3,46,56,10101)
    hr = [0]*24
    hrDetailed = [0]*nbBins # one segment every 15 min
    for h in hourMsg:
        hr[h.hour] += 1 # Increase the hth value of counter (msg between h:00 and h:59)
        if (nbBins!=24):
            hrDetailed[int(nbBins/24)*h.hour+h.minute//int(60*24/nbBins)]+= 1
    if(nbBins != 24):
        return hr, hrDetailed
    else:
        return hr, hr
 
def nbDailyMsg(hourMsgD):
    # Get distribution msg per day
    firstMsg = hourMsgD[-1]
    lastMsg = hourMsgD[0]
    xAxis = daterange(firstMsg, lastMsg)
    nbDays = len(xAxis)
    yAxis = [0]*nbDays # The array gives the nb of occurences
    for i in range(nbDays):
        yAxis[i] = hourMsgD.count(xAxis[i])
    return xAxis, yAxis

def nbWeekDayMsg(day, nb):
    # day represents a array with consecutive dates (from the creation to today), repeated only once
    # nb represents the number of msg per day (from 0 to a lot)
    # res represents the nb of msg on Monday, Tuesay, etc. 
    res = [0, 0, 0, 0, 0, 0, 0]
    for i in range(len(day)):
        wd = day[i].weekday() # weekday gives a value between 0 (Monday) and 6 (Sunday)
        res[wd] += nb[i]
    return res

def nbMonthlyMsg(hourMsgD):
    # Get distribution msg per month
    firstMsg = dt.date(hourMsgD[-1].year, hourMsgD[-1].month, 1) # Put to the 1st day
    lastMsg = hourMsgD[0]
    xAxis = daterange(firstMsg, lastMsg) # Same x axis than for daily msg. Width of bins will change.
    nbDays = len(xAxis)
    yAxis = [0]*nbDays # The nb of occurences
    for i in range(nbDays):
        # Put every value in the 1st of month
        firstOfMonthIndex = xAxis.index(dt.date(xAxis[i].year, xAxis[i].month, 1)) # Pos of the 1st of xxx
        yAxis[firstOfMonthIndex] = hourMsgD.count(xAxis[i])
    return xAxis, yAxis

def categorizeMsg(m):
        # Goal: tell if the sent message is a photo, or a video or something else
        # So far, categories are: (0) "Photos", (1) "Stickers", (2) "GIF", (3) "Videos", (4) "Audio Msgs", (5)"Files", 
        #                         (6) "Links", (7) "Calls", (8) "Blank/Removed Msgs", (9) Waving, (10) Waving back, 
        #                         (11) App used, (12) Adding someone, (13) Leave, (14) Kickig someone, (15) Create a poll
        #                         (16) Participate in a poll, (17) Change group photo, (18) Change nicknames, (19) Change group name 
        #                         (20) Change chat colors, (21) Change like button, (22) Group admin, (23) Regular messages (what's left)
        # cat is between 0 and 8+ and count is the number of items
        try:
            msg = m['content'].lower()
        except KeyError:
            msg = ""
        if ("photos" in m.keys()):
            cat = 0
            count = len(m['photos'])
        elif ("sticker" in m.keys()):
            cat = 1
            count = 1 # There can be only one (per msg)
        elif ("gifs" in m.keys()):
            cat = 2
            count = len(m['gifs'])
        elif ("videos" in m.keys()):
            cat = 3
            count = len(m['videos'])
        elif ('audio_files' in m.keys()):
            cat = 4
            count = len(m['audio_files'])
        elif ('files' in m.keys()):
            cat = 5
            count = len(m['files'])
        elif (("https://" in msg) or ("http://" in msg)):
            cat = 6 # I see (a) new link(s)
            count = msg.count("https://") + msg.count("http://")
        elif (m['type'] == "Call" or \
                    (" a call." in msg and m['type'] == 'Generic')): # Beware, works better if FB in English. TODO: adapt to other languages!
            cat = 7 # For group calls (type as Generic... WTF)
            count = 1
        elif (m['type'] == 'Generic' and ('content' not in m.keys())):
            cat = 8 # Blank or removed message
            count = 1
        elif (m['type'] == 'Share' and (("is waving at" in msg) or ("you waved at" in msg))):
            cat = 9
            count = 1
        elif (m['type'] == 'Share' and ("waved at each other" in msg)):
            cat = 10
            count = 1
        elif (m['type'] == 'Share' and ('share' not in m.keys())):
            cat = 11
            count = 1
        elif (m['type'] == 'Subscribe'):
            cat = 12
            try:
                count = len(m['users'])
            except: # The user quit Facebook therefore users attribute is not present
                count = 1
        elif ((m['type'] == 'Unsubscribe') and ("left the group" in msg)):
            cat = 13 # Left on his/her own
            try:
                count = len(m['users'])
            except: # The user quit Facebook therefore users attribute is not present
                count = 1
        elif ((m['type'] == 'Unsubscribe') and (" removed " in msg)):
            cat = 14 # Kick
            try:
                count = len(m['users'])
            except: # The user quit Facebook therefore users attribute is not present
                count = 1
        elif ((m['type'] == 'Generic') and ("created a poll:" in msg)):
            cat = 15
            count = 1
        elif ((m['type'] == 'Generic') and ("in the poll:" in msg)):
            cat = 16
            count = 1
        elif ((m['type'] == 'Generic') and ("changed the group photo" in msg)):
            cat = 17
            count = 1
        elif ((m['type'] == 'Generic') and (
                        ("set the nickname for" in msg) or ("own nickname to" in msg) or ("set your nickname to" in msg))):
            cat = 18
            count = 1
        elif ((m['type'] == 'Generic') and ("named the group" in msg)):
            cat = 19
            count = 1
        elif ((m['type'] == 'Generic') and ("changed the chat colors" in msg)):
            cat = 20
            count = 1
        elif ((m['type'] == 'Generic') and ("set the emoji to" in msg)):
            cat = 21
            count = 1
        elif ((m['type'] == 'Generic') and ("as a group admin" in msg)):
            cat = 22
            count = 1
        elif (m['type'] == 'Plan'): # (!) I forgot that thing... 
            cat = 23
            count = 1
        else: # For everything else (messages only... theoretically)
            cat = 24
            count = 1      
        return cat, count

def printToFile(text, outFile):
    # When you want to print AND to save text, this function is your savior!
    # Note: you will need to open the file before calling this function and don't forget to close it!!!
    print(text.encode(encoding))
    outFile.write(text.encode(encoding)+'\n'.encode(encoding))
  
def toDaysArray(ArrayDt):
    return [dt.days+dt.seconds/86400. for dt in ArrayDt]

def toDays(dt):
    return dt.days+dt.seconds/86400.

def totalSecondsToStr(seconds):
    # Convert a number of seconds (e.g. 100000) into a nice representation (1 day, ...)
    res = ""
    if (seconds < 0):
        res += "(Negative time) "
    sec = abs(int(seconds))
    yr = sec // 31536000
    sec = sec % 31536000
    if (yr > 0):
        res = res + str(yr) + " year"
        if (yr > 1):
            res += 's'
        res += ", "
    day = sec // 86400
    sec = sec % 86400
    if (day > 0):
        res = res + str(day) + " day"
        if (day > 1):
            res += 's'
        res += ", "
    hr = sec // 3600
    sec = sec % 3600
    if (hr > 0):
        res = res + str(hr) + " hour"
        if (hr > 1):
            res += 's'
        res += ", "
    mn = sec // 60
    sec = sec % 60
    if (mn > 0):
        res = res + str(mn) + " min, "
    if (sec > 0):
        res = res + str(sec) + " sec"
    return res

def totalSecondsToStrShort(seconds):
    # Convert a number of seconds (e.g. 100000) into a nice representation (2d 14:54:08)
    res = ""
    if (seconds < 0):
        res += "-"
    sec = abs(int(seconds))
    yr = sec // 31536000
    sec = sec % 31536000
    if (yr > 0):
        res = res + str(yr) + "y "
    day = sec // 86400
    sec = sec % 86400
    if (day > 0):
        res = res + str(day) + "d "
    hr = sec // 3600
    sec = sec % 3600
    if (hr > 0):
        res = res + str(hr) + ":"
    # Example: 5y 55d 5:12:03 or 15:43
    mn = sec // 60
    sec = sec % 60
    res = res + str(mn).zfill(2) + ":" + str(sec).zfill(2) 
    return res

def divideList(L, x):
    # Self-explanatory: divise every term of L by x. 
    # For multiplying, divide by 1/x
    return [L[i]*1.0/x for i in range(len(L))]

def makeAutopct(values):
    # Thanks to https://stackoverflow.com/questions/6170246/how-do-i-use-matplotlib-autopct
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        if (pct>1.5):
            return '{p:.1f}%  ({v:d})'.format(p=pct,v=val)
        elif (pct>1):
            return '({v:d})'.format(p=pct,v=val)
        else:
            return ""
    return my_autopct

def avgTTR(TTR):
    # TTR is a list of lists with times in seconds (for each participant).
    # res is a list af average TTR for each guy (in seconds)
    # Note: for zero values, a value of 0s will be given. Hope this won't be displayed...
    res = []
    for oneTTR in TTR:
        s=0  # Total of time (<24h or endConvDelay) 
        nb=0 # Nb of message processed
        for val in oneTTR:
            if val<endConvDelay:
                s+=val
                nb+=1
        try:
            res.append(s*1.0/nb)  
        except ZeroDivisionError:
            res.append(0)
    return res # Form of: replies within 5s, 30s, ...

def getRowTabl(tabl, row):
    # Returns a list, with the row-th values for each line of the tableau (tabl).
    res = []
    for L in tabl:
        res.append(L[row])
    return res

def divideRowTabl(tabl, row):
    # Like getRowTabl, but divides each value of res by the sum of the row. 
    # Summing res should give you 1 (except when sum=0)
    L = getRowTabl(tabl, row) # Intermediate result.
    sumTabl = sum(L)
    if(sumTabl == 0):
        return L # We let the valuas as is. No DIV/0.
    else:
        res = []
        for i in L:
            res.append(decimize(i*1.0/sumTabl, 4))
        return res

def percentageRowTabl(tabl, row):
    # Like divideRowTabl, but gives a sum of 100 (percentages).
    L = getRowTabl(tabl, row) # Intermediate result.
    sumTabl = sum(L)
    if(sumTabl == 0):
        return L # We let the valuas as is. No DIV/0.
    else:
        res = []
        for i in L:
            res.append(decimize(100.0*i/sumTabl, 4))
        return res

def addToCsv(txt):
    if sys.version_info[0] == 2: # If you have Python 2
        try:
            tmp = txt.encode(encoding)
        except AttributeError:
            tmp = str(txt)  
        separator = ';'.encode(encoding)    
        return tmp + separator
    else: 
        separator = u';'    
        return str(txt) + separator
  
def sendToCsv():
    csvName = "stats.csv"
    res = ""
    # To make global analysis: we will save interesting values to a CSV. 
    # If it already exists, apppend data in the next line.
  
    # header = ("Type;Name;Start_Date;Start_Who;End_Date;End_Who;NbPart_curr;NbPart_total;" + "")
    res += addToCsv(str(typ))         # Type (Regular or RegularGroup)  
    res += addToCsv(name)             # Name of the conv
    res += addToCsv(firstMsg)         # Date of the 1st msg
    res += addToCsv(nameFirst)        # Who sent the 1st msg
    res += addToCsv(lastMsg)          # Date of the last msg
    res += addToCsv(nameLast)         # Who sent the last msg
    res += addToCsv(N)                # NbPart_curr
    res += addToCsv(N2)               # NbPart_total
    # TODO
    if (sys.version_info[0] == 2):
        with open(pathRes+'/'+csvName, 'ab') as csvFile: # a for append, b for bytes mode
            csvFile.write('\n')
            csvFile.write(res)  
    else: # With Python 3, you must use convert text to bytes to add, hence the .encode()
        with open(pathRes+'/'+csvName, 'ab') as csvFile: # a for append, b for bytes mode
            csvFile.write('\n'.encode())
            csvFile.write(res.encode())

def removeFile(fileName):
    with open(fileName,'w') as f: 
        f.write("This file will be removed") # Erase the figure, if it existed before
    if os.path.isfile(fileName):
        os.remove(fileName)

def resizePicsForHtml():
    listFiles=["01-participants.png","02a-hourUse.png","02b-hourlyRadarGraph.png","02c-hourlyRadarGraphPerUser.png",
             "03a-preciseHourUse.png","03b-preciseRadarGraph.png","04-emptyMoments.png",
             "05a-dateMsgPerDay.png","05b-dateMsgPerMonth.png","05c-dateMsgPerWeekDay.png","06a-reacSent.png",
             "06b-reacReceived.png","06c-reacReceivedPerMsg.png","07-lenMsg.png","08-behaviorStats.png",
             "09-lengthOfMsg.png","10-lengthOfSilences.png","11-duCoup.png",
             "12-TTR.png", "13a-lastConv.png", "13b-lastConvDuration.png", "13c-lastConvSilence.png",
             "14a-mediaShared.png", "14b-actionsDone.png"]
    try:
        # If we can create miniatures for a better webpage
        from PIL import Image
        # Resize images and add '_mini' after (TODO)
        sizeImg="_mini.png" # By default: 800 px wide.
        for imgFiles in listFiles:
            try:
                img=Image.open(pathRes+'/'+imgFiles)
                (wid,hei)=img.size
                heightImg = 1.0*widthImg/wid*hei # To keep proportions
                img=img.resize((int(widthImg), int(heightImg)), Image.ANTIALIAS)
                img.save(pathRes+'/'+imgFiles+sizeImg, optimize=True, quality=85)
            except IOError:
                print(str(imgFiles)+": No such file...")
    except ImportError:
        # If PIL is not installed, I will not use miniatures but the full img (For tests only!!!)
        print("PIL/Pillow not found. Install it by running 'pip install Pillow' or 'pip3 install Pillow'.")
        sizeImg=""

def saveReportToHtml():
    # Create a HTML file with all the information
    templateLoader = jinja.FileSystemLoader(searchpath="./")
    templateEnv = jinja.Environment(loader=templateLoader)
    # Insertion of images (miniature or full)
    try:
        # If we can create miniatures for a better webpage
        resizePicsForHtml()
        sizeImg="_mini.png" # By default: 800 px wide.
    except:
        # If PIL is not installed, I will not use miniatures but the full img (For tests only!!!)
        print("PIL/Pillow not found. Install it by running 'pip install Pillow' or 'pip3 install Pillow'.")
        sizeImg=""
    if(typ == "RegularGroup"):
        TEMPLATE_FILE = "html/templateGroup.html"
    else:
        TEMPLATE_FILE = "html/templatePrivate.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    # Manage the title of the page
    global customTitle
    if customTitle=="":
        customTitle = str(name) + " | Analysis"
    elif customTitle.find("xxx") != -1:
        varField=customTitle.find("xxx")
        customTitle = customTitle[:varField] + name + customTitle[varField+3:]
    else:
        # No names so no need to do anything :) 
        customTitle=customTitle
    outputText = template.render(customTitle=customTitle, encoding=encoding, sizeImg=sizeImg, widthImg=widthImg, name=name, N=N, Nout=N2-N, 
                               dateCreation= dt.datetime.now().strftime("%Y-%m-%d at %H:%M"), ageConv=ageConv, 
                               firstMsg=firstMsgPretty, lastMsg=lastMsgPretty, nameFirst=nameFirst, nameLast=nameLast, 
                               firstMsgShort=firstMsgShort, lastMsgShort=lastMsgShort, lenMsg=lenMsg,
                               silenceTime=totalSecondsToStr(silenceTime.total_seconds()),
                               nbMsg=nbMsg, avgNbMsg=decimizeStr(1.0*nbMsg/(1.0*N), 2),
                               Q2=Q2, Q1=Q1, Q3=Q3, mostActiveDay=mostActiveDay, mostMsgDay=mostMsgDay, 
                               nbConv=sum(convStartedBySender), endConvDelay=totalSecondsToStrShort(endConvDelay),
                               nbMsgReac=nbMsgReac, percentMsgReac=decimizeStr(100*nbMsgReac/nbMsg,1), nbReacSum=nbReacSum, reacPerMsg=decimizeStr(nbReacSum/nbMsgReac, 2) if nbMsgReac!=0 else "NaN",
                               reac0=reacNb[0], reac1=reacNb[1], reac2=reacNb[2], reac3=reacNb[3], reac4=reacNb[4], reac5=reacNb[5], reac6=reacNb[6], reac7=str(sum(reacNb)-sum(reacNb[:7])),
                               pareto0=paretoRes[0], pareto1=paretoRes[1], pareto2=paretoRes[2], lenMsgConv=decimizeStr(nbMsg/(sum(convStartedBySender)+1), 1), 
                               totalTimeConv=totalSecondsToStr(convoTimeSpent.total_seconds()), totalTimeConvShort=totalSecondsToStrShort(convoTimeSpent.total_seconds()), 
                               nbHeart=sum(nbHeart), nbDuCoup=sum(nbDuCoup), avgLengthOverall=avgLengthOverall, nbBarsFig13=nbBarsFig13, ratioConvTotal=ratioConvTotal,
                               nbPics=typeMessages[6], nbStickers=typeMessages[7], nbGIFS=typeMessages[8], nbVids=typeMessages[9], nbAudioMsg=typeMessages[10], 
                               nbLinks=typeMessages[12], nbDocs=typeMessages[11], nbCalls=typeMessages[13], nbChgNick=typeMessages[24], nbAdded=typeMessages[18], 
                               nbLeft=typeMessages[19], nbKicked=typeMessages[20], nbWaves=typeMessages[15]+typeMessages[16], nbBlank=typeMessages[14], nbMsgRegular=typeMessages[-1],
                               nbMedia=nbMedia, nbActions=nbActions, genTime=decimizeStr(times[-1]-times[0], 3))
    html_file = open(pathRes+'/stats.html', 'wb')
    html_file.write(outputText.encode(encoding))
    html_file.close()

#%%

###### Using the functions for stats
typ = j['thread_type']
name = j['title']
N = len(j['participants'])
listPeople = getListPeople(j, N)
idPeople = list(range(N)) # Assign a number to each user. Will make searches easier
reacSentPerActor = [[0]*8 for x in range(N)] # Position k for listPeople[k] - reactions SENT
reacReceivedPerSender = [[0]*8 for x in range(N)] # Position k for listPeople[k] - reactions RECEIVED
hrPerSender = [[0]*24 for x in range(N)] # Position k for listPeople[k] - hour msg # Hourly distribution per user
nbMsgPerSender = [0]*N # Messages sent by Sender
lenMsgPerSender = [0]*N # Length of msg written by Sender
convStartedBySender = [0]*N # Who starts conversations? (Used so far if N==2)
ignoredMessagesPerUser = [0]*N # Who ignores their friend? (Used so far if N==2)
labelTypeMessages = ["Generic", "Share", "Subscribe", "Unsubscribe", "Call", "Plan",
                     "Photos", "Stickers", "GIF", "Videos", "Audio Msgs",  
                     "Files", "Links", "Calls", "Blank/Removed Msgs", "Waving",  
                     "Waving Back", "App used", "Adding someone", "Leave", "Kicking someone", 
                     "Create poll", "Participate poll", "Change group photo", "Change nicknames", "Change group name",
                     "Change chat colors", "Change emoji", "Group admin", "Plan", "Misc"] 
                     # First 5: official types (on JSON). Next: I created them (cf categorizeMsg()). 
                     # Important! If you change the function, update this list! 
offsetLabelTypeMessages = 6 # Number of types
typeMessagesPerSender = [[0]*len(labelTypeMessages) for x in range(N)] # nb of messages per sender, depending on type (so far: 5 types) + sorting with categorize() (so far: 24 categories)
typeMessages = [0]*len(labelTypeMessages) # Sum of typeMessagesPerSender (30)
nbHeart = [0]*N
nbJe = [0]*N
nbTu = [0]*N
nbDuCoup = [0]*N
timeToReply = [[] for x in range(N)] # How long does X reply to the previous msg? // akaa TTR (too long to write)
hourMsg = []
hourMsgD = []
hourMsgMo = []
nbMsgTotal = len(j['messages'])
lenMsgTotal = getTotalLenMsg(j['messages'], nbMsgTotal)
nbMsg = 0
lenMsg = 0
silenceTime = dt.timedelta(0,0) # In (days,seconds)
silenceArray = [[],[]] # Length of silences. Can be used to foresee a future interaction
convoTimeSpent = dt.timedelta(0,0) # (days, seconds)
# Reactions
nbReacSum = 0
nbMsgReac = 0
reacMean =["Love","Haha","Wow!","Sad ","Grrr"," +1 "," -1 ","Misc"]
reacHex  =["98 8d","98 86","98 ae","98 a2","98 a0","91 8d","91 8e","00 00"]
reacNb = [0]*8
heartHex = "e2 9d a4" # This variable represents a heart

# Stats of participation / Analysis per message
for m in j['messages']:
    # Date filter. Nothing goes here.
    if (m['timestamp_ms']/1000. >= startTimeStamp):
        # Count number of messages
        nbMsg += 1
        typeMessages[labelTypeMessages.index(m['type'])] += 1 # Append 1 to the right type of message
        category,nbr = categorizeMsg(m)
        typeMessages[category+offsetLabelTypeMessages] += nbr # Sum of typeMessagesPerSender for all users
        if(category+offsetLabelTypeMessages==len(labelTypeMessages)-1): # Regular Message (last category)
            lenMsg += getLenMsg(m) # Don't add characters if not regular msg!
        try:
            idUser = listPeople.index(m['sender_name']) # idUser is between 0 and N-1 and identifies an user
            nbMsgPerSender[idUser] += 1
            typeMessagesPerSender[idUser][labelTypeMessages.index(m['type'])] += 1
            typeMessagesPerSender[idUser][category+offsetLabelTypeMessages] += nbr
            hourCurrentMsg = dt.datetime.fromtimestamp(m['timestamp_ms']/1000).hour # Refers to the hour of the msg sent
            hrPerSender[idUser][hourCurrentMsg] += 1
            if(category+offsetLabelTypeMessages==len(labelTypeMessages)-1): # Regular Message (last category)
                lenMsgPerSender[idUser] += getLenMsg(m)
        except KeyError:
            # The user does not exist anymore (removed account, ...) 
            # and Facebook devs find nice to remove the whole attribute. ...
            if "UNKNOWN" in listPeople:
                # We already analysed a message from a deleted account
                unk = listPeople.index("UNKNOWN")
                nbMsgPerSender[unk] += 1
                idUser = unk
            else:
                # Oh, just discovered a removed account. Let's count it!
                listPeople.append(u"UNKNOWN")
                idPeople.append(len(idPeople)) # Add a number to the list
                nbMsgPerSender.append(1)
                typeMessagesPerSender.append([0]*len(labelTypeMessages))
                reacReceivedPerSender.append([0]*8)
                reacSentPerActor.append([0]*8)
                hrPerSender.append([0]*24)
                if(category+offsetLabelTypeMessages==len(labelTypeMessages)-1):
                    lenMsgPerSender.append(getLenMsg(m))
                else:
                    lenMsgPerSender.append(0)
                convStartedBySender.append(0)
                ignoredMessagesPerUser.append(0)
                nbHeart.append(0)
                nbDuCoup.append(0)
                nbJe.append(0)
                nbTu.append(0)
                timeToReply.append([])
                idUser = listPeople.index("UNKNOWN") # Now, the user is added :) 
                typeMessagesPerSender[idUser][labelTypeMessages.index(m['type'])] += 1
                typeMessagesPerSender[idUser][category+offsetLabelTypeMessages] += nbr
                hourCurrentMsg = dt.datetime.fromtimestamp(m['timestamp_ms']/1000).hour # Refers to the hour of the msg sent
                hrPerSender[idUser][hourCurrentMsg] += 1
        except ValueError:
            # If the user does not belong to the conv anymore
            # print("INFO: "+m['sender_name']+" is not in the conv anymore. Added to the list.")
            listPeople.append(m['sender_name'])
            idPeople.append(len(idPeople)) # Add a number to the list
            nbMsgPerSender.append(1)
            typeMessagesPerSender.append([0]*len(labelTypeMessages))
            reacReceivedPerSender.append([0]*8)
            reacSentPerActor.append([0]*8)
            hrPerSender.append([0]*24)
            if(category+offsetLabelTypeMessages==len(labelTypeMessages)-1):
                lenMsgPerSender.append(getLenMsg(m))
            else:
                lenMsgPerSender.append(0)
            convStartedBySender.append(0)
            ignoredMessagesPerUser.append(0)
            nbHeart.append(0)
            nbDuCoup.append(0)
            nbJe.append(0)
            nbTu.append(0)
            timeToReply.append([])
            idUser = listPeople.index(m['sender_name']) # Now, the user is added :) 
            typeMessagesPerSender[idUser][labelTypeMessages.index(m['type'])] += 1
            typeMessagesPerSender[idUser][category+offsetLabelTypeMessages] += nbr
            hourCurrentMsg = dt.datetime.fromtimestamp(m['timestamp_ms']/1000).hour # Refers to the hour of the msg sent
            hrPerSender[idUser][hourCurrentMsg] += 1
        # Classic procedure for each message (retrieving date of the msg, the hour, etc)
        hourMsg.append(dt.datetime.fromtimestamp(m['timestamp_ms']/1000))
        d=dt.datetime.fromtimestamp(m['timestamp_ms']/1000).date() # date in the form of datetime.date(2018,12,25)
        hourMsgD.append(d)
        hourMsgMo.append(dt.date(d.year, d.month, 1))  # We create a distribution depending on the month (day of the month=1)
    
        # Getting TTR
        try:
            currentUser = m['sender_name']
            currentTS = m['timestamp_ms']/1000.
        except KeyError:
            True # No sender name attribute. Just ignore the message.
        try:
            if currentUser != previousUser:
                # Someone else talked
                timeToReply[previousId] += [abs(currentTS-previousTS)]
        except NameError:
            # First message. previousUser not defined yet
            print("First msg analyzed!")
        # Count nb of certain words.
        if m['type'] == "Generic":
            try:
                blabla = m['photos'] # For filtering message analysis if someone sends a picture
            except KeyError:
                occ = 0
                for keyword in ["je", "moi", "j'", "m'", "me"]:
                    try: 
                        occ += (keyword in m['content'].lower())
                    except KeyError:
                        True
                nbJe[idUser] += min(1, occ)
                occ = 0
                for keyword in ["tu", "toi", "t'", "te"]:
                    try: 
                        occ += (keyword in m['content'].lower())
                    except KeyError:
                        True
                nbTu[idUser] += min(1, occ)
                try: 
                    nbDuCoup[idUser] += ("du coup" in m['content'].lower())
                except KeyError:
                        True
            
                try: 
                    msgHex = (" ".join("{:02x}".format(ord(c)) for c in m['content']))
                    nbHeart[idUser] += (heartHex in msgHex)
                except KeyError:
                        True
            
                occ = 0
                for keyword in ["e2 9d a4","f0 9f 92 9b","f0 9f 92 9a","f0 9f 92 99","f0 9f 92 9c",
                        "f0 9f 92 95","f0 9f 92 93","f0 9f 92 9e","f0 9f 92 97","f0 9f 92 98",
                        "f0 9f 92 96","f0 9f 92 9d","f0 9f 92 9f",
                        "f0 9f 98 8d","f0 9f 98 98","f0 9f 98 97","f0 9f 98 99","f0 9f 98 9a",
                        "f0 9f 98 bb","f0 9f 98 bd","f0 9f 91 84"]:
                    try: 
                        msgHex = (" ".join("{:02x}".format(ord(c)) for c in m['content']))
                        occ += (keyword in msgHex)
                    except KeyError:
                        True
                nbHeart[idUser] += occ # Don't abuse of hearts. Else, this count will explode...
        # End of counting
    
        # Reactions!  
        try:
            reacs = m['reactions']
            nbReacSum = nbReacSum + len(m['reactions'])
            nbMsgReac = nbMsgReac + 1
            for reac in reacs:
                ch = reac['reaction'][2:]
                reacMsgHex = (" ".join("{:02x}".format(ord(c)) for c in ch)) # Convert weird chars into (0x)98 for example.
                reacActor = reac['actor'] # Get actor of the reaction
                try:
                    reacActorIndex = listPeople.index(reacActor)
                except ValueError:
                    # Someone reacted but never commented (...)
                    # Add the user to the list of users (listPeople)
                    listPeople.append(reacActor)
                    idPeople.append(len(idPeople)) # Add a number to the list
                    nbMsgPerSender.append(0)
                    typeMessagesPerSender.append([0]*len(labelTypeMessages))
                    reacReceivedPerSender.append([0]*8)
                    reacSentPerActor.append([0]*8)
                    hrPerSender.append([0]*24)
                    lenMsgPerSender.append(0)
                    convStartedBySender.append(0)
                    ignoredMessagesPerUser.append(0)
                    nbHeart.append(0)
                    nbDuCoup.append(0)
                    nbJe.append(0)
                    nbTu.append(0)
                    timeToReply.append([])
                    reacActorIndex = listPeople.index(reacActor) # Now, the user is added and this should be okay
                reacSender = m['sender_name'] # Get the sender of the message provoking reac(s)
                reacSenderIndex = listPeople.index(reacSender)
                try:
                    reacNb[reacHex.index(reacMsgHex)] += 1 # Update overall nb of reactions
                    reacSentPerActor[reacActorIndex][reacHex.index(reacMsgHex)] += 1
                    reacReceivedPerSender[reacSenderIndex][reacHex.index(reacMsgHex)] += 1
                except ValueError:
                    reacNb[7] += 1
                    reacSentPerActor[reacActorIndex][7] += 1
                    reacReceivedPerSender[reacSenderIndex][7] += 1  
        except KeyError:
            False # No reactions
        # NOTE: previousUser and previousDate refer to the previous iteration of the loop
        # Indeed, these data are more recent than the next message (reading from the most recent to the oldest msg)
        # Facebook sucks sometimes...
        try:
            previousUser = m['sender_name'] # To get the user from the msg before (for assessing TTR)
        except KeyError:
            True # Ignore this. No sender name.
        previousTS = m['timestamp_ms']/1000.
        previousId = idUser
    # else:
        # Not counted. Out of date bounds.

N2 = len(listPeople)
reacReceived = [sum(reacReceivedPerSender[i]) for i in range(N2)]
reacSent = [sum(reacSentPerActor[i]) for i in range(N2)]
reacPerMsg = [reacReceived[i]/max(nbMsgPerSender[i],0.1) for i in range(N2)] # If no messages, I avoid a ZeroDivisionError exception by artificially adding a message w/ the max function.
                                                                        # If there are no messages, there won't be reac received!
if(len(hourMsgD) == 0):
    print("[FATAL] Date bounds too tight or empty conversation! Change the value of startDate or reset it by choosing year 2000")
    print("The next line will yield a IndexError exception: this is a logic consequence.")

# Who starts first and Fig8
startUser = [] # Who started the conversation
nbMsgConv = [] # Length of the conversation
durationConv = [] # How long dit it last?
indexNbMsg = 0 # When new conv starts, this value is updated
t0 = hourMsg[0] # The most recent message
# silenceArray contains data about silence's length (and when a conversation started)
for i in range(1, nbMsg):
    a,b = hourMsg[i-1], hourMsg[i] # a > b : a is more recent than b ([0]: most recent)
    if (a-b > silenceTime): # Silence time
        silenceTime = a-b # The longest silence ever
    if (a-b > dt.timedelta(0,endConvDelay)): 
        # There is more than 24h between two msgs (or other value defined on the start of the prog)
        idUser = listPeople.index(j['messages'][i-1]['sender_name']) # id of the guy who started the conv.
        convStartedBySender[idUser] += 1
        startUser.append(idUser)
        nbMsgConv.append(i-indexNbMsg)
        durationConv.append(t0-a) # 'a' is when the conversation started
        indexNbMsg = i # Reset the index
        t0 = b # The end date of the new conversation
        silenceArray[0].append(a)       # When
        silenceArray[1].append(a-b)     # How long
        #if ('?' in j['messages'][i]['content']):
            # Now, we had an unanswered question = Ignored :(
            #idUser2 = listPeople.index(j['messages'][i]['sender_name']) # id of the guy poor ignored
            #ignoredMessagesPerUser[idUser2] += 1
        #else:
            #True
    elif ((a-b) < dt.timedelta(0,300)):
        # I suppose you are spending time on this conversation if there is less than 5 min between messages.
        convoTimeSpent += (a-b)

# Average length msg (Fig10)
avgLengthPerSender = []
avgLengthOverall = decimizeStr(lenMsg/nbMsg, 1)
for i in range(N2):
    if (sum(hrPerSender[i]) == 0):
        avgLengthPerSender.append(0)
    else:
        avgLengthPerSender.append(decimize(lenMsgPerSender[i]/sum(hrPerSender[i]), 1))

# First thing, last thing (+by ...)
firstMsgTS = j['messages'][nbMsg-1]['timestamp_ms']/1000. 
firstMsg = dt.datetime.fromtimestamp(firstMsgTS).isoformat()
firstMsgPretty = dt.datetime.fromtimestamp(firstMsgTS).strftime("%Y-%m-%d at %H:%M")
firstMsgShort = str(dt.datetime.fromtimestamp(firstMsgTS).date())
lastMsgTS = j['messages'][0]['timestamp_ms']/1000. # FB logic: the last message is 1st
lastMsg = dt.datetime.fromtimestamp(lastMsgTS).isoformat()
lastMsgPretty = dt.datetime.fromtimestamp(lastMsgTS).strftime("%Y-%m-%d at %H:%M")
lastMsgShort = str(dt.datetime.fromtimestamp(lastMsgTS).date())
ageConv = totalSecondsToStrShort(lastMsgTS-firstMsgTS)
nameFirst = j['messages'][nbMsg-1]['sender_name']
nameLast = j['messages'][0]['sender_name']

# Sort everything
nbMsgPerSender, typeMessagesPerSender, reacPerMsg, listPeople, idPeople, reacSentPerActor, reacSent, reacReceived, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart = zip(*sorted(zip(nbMsgPerSender, typeMessagesPerSender, reacPerMsg, listPeople, idPeople, reacSentPerActor, reacSent, reacReceived, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart), reverse=False))
msgPerDayX, msgPerDayY = nbDailyMsg(hourMsgD)
msgPerMonthX, msgPerMonthY = nbDailyMsg(hourMsgMo)
msgPerWeekDayX = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
msgPerWeekDayY = nbWeekDayMsg(msgPerDayX, msgPerDayY) # Will be filled from msgPerDayX,Y
times.append(time.time())

# Correcting the encoding before displaying everything
prettyAllTxt()

print("Process done in "+str(times[-1]-times[-2])+"+ sec")

if not os.path.isdir(pathRes):
   os.makedirs(pathRes)

times.append(time.time())
# Display everything (or export them - up to you!)
textFile = open(pathRes+'/Stats.txt','wb')
#textFile = 'Stats.txt'
print("####################")
if (typ=="RegularGroup"):
    printToFile("Stats of the conversation ["+name+"]:", textFile)
    #printToFile("> Number of current participants: "+str(N) + ", plus "+str(N2-N)+" former participants.", textFile)
else:
    printToFile("Your interaction with "+name+":", textFile)
# Generic information
Q1, Q2, Q3 = findQuarters(msgPerDayX, msgPerDayY) # Dates when quarters have been reached
mostMsgDay = max(msgPerDayY)
mostActiveDay = msgPerDayX[msgPerDayY.index(mostMsgDay)]
paretoRes = pareto(nbMsgPerSender)
if (typ=="RegularGroup"): 
    # If there is more than two participants
    printToFile("> Among the "+str(nbMsgReac)+" messages with reactions ("+decimizeStr(100*nbMsgReac/nbMsg,1)+"%), participants have reacted "+str(nbReacSum)+" times ("+decimizeStr(nbReacSum/nbMsgReac, 2)+" times per message).", textFile)
    #printToFile("> Pareto: "+paretoRes[0]+"% of users posted more than "+paretoRes[1]+"% of messages ("+paretoRes[2]+"%).", textFile)
else:
    # Private conv
    printToFile("> "+str(nbMsgReac)+" messages led to a reaction ("+decimizeStr(100*nbMsgReac/nbMsg,1)+"%).", textFile)
    #printToFile("> On average, each coversation lasted "+decimizeStr(nbMsg/sum(convStartedBySender), 1)+" messages before dying", textFile)
    if (0 not in convStartedBySender):
        ratio=convStartedBySender[0]/convStartedBySender[1]
        printToFile("> The person who started the most the conversations did it "+decimizeStr(max(ratio, 1./ratio), 2)+" times more than the receiver.", textFile)
    # DEBUG
    if (0 not in nbJe):
        printToFile("> "+listPeople[0]+" talked about himself "+str(nbJe[0])+" times and about his friend(s) "+str(nbTu[0])+" times (r="+decimizeStr(nbTu[0]/nbJe[0],2)+") and said 'Du coup' "+str(nbDuCoup[0])+" times.", textFile)
        printToFile("> "+listPeople[1]+" talked about himself "+str(nbJe[1])+" times and about his friend(s) "+str(nbTu[1])+" times (r="+decimizeStr(nbTu[1]/nbJe[1],2)+") and said 'Du coup' "+str(nbDuCoup[1])+" times.", textFile)
    else:
        # Avoid a ZeroDivisionError: do not do the division by zero...
        printToFile("> "+listPeople[0]+" talked about himself "+str(nbJe[0])+" times and about his friend(s) "+str(nbTu[0])+" times and said 'Du coup' "+str(nbDuCoup[0])+" times.", textFile)
        printToFile("> "+listPeople[1]+" talked about himself "+str(nbJe[1])+" times and about his friend(s) "+str(nbTu[1])+" times and said 'Du coup' "+str(nbDuCoup[1])+" times.", textFile)
    printToFile("> Overall, "+totalSecondsToStr(convoTimeSpent.total_seconds())+" were spent on this conversation (plus passive participation).", textFile)
textFile.close()
times.append(time.time())
print("Process done in "+str(times[-1]-times[-2])+"+ sec")
#%%
### Graphes     ###############################################################
## Cleanup!
for f in os.listdir(pathRes):
    if re.search("png", f):
        os.remove(os.path.join(pathRes, f))
#plt.figure(1)  ###############################################################
print("Plotting Fig. 1: participants.")
matplotlib.rcParams['font.size'] = 18
if(N2>2):
    plt.figure(figsize=(12+N/3., 9+N/4.))
    plt.pie(nbMsgPerSender, labels=listPeople, autopct=makeAutopct(nbMsgPerSender), shadow=False, rotatelabels =True, labeldistance=1.02,  pctdistance=0.8, startangle=90)
    plt.axis('equal')
else:
    # There are two people. Don't ressort to that pie chart!
    colors = ['cornflowerblue', 'orange'] # We will use at most 2 colors anyway!
    offset = [0, nbMsgPerSender[0]]
    plt.figure(figsize=(12, 3))
    plt.grid(axis='x')
    y = nbMsgPerSender
    p = plt.barh("", y, color=colors, left=offset) # Plot material
    for i in range(2):
        plt.text(y[i]/2.+offset[i], 0, str(y[i])+" ("+decimizeStr(y[i]*100./nbMsg,1)+"%)", ha='center', va='center')
    plt.legend([p[i] for i in range(2)], listPeople)
plt.title("Participants of the conversation ("+firstMsgShort+" -> "+lastMsgShort+")\n")
plt.savefig(pathRes+"/01-participants.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(2) ################################################################
# Rule of thumb: for high values (>360), prepare a good computer (720: 2GB of RAM + 60'' CPU time, 1440: 5GB + 90'' for the program alone)
hr=hourPost(hourMsg, nbBins)
print("Plotting Fig. 2: messages per hour.")
matplotlib.rcParams['font.size'] = 12
plt.figure(figsize=(12, 9))
plt.bar(np.arange(24), hr[0], width=1, alpha=.8, align='edge')
for (a,b) in zip(np.arange(24), hr[0]):
    if(max(hr[0])>999):
        plt.text(a+.02, b, str(b), fontsize=15, weight='bold', rotation=90, verticalalignment='top' if b*1.0/max(hr[0])>0.8 else 'bottom')
    else:
        if(b>0):
            plt.text(a+.02, b+.5 if b>10 else 1.05*b, str(b), fontsize=15, weight='bold')
plt.xticks(np.arange(0,24,1))    
plt.grid(axis='x')
plt.title("Hourly repartition of msgs ("+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig(pathRes+"/02a-hourUse.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(2bis) #############################################################
print("Plotting Fig. 2bis: radar graph for active hours.")
# Taken from SO #
fig = plt.figure(figsize=(15,15))
ax = fig.add_subplot(111,polar=True)
H = len(hr[0]) 
theta = np.arange(0, 2*np.pi, 2*np.pi/H) 
ax.set_theta_zero_location('S') # To start with 0 on the bottom, 12 on the top
bars = ax.bar(theta, hr[0], width=2*np.pi/H, align='edge') # Width = 2pi divided by nbr of bins (24)
ax.set_xticks(theta)
ax.set_xticklabels(range(len(theta)), fontsize=15)
for (a,b) in zip(theta, hr[0]):
    plt.text(a+(2*np.pi/24/2.), max(hr[0])*1.1, str(b), fontsize=20, color="red" if b>0 else 'white', weight='bold', ha='center',va='center')
ax.yaxis.grid(True)
plt.title("Hourly repartition of msgs ("+firstMsgShort+" -> "+lastMsgShort+" - radar graph)\nTotal = "+str(sum(hr[0]))+" msg")
plt.savefig(pathRes+"/02b-hourlyRadarGraph.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(2c) ###############################################################
if (N <= 30):
    print("Plotting Fig. 2ter: radar graph for active hours PER user.")
    subX, subY = makeSubplot(N)
    fig = plt.figure(figsize=(8*subY, 8*subX))
    for i in range(N):
        #col = sample(all_colors2, 1)
        col = all_colors2[i]
        ax = fig.add_subplot(subX,subY,i+1,projection='polar')
        H = len(hr[0]) 
        theta = np.arange(0, 2*np.pi, 2*np.pi/H) 
        ax.set_theta_zero_location('S') # To start with 0 on the bottom, 12 on the top
        ax.set_xticks(theta)
        ax.set_xticklabels(range(len(theta)))
        # Plotting for each user
        bar2c = ax.bar(theta, hrPerSender[i], width=2*np.pi/H, align='edge', color=col) # Width = 2pi divided by nbr of bins (24)
        for (a,b) in zip(theta, hrPerSender[i]):
            plt.text(a+(2*np.pi/24/2.), max(hrPerSender[i]), str(b), fontsize=10, color="black" if b>0 else 'white', weight='bold')
        ax.yaxis.grid(True)
        if(lenMsgPerSender[i]>0 and nbMsgPerSender[i] > 0):
            plt.title("Hourly messages from "+listPeople[i]+"\nSum = "+str(sum(hrPerSender[i]))+" msg / Average length of msg: "+decimizeStr(lenMsgPerSender[i]/nbMsgPerSender[i], 1)+" characters.")
        else: # Otherwise, you will have the exception ZeroDivisionError and you will kill a mathematician :(
            plt.title("Hourly messages from "+listPeople[i]+"\nSum = "+str(sum(hrPerSender[i]))+" msg")
    plt.savefig(pathRes+"/02c-hourlyRadarGraphPerUser.png", dpi=100, bbox_inches='tight')
    plt.close()
else:
    removeFile(pathRes+"/02c-hourlyRadarGraphPerUser.png*")
    print("Skipping Fig. 2ter: too many users...")
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
# Fig 3         ###############################################################
if(nbBins != 24):
    print("Plotting Fig. 3: messages per 1/4h.")
    plt.figure(figsize=(24,9))
    plt.grid(True)
    plt.bar(np.linspace(0,24-(24./nbBins),nbBins), hr[1], width=24.0/nbBins, alpha=.8, align='edge')
    # 3rd argument: bin every x=.25 (for every 15 min)
    # Example: np.linspace(0,23.75,96)
    for (a,b) in zip(np.linspace(0,24-(24./nbBins),nbBins), hr[1]):
        if(b>0): # For better visibility, we hide values below 10
            plt.text(a, b+.5 if b>10 else 1.05*b, str(b), fontsize=11)
    plt.xticks(np.arange(0,24,1))  
    plt.title("More accurate hourly repartition of msgs ("+firstMsgShort+" -> "+lastMsgShort+")")
    plt.savefig(pathRes+"/03a-preciseHourUse.png", dpi=100, bbox_inches='tight')
    plt.close()
    times.append(time.time())
    print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
    #plt.figure(3bis) #############################################################
    print("Plotting Fig. 3bis: precise radar graph for active hours.")
    # Taken from SO #
    matplotlib.rcParams['font.size'] = 16
    fig = plt.figure(figsize=(12+nbBins/8,12+nbBins/8))
    ax = fig.add_subplot(111,polar=True)
    H = len(hr[1]) 
    theta = np.arange(0, 2*np.pi, 2*np.pi/H) 
    ax.set_theta_zero_location('S') # To start with 0 on the bottom, 12 on the top
    bars = ax.bar(theta, hr[1], width=2*np.pi/H, align='edge') # Width = 2pi divided by nbr of bins (24)
    ax.set_xticks(theta)
    xLabels = np.linspace(0,24-(24./nbBins),nbBins)
    ax.set_xticklabels(decimizeList(xLabels, 1), fontsize=12)
    for (a,b) in zip(theta, hr[1]):
        plt.text(a+(2*np.pi/nbBins/3.), max(hr[1])*1.03, str(b), fontsize=14, color="red" if b>0 else 'gray', weight='bold', ha='center',va='center')
    ax.yaxis.grid(True)
    plt.title("Hourly repartition of msgs ("+firstMsgShort+" -> "+lastMsgShort+" - radar graph)\nTotal = "+str(sum(hr[0]))+" msg!")
    plt.savefig(pathRes+"/03b-preciseRadarGraph.png", dpi=100, bbox_inches='tight')
    plt.close()
    times.append(time.time())
    print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
else:
    print("Fig 3 == Fig 2: ignoring.")
    removeFile(pathRes+"/03a-preciseHourUse.png*")
    removeFile(pathRes+"/03b-preciseRadarGraph.png*")
#plt.figure(3ter) #############################################################
print("Plotting Fig. 4: stressing inactive moments.")
# Taken from SO #
matplotlib.rcParams['font.size'] = 12
fig = plt.figure(figsize=(min(48,12+nbBins/8),min(48,12+nbBins/8)))
ax = fig.add_subplot(111,polar=True)
H = len(hr[1]) 
theta = np.arange(0, 2*np.pi, 2*np.pi/H) 
ax.set_theta_zero_location('S') # To start with 0 on the bottom, 12 on the top
bars = ax.bar(theta, [min(hr[1][i],1) for i in range(nbBins)], width=2*np.pi/H, align='edge') # Width = 2pi divided by nbr of bins (24)
ax.set_xticks(theta)
xLabels = np.linspace(0,24-(24./nbBins),nbBins)
ax.set_xticklabels(decimizeList(xLabels, 1), fontsize=12)
ax.yaxis.grid(True)
plt.title("Number of empty bins: "+str(hr[1].count(0))+" / "+str(nbBins)+".\nTotal = "+str(sum(hr[0]))+" msg!", fontsize=40)
plt.savefig(pathRes+"/04-emptyMoments.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(5a)  ###############################################################
print("Plotting Fig. 5: daily repartition of msg.")
plt.figure(figsize=(24,9))
plt.grid(True)
for (a,b) in zip(msgPerDayX, msgPerDayY):
    if(b>0): # For better visibility, we hide values below 10
        plt.text(a, b+.5 if b>10 else 1.05*b, str(b), fontsize=10, ha='center',va='center')
#plt.xticks(np.arange(msgPerDayX[0], msgPerDayX[-1],5))
Q1, Q2, Q3 = findQuarters(msgPerDayX, msgPerDayY) # Dates when quarters have been reached
# Plotting quarter labels (+text)
plt.plot([Q1, Q2, Q3], [0,0,0], 'rD')
plt.text(Q1,0,"1/4", fontsize=15, color='red')
plt.text(Q2,0,"1/2", fontsize=15, color='red')
plt.text(Q3,0,"3/4", fontsize=15, color='red')
plt.bar(msgPerDayX, msgPerDayY, width=1, alpha=.8)
plt.title("Daily repartition of msgs ("+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig(pathRes+"/05a-dateMsgPerDay.png", dpi=100)
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(5b)  ###############################################################
print("Plotting Fig. 5b: monthly repartition of msg.")
plt.figure(figsize=(12,12))
plt.grid(True)
for (a,b) in zip(msgPerMonthX, msgPerMonthY):
    if(max(hr[0])>999):
        if(b>0):
            plt.text(a+dt.timedelta(days=7), b, str(b), fontsize=15, weight='bold', rotation=90, verticalalignment='top' if b*1.0/max(hr[0])>0.8 else 'bottom')
    else:
        if(b>0): # For better visibility, we hide values below 1
            plt.text(a+dt.timedelta(days=7), b+.5 if b>10 else 1.05*b, str(b), fontsize=16, weight='bold', horizontalalignment='left')
#plt.xticks(np.arange(msgPerDayX[0], msgPerDayX[-1],5))
# Plotting quarter labels (+text)
plt.plot([Q1, Q2, Q3], [0,0,0], 'rD')
plt.text(Q1,0,"1/4", fontsize=10, color='red')
plt.text(Q2,0,"1/2", fontsize=10, color='red')
plt.text(Q3,0,"3/4", fontsize=10, color='red')
plt.bar(msgPerMonthX, msgPerMonthY, align='edge', width=31, alpha=1)
plt.title("Monthly repartition of msgs ("+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig(pathRes+"/05b-dateMsgPerMonth.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(5c)  ###############################################################
print("Plotting Fig. 5c: days of the week")
plt.figure(figsize=(12,12))
plt.grid(True)
for (a,b) in zip(msgPerWeekDayX, msgPerWeekDayY):
    if(b>0): # For better visibility, we hide values below 1
        plt.text(a, b+.5 if b>10 else 1.05*b, str(b), fontsize=16, weight='bold', horizontalalignment='center')
#plt.xticks(np.arange(msgPerDayX[0], msgPerDayX[-1],5))
plt.bar(msgPerWeekDayX, msgPerWeekDayY, align='center', width=.7, alpha=1)
plt.title("Weekly repartition of msgs ("+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig(pathRes+"/05c-dateMsgPerWeekDay.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(6) ###############################################################
if nbMsgReac > 0:
    print("Plotting Fig. 6: reactions sent.")
    endList=N2-reacSent.count(0) # We strip away zero values by setting the starting point of our graph
    plt.figure(figsize=(min(200,6+max(reacSent)//10),min(600, 8+endList/2)))
    matplotlib.rcParams['font.size'] = 15
    plt.grid(axis='x')
    colors=['#ff8888','#eeee00','#0000ff','#00eeee','#ff0000','#00cc00','#cc0000','#00cccc']
    # Matplotlib bug: it sorts y axis by alphabetical order automatically, without sorting the other data :(
    reacSent, typeMessagesPerSender, reacPerMsg, reacReceived, listPeople, idPeople, nbMsgPerSender, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart = zip(*sorted(zip(reacSent, typeMessagesPerSender, reacPerMsg, reacReceived, listPeople, idPeople, nbMsgPerSender, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart), reverse=False)) # Get a clean ranking
    width = .7
    #plt.xticks(np.arange(msgPerDayX[0], msgPerDayX[-1],5))
    y = []
    p = []
    offset = [0]*endList
    for k in range(8): # For each reaction
        y.append([reacSentPerActor[i][k] for i in range(N2-endList, N2)])
        p.append([plt.barh(listPeople[N2-endList:], y[k], width, color=colors[k], left=offset)])
        for i in range(len(y[0])): # For each person
            if(y[k][i]!=0): 
                plt.text(y[k][i]/2.+offset[i], i, y[k][i], ha='center',va='center')
        offset = addList(offset, y[k])
    plt.legend([p[i][0] for i in range(8)], reacMean)
    plt.title("Reactions sent by participant ("+firstMsgShort+" -> "+lastMsgShort+")\nTotal = "+str(sum(reacSent))+" reactions")
    plt.savefig(pathRes+"/06a-reacSent.png", dpi=100, bbox_inches='tight')
    plt.close()  
    times.append(time.time())
    print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
    #plt.figure(6b)  ###############################################################
    if(N>2):
        print("Plotting Fig. 6b: reactions received.")
        endList=N2-reacReceived.count(0) # We strip away zero values by setting the starting point of our graph
        plt.figure(figsize=(min(200,6+max(reacReceived)//10),min(600, 8+endList/2)))
        plt.grid(axis='x')
        reacReceived, typeMessagesPerSender, reacPerMsg, avgLengthPerSender, nbMsgPerSender, listPeople, idPeople, reacSent, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart = zip(*sorted(zip(reacReceived, typeMessagesPerSender, reacPerMsg, avgLengthPerSender, nbMsgPerSender, listPeople, idPeople, reacSent, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart), reverse=False)) # Get a clean ranking
        y = []
        p = []
        offset = [0]*endList
        for k in range(8):
            y.append([reacReceivedPerSender[i][k] for i in range(N2-endList, N2)])
            p.append([plt.barh(listPeople[N2-endList:], y[k], width, color=colors[k], left=offset)])
            for i in range(len(y[0])): # For each participant
                if(y[k][i]!=0):
                    plt.text(y[k][i]/2.+offset[i], i, y[k][i], ha='center',va='center')
            offset = addList(offset, y[k])
        plt.legend([p[i][0] for i in range(8)], reacMean)
        plt.title("Reactions received for participants ("+firstMsgShort+" -> "+lastMsgShort+")\nTotal = "+str(sum(reacReceived))+" reactions")
        plt.savefig(pathRes+"/06b-reacReceived.png", dpi=100, bbox_inches='tight')
        plt.close()
        #plt.figure(6c)  ###############################################################
        print("Plotting Fig. 6c: reactions received PER MESSAGE.")
        endList=N2-reacPerMsg.count(0) # We strip away zero values by setting the starting point of our graph
        plt.figure(figsize=(16,min(600, 8+endList/2)))
        plt.grid(axis='x')
        reacPerMsg, typeMessagesPerSender, reacReceived, avgLengthPerSender, nbMsgPerSender, listPeople, idPeople, reacSent, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart = zip(*sorted(zip(reacPerMsg, typeMessagesPerSender, reacReceived, avgLengthPerSender, nbMsgPerSender, listPeople, idPeople, reacSent, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart), reverse=False)) # Get a clean ranking
        y = []
        p = []
        offset = [0]*endList
        for k in range(8):
            y.append([reacReceivedPerSender[i][k]/nbMsgPerSender[i] for i in range(N2-endList, N2)])
            p.append([plt.barh(listPeople[N2-endList:], y[k], width, color=colors[k], left=offset)])
            for i in range(len(y[0])): # For each participant
                if(y[k][i]!=0):
                    plt.text(y[k][i]/2.+offset[i], i, decimizeStr(y[k][i],2), ha='center',va='center')
            offset = addList(offset, y[k])
        plt.legend([p[i][0] for i in range(8)], reacMean)
        plt.title("Reactions received PER message ("+firstMsgShort+" -> "+lastMsgShort+")")
        plt.savefig(pathRes+"/06c-reacReceivedPerMsg.png", dpi=100, bbox_inches='tight')
        plt.close()
    
    else:
        print("Skipping Fig. 6b: duplicate with Fig6.")
        removeFile(pathRes+"/06b-reacReceived*")
        removeFile(pathRes+"/06c-reacReceived*")
else:
    print("Skipping Fig 6 and 6b: no reactions.")
    removeFile(pathRes+"/06*")
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(7)  ###############################################################
lenMsgPerSender, typeMessagesPerSender, reacPerMsg, nbMsgPerSender, listPeople, idPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart = zip(*sorted(zip(lenMsgPerSender, typeMessagesPerSender, reacPerMsg, nbMsgPerSender, listPeople, idPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart), reverse=False)) # Get a clean ranking
print("Plotting Fig. 7: length of msg by participants.")
matplotlib.rcParams['font.size'] = 16
if(N2>2):
    plt.figure(figsize=(12+N/3., 9+N/4.))
    plt.pie(lenMsgPerSender, labels=listPeople, autopct=makeAutopct(lenMsgPerSender), rotatelabels =True, shadow=False, labeldistance=1.02,  pctdistance=0.8, startangle=90)
    plt.axis('equal')
else:
    # There are two people. Don't ressort to that pie chart!
    colors = ['cornflowerblue', 'orange'] # We will use at most 2 colors anyway!
    listPeople, typeMessagesPerSender, idPeople, lenMsgPerSender, reacPerMsg, nbMsgPerSender, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart = zip(*sorted(zip(listPeople, typeMessagesPerSender, idPeople, lenMsgPerSender, reacPerMsg, nbMsgPerSender, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart), reverse=False)) # Get a clean ranking
    offset = [0, lenMsgPerSender[0]]
    plt.figure(figsize=(12, 3))
    plt.grid(axis='x')
    y = lenMsgPerSender
    p = plt.barh("", y, color=colors, left=offset) # Plot material
    for i in range(2):
        plt.text(y[i]/2.+offset[i], 0, str(y[i])+" ("+decimizeStr(y[i]*100./lenMsg,1)+"%)", ha='center', va='center')
    plt.legend([p[i] for i in range(2)], listPeople)
plt.title("Participants of the conversation *by characters written* ("+firstMsgShort+" -> "+lastMsgShort+")\nTotal Length: "+str(lenMsg)+" characters")
plt.savefig(pathRes+"/07-lenMsg.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")

#plt.figure(8)  ###############################################################
# This figure is special: it will show how often you start a message and how much "winds" you gave.
# A "wind" (ou vent in French) is when you ask a question and it stays without replies within 36h (*cries inside*).
# Warning: Data unreliable, especially if your friend replied in another way (SMS, directly, etc)
# So, don't start an argument from these data, thank you!
matplotlib.rcParams['font.size'] = 12
if (N != 0 and sum(convStartedBySender) != 0): # In fact, we can do that for any conversation! (Of course, there should be at least one message...)
    print("Plotting Fig. 8: conversation starters.")
    convStartedBySender, typeMessagesPerSender, reacPerMsg, avgLengthPerSender, nbMsgPerSender, listPeople, idPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart = zip(*sorted(zip(convStartedBySender, typeMessagesPerSender, reacPerMsg, avgLengthPerSender, nbMsgPerSender, listPeople, idPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart), reverse=False)) # Get a clean ranking
    if(N2>2):
        fig = plt.figure(figsize=(18,9))
        ax = fig.add_subplot(1,2,1)
        ax.pie(convStartedBySender, labels=listPeople, rotatelabels =True, autopct=makeAutopct(convStartedBySender), startangle=90)
        plt.axis('equal')
        plt.title("Who sends the 1st message?\n       Total = "+str(sum(convStartedBySender))+" starts.")
        #plt.text(-1.2,-1.2,"One conversation 'starts' when there is a message sent after 36 hours without messages sent/received.", ha='center')
        # Not quite pertinent... 
        ax = fig.add_subplot(1,2,2)
        nbHeart, typeMessagesPerSender, reacPerMsg, convStartedBySender, avgLengthPerSender, nbMsgPerSender, listPeople, idPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, ignoredMessagesPerUser, nbJe, nbTu, timeToReply, nbDuCoup = zip(*sorted(zip(nbHeart, typeMessagesPerSender, reacPerMsg, convStartedBySender, avgLengthPerSender, nbMsgPerSender, listPeople, idPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, ignoredMessagesPerUser, nbJe, nbTu, timeToReply, nbDuCoup), reverse=False)) # Get a clean ranking
        ax.pie(nbHeart, labels=listPeople, autopct=makeAutopct(nbHeart), rotatelabels =True, startangle=90)
        plt.axis('equal')
        plt.title("How many hearts <3 ?\n       Total = "+str(sum(nbHeart)))
        plt.savefig(pathRes+"/08-behaviorStats.png", dpi=100, bbox_inches='tight')
        plt.close()
    else:
        # For F2F conversations
        colors = ['cornflowerblue', 'orange'] # We will use at most 2 colors anyway!
        listPeople, typeMessagesPerSender, idPeople, nbHeart, colors, reacPerMsg, convStartedBySender, avgLengthPerSender, nbMsgPerSender, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, ignoredMessagesPerUser, nbJe, nbTu, timeToReply, nbDuCoup = zip(*sorted(zip(listPeople, typeMessagesPerSender, idPeople, nbHeart, colors, reacPerMsg, convStartedBySender, avgLengthPerSender, nbMsgPerSender, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, ignoredMessagesPerUser, nbJe, nbTu, timeToReply, nbDuCoup), reverse=False)) # Get a clean ranking
        plt.figure(figsize=(12, 6))
        plt.grid(axis='x')
        # Warning of DivisionByZero!
        if (sum(nbHeart) != 0):
            offset = [[0, convStartedBySender[0]*1.0/sum(convStartedBySender)*100.],[0, nbHeart[0]*1.0/sum(nbHeart)*100.]] # Values displayed between 0 and 100 (percentage)
            y = [divideList(convStartedBySender, sum(convStartedBySender)/100.), divideList(nbHeart, sum(nbHeart)/100.)]
            p = [plt.barh("Conv.\nstarted", y[0], color=colors, left=offset[0]), 
           plt.barh("Nb of\nhearts", y[1], color=colors, left=offset[1])] # Plot material
            for i in range(2):
                plt.text(y[0][i]/2.+offset[0][i], 0, decimizeStr(y[0][i]/100.*sum(convStartedBySender),0)+" ("+decimizeStr(y[0][i],1)+"%)", ha='center', va='center')
                plt.text(y[1][i]/2.+offset[1][i], 1, decimizeStr(y[1][i]/100.*sum(nbHeart),0)+" ("+decimizeStr(y[1][i],1)+"%)", ha='center', va='center')
            plt.legend(p[0], listPeople)
            plt.title("Some stats ("+str(sum(convStartedBySender))+" conversations and "+str(sum(nbHeart))+" <3)")
        else:
            offset = [[0, convStartedBySender[0]*1.0/sum(convStartedBySender)*100.]] # Values displayed between 0 and 100 (percentage)
            y = [divideList(convStartedBySender, sum(convStartedBySender)/100.)]
            p = [plt.barh("Conv.\nstarted", y[0], color=colors, left=offset[0])] # Plot material
            for i in range(2):
                plt.text(y[0][i]/2.+offset[0][i], 0, decimizeStr(y[0][i]/100.*sum(convStartedBySender),0)+" ("+decimizeStr(y[0][i],1)+"%)", ha='center', va='center')
            plt.legend(p[0], listPeople)
            plt.title("Some stats ("+str(sum(convStartedBySender))+" conversations but NO hearts (</3))")
        plt.savefig(pathRes+"/08-behaviorStats.png", dpi=100, bbox_inches='tight')
        plt.close()
else:
    print("Skipping Fig. 8: Suitable only if there is a F2F conversation.")
    removeFile(pathRes+"/08-behaviorStats.png*")
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(9)  ##############################################################
print("Plotting Fig. 9: average length of msg.")
avgLengthPerSender, typeMessagesPerSender, reacPerMsg, nbMsgPerSender, listPeople, idPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart = zip(*sorted(zip(avgLengthPerSender, typeMessagesPerSender, reacPerMsg, nbMsgPerSender, listPeople, idPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, timeToReply, nbHeart), reverse=False)) # Get a clean ranking
startList=avgLengthPerSender.count(0) # We strip away zero values by setting the starting point of our graph
plt.figure(figsize=(15, min(200, 8+(startList)/1.2)))
plt.grid(axis='x')
width = .8
plt.barh(listPeople[startList:], avgLengthPerSender[startList:], width, color='#00cc00')
for i in range(startList, N2):
    plt.text(max(avgLengthPerSender)*0.1, i-startList, str(avgLengthPerSender[i]), ha='center',va='center')
plt.title("Average length of each message ("+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig(pathRes+"/09-lengthOfMsg.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(10)  ##############################################################
print("Plotting Fig. 10: Length of long silences")
plt.figure(figsize=(12,10))
plt.grid(axis='y')
plt.plot(silenceArray[0][:1:-1], toDaysArray(silenceArray[1][:1:-1]))
plt.title("Length of silences (in days -- "+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig(pathRes+"/10-lengthOfSilences.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(11)  ##############################################################
if(sum(nbDuCoup) > 0):
    print("Plotting Fig. 11: Du coup...")
    nbDuCoup, typeMessagesPerSender, reacPerMsg, timeToReply, avgLengthPerSender, nbMsgPerSender, listPeople, idPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbHeart = zip(*sorted(zip(nbDuCoup, typeMessagesPerSender, reacPerMsg, timeToReply, avgLengthPerSender, nbMsgPerSender, listPeople, idPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbHeart), reverse=False)) # Get a clean ranking
    endList=N2-nbDuCoup.count(0) # We strip away zero values by setting the ending point of our graph
    startList=nbDuCoup.count(0) # We strip away zero values by setting the starting point of our graph
    plt.figure(figsize=(15, min(200, 8+endList/2)))
    plt.grid(axis='x')
    width = .8
    plt.barh(listPeople[startList:], nbDuCoup[startList:], width, color='#00dddd')
    for i in range(len(nbDuCoup)-startList):
        plt.text(0.1*max(nbDuCoup), i, str(nbDuCoup[i+startList]), ha='center',va='center')
    plt.title("Du coup, combien de 'Du coup'? ("+firstMsgShort+" -> "+lastMsgShort+")\nTotal = "+str(sum(nbDuCoup)))
    plt.savefig(pathRes+"/11-duCoup.png", dpi=100, bbox_inches='tight')
    plt.close()
else:
    print("Skipping Fig. 11: No 'Du coup' said")
    removeFile(pathRes+"/11*")  
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(12)  ##############################################################
#print("Plotting Fig. 12: Time to reply")
if (N2 <= 8):
    print("Plotting Fig. 12: time to reply per user")
    averageTTR = avgTTR(timeToReply) # Warning, this list is not attached to the other ones. Please add it when you zip lists!
    intervals = [0, 5, 30, 120, 300, 900, 3600, 
               3*3600, 6*3600, 12*3600, 86400,
               2*86400, 4*86400, 7*86400, 1e+10] 
    labelInt=["< 5s","5-30s","30s-2m","2-5m","5-15m",
                        "15m-1h", "1-3h", "3-6h", "6-12h", "12-24h",
                        "1-2d", "2-4d", "4-7d", "> 7d"]
    colorInt=['blue']*4 + ['green']*6 + ['red']*4
    fig = plt.figure(figsize=(12, 8*N2))
    for i in range(N2):
        ax = fig.add_subplot(N2,1,i+1)
        hist,binInt=np.histogram(timeToReply[i],intervals) # Substitute of distribTTR()
        ax.bar(range(len(hist)),hist,width=1,color=colorInt)
        ax.set_xticks(range(len(labelInt)))
        ax.set_xticklabels(labelInt[j] for j in range(len(labelInt)))
        if(len(timeToReply[i]) == 0):
            plt.title("TTR repartition for "+listPeople[i])
        else:
            plt.title("TTR repartition for "+listPeople[i]+"\nAverage: "+totalSecondsToStrShort(averageTTR[i]))
    plt.savefig(pathRes+"/12-TTR.png", dpi=100, bbox_inches='tight')
    plt.close()
else:
    removeFile(pathRes+"/12*")
    print("Skipping Fig. 12: too many users...")
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(13)  ##############################################################
print("Plotting Fig. 13a: About the last conversations / Length") # There are simpler ways to do it but here is the code from my sleep-deprived brain
# Extend the list of colors 
while(len(all_colors2) < N2):
    all_colors2 += all_colors2
fig=plt.figure(figsize=(12,12))
idPeople, typeMessagesPerSender, nbDuCoup, reacPerMsg, timeToReply, avgLengthPerSender, nbMsgPerSender, listPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbHeart = zip(*sorted(zip(idPeople, typeMessagesPerSender, nbDuCoup, reacPerMsg, timeToReply, avgLengthPerSender, nbMsgPerSender, listPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbHeart), reverse=False)) # Get a clean ranking
ax=fig.add_subplot(1,1,1)
nbBarsFig13 = min(15, len(startUser)) # If there are less than 15 conv, diplay less bars (obv.)
startUserUpdated = [i for i in startUser[:nbBarsFig13]] # The problem is that user id may change depending on the list sort. Solution: adding a unique id and compensate the changes.
plt.grid(False)
for (a,b) in zip(range(nbBarsFig13), list(reversed(nbMsgConv[:nbBarsFig13]))):
    plt.text(a, b+.5 if b>10 else 1.05*b, str(b), fontsize=16, weight='bold', horizontalalignment='center')
p = plt.bar(range(nbBarsFig13), list(reversed(nbMsgConv[:nbBarsFig13])), align='center', width=.85, alpha=1, color=[all_colors2[i] for i in list(reversed(startUserUpdated))])
plt.title("Last conversations: length and who started?")
listPeopleWithCount = [listPeople[i]+" ("+str(startUserUpdated.count(i))+")" for i in range(len(listPeople))]
legend1,legend2=[],[] # For making the legend (legend1: list of interesting bars, legend2: the respective labels)
ax.set_xticks(range(nbBarsFig13)) # One tick for each bar
ax.set_xticklabels([]+[str(nbBarsFig13)+"\nconv ago"]+list(reversed(range(2,nbBarsFig13)))+["Last\nconv"]) # Custom axis, way more class ;) 
for i in range(len(listPeopleWithCount)):
    try:
        legend1.append(p[list(reversed(startUserUpdated)).index(i)])
        legend2.append(listPeopleWithCount[i])
    except:
        True # This person did not start any of the last 15 conversations
plt.legend(legend1,legend2) 
# Explanations: for the legend, I take only one bar per person (the first one... if it exists, hence the try/except)
plt.savefig(pathRes+"/13a-lastConv.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
###############################################################################
print("Plotting Fig. 13b: About the last conversations / Duration") # There are simpler ways to do it but here is the code from my sleep-deprived brain
fig=plt.figure(figsize=(12,12))
ax=fig.add_subplot(1,1,1)
lastDurationConvInSeconds = [durationConv[:nbBarsFig13][i].total_seconds() for i in range(nbBarsFig13)] # Not inverted yet: 1st value = most recent
for (a,b) in zip(range(nbBarsFig13), list(reversed(lastDurationConvInSeconds))):
    plt.text(a, b, totalSecondsToStrShort(b), fontsize=14, rotation=90, ha='center',va='center', verticalalignment='top' if b*1.0/max(lastDurationConvInSeconds)>0.8 else 'bottom')
p = plt.bar(range(nbBarsFig13), list(reversed(lastDurationConvInSeconds)), align='center', width=.85, alpha=1, color=[all_colors2[i] for i in list(reversed(startUserUpdated))])
plt.title("Last conversations: duration")
ax.set_xticks(range(nbBarsFig13)) # One tick for each bar
ax.set_xticklabels([]+[str(nbBarsFig13)+"\nconv ago"]+list(reversed(range(2,nbBarsFig13)))+["Last\nconv"]) # Custom axis, way more class ;) 
listPeopleWithCount = [listPeople[i]+" ("+str(startUserUpdated.count(i))+")" for i in range(len(listPeople))]
plt.legend(legend1,legend2)  # The same legend as Fig 13a
# Explanations: for the legend, I take only one bar per person (the first one... if it exists, hence the try/except)
plt.savefig(pathRes+"/13b-lastConvDuration.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
###############################################################################
print("Plotting Fig. 13c: About the last conversations / Time between conv (silences)") # There are simpler ways to do it but here is the code from my sleep-deprived brain
fig=plt.figure(figsize=(12,12))
ax=fig.add_subplot(1,1,1)
silenceInSeconds = [silenceArray[1][i].total_seconds() for i in range(nbBarsFig13)]
for (a,b) in zip(range(nbBarsFig13), list(reversed(silenceInSeconds))):
    plt.text(a, b, totalSecondsToStrShort(b), fontsize=14, rotation=90, ha='center',va='center', verticalalignment='top' if b*1.0/max(silenceInSeconds)>0.8 else 'bottom')
p = plt.bar(range(nbBarsFig13), list(reversed(silenceInSeconds)), align='center', width=.85, alpha=1, color='grey')
plt.title("Last conversations: silences (before starting the nth conv)")
ax.set_xticks(range(nbBarsFig13)) # One tick for each bar
ax.set_xticklabels([]+[str(nbBarsFig13)+"\nconv ago"]+list(reversed(range(2,nbBarsFig13)))+["Last\nconv"]) # Custom axis, way more class ;) 
plt.savefig(pathRes+"/13c-lastConvSilence.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(14a)  #############################################################
matplotlib.rcParams['font.size'] = 13
nbMedia = sum(typeMessages[offsetLabelTypeMessages:offsetLabelTypeMessages+7])
if (N != 0 and nbMedia != 0): # Avoid drawing blank graphes
    print("Plotting Fig. 14a: Media sent.")
    # all_colors2 are the colors used (enough values for the conversations, don't worry)
    plt.figure(figsize=(20,17))
    plt.grid(axis='x')
    valuesAsPercent = []
    graphLabel = []
    for i in range(offsetLabelTypeMessages,offsetLabelTypeMessages+7): 
        # From 6 to 13, unless other categories are added
        if(sum(percentageRowTabl(typeMessagesPerSender, i))) >= 0:
            valuesAsPercent.append(percentageRowTabl(typeMessagesPerSender, i))
            graphLabel.append(labelTypeMessages[i])
    y = []
    p = []
    labelPerson = []
    skippedI = 0 # We will remove 0 values in y. So, when checking the values, we should count skipped values to avoid IndexOutOfRange
    offset = [0]*len(graphLabel) # Can be 7... or less
    for i in range(N2): # For each participant
        tabl = getRowTabl(valuesAsPercent, i)
        if(sum(tabl) != 0):
            y.append(tabl)
            p.append([plt.barh(graphLabel, tabl, width, color=all_colors2[i], left=offset)])
            for j in range(len(graphLabel)):
                val = int(round(y[i-skippedI][j]/100.0*typeMessages[offsetLabelTypeMessages+j],0)) # A number of occurences
                percentage = y[i-skippedI][j]
                if (percentage == 0): # No annotation
                    pass 
                elif (percentage < 4.4): # Too small: only the value
                    plt.text(y[i-skippedI][j]/2.+offset[j], j, str(val), ha='center',va='center')
                else: # Enough room to display the percentage AND the value
                    plt.text(y[i-skippedI][j]/2.+offset[j], j, str(val)+" ("+decimizeStr(y[i-skippedI][j],1)+"%)", ha='center',va='center')
            labelPerson.append(listPeople[i])
            offset = addList(offset, tabl)
            plt.xticks(np.arange(0,110,10))
        else:
            skippedI += 1
    plt.legend([p[i][0] for i in range(len(labelPerson))], labelPerson, bbox_to_anchor=(1, 1))
    plt.title("Media shared (pics, vids, GIF, etc) - Total: "+str(nbMedia))
    plt.savefig(pathRes+"/14a-mediaShared.png", dpi=100, bbox_inches='tight')
    plt.close()
else:
    removeFile(pathRes+"/14a*")
    print("Skipping Fig. 14a: No other media sent")
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(14b)  #############################################################
#%%
nbActions = sum(typeMessages[offsetLabelTypeMessages+7:-2])
if (N != 0 and nbActions != 0): # Avoid drawing blank graphes
    print("Plotting Fig. 14b: Actions done.")
    # all_colors2 are the colors used (enough values for the conversations, don't worry)
    plt.figure(figsize=(20,32))
    plt.grid(axis='x')
    valuesAsPercent = []
    graphLabel = []
    for i in range(offsetLabelTypeMessages+7,offsetLabelTypeMessages+24): 
        # From 7 to 23, unless other categories are added
        if(sum(percentageRowTabl(typeMessagesPerSender, i))) >= 0:
            valuesAsPercent.append(percentageRowTabl(typeMessagesPerSender, i))
            graphLabel.append(labelTypeMessages[i])
    y = []
    p = []
    labelPerson = []
    skippedI = 0 # We will remove 0 values in y. So, when checking the values, we should count skipped values to avoid IndexOutOfRange
    offset = [0]*len(graphLabel) # Can be 17... or less
    for i in range(N2): # For each participant
        tabl = getRowTabl(valuesAsPercent, i)
        if(sum(tabl) != 0):
            y.append(tabl)
            p.append([plt.barh(graphLabel, tabl, width, color=all_colors2[i], left=offset)])
            for j in range(len(graphLabel)):
                val = int(round(y[i-skippedI][j]/100.0*typeMessages[offsetLabelTypeMessages+7+j],0)) # A number of occurences (+7 'cause we check the actions! (from #13))
                percentage = y[i-skippedI][j]
                if (percentage == 0): # No annotation
                    pass 
                elif (percentage < 4.4): # Too small: only the value
                    plt.text(y[i-skippedI][j]/2.+offset[j], j, str(val), ha='center',va='center')
                else: # Enough room to display the percentage AND the value
                    plt.text(y[i-skippedI][j]/2.+offset[j], j, str(val)+" ("+decimizeStr(y[i-skippedI][j],1)+"%)", ha='center',va='center')
            labelPerson.append(listPeople[i])
            offset = addList(offset, tabl)
            plt.xticks(np.arange(0,110,10))
        else:
            skippedI += 1
    plt.legend([p[i][0] for i in range(len(labelPerson))], labelPerson, bbox_to_anchor=(1, 1))
    plt.title("Actions done (group management, waving, polling, etc) - Total: "+str(nbActions))
    plt.savefig(pathRes+"/14b-actionsDone.png", dpi=100, bbox_inches='tight')
    plt.close()
else:
    removeFile(pathRes+"/14b*")
    print("Skipping Fig. 14b: No actions done...")
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
###############################################################################
#%%
try:
    ratioConvTotal = decimizeStr(100.0*sum(lastDurationConvInSeconds)/(sum(silenceInSeconds)+sum(lastDurationConvInSeconds)),2)
except:
    ratioConvTotal = 100 # Active all the time (!)
###############################################################################

# For further analysis: I will do a .csv file for comparing other conversations :) 
# TODO
#%%
sendToCsv()
try:
    if (sys.version_info[0] == 2):
        import jinja
    else:
        import jinja2 as jinja
    saveReportToHtml()
except ImportError:
    print("/!\\ Jinja lib is not found. You should install it with 'pip install jinja' (no need to have admin rights)")
times.append(time.time())
print("~ Analysis done with love in "+decimizeStr(times[-1]-times[0], 3)+" seconds! ~")
###### END OF PROGRAM ######
