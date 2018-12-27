# Make stats for Facebook
# f: the file (wille be quickly closed anyway)
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
import sys


#from random import sample
all_colors = [k for k,v in pltc.cnames.items()]
all_colors2=["steelblue","indianred","darkolivegreen","olive","darkseagreen","pink","tomato","orangered","darkslategrey","greenyellow","burlywood","mediumspringgreen","chartreuse","dimgray","black","springgreen","orange","darkslategray","brown","dodgerblue","peru","lawngreen","chocolate","crimson","forestgreen","darkgrey","cyan","mediumorchid","darkviolet","darkgray","darkgreen","darkturquoise","red","deeppink","darkmagenta","gold","hotpink","firebrick","steelblue","indianred","mistyrose","darkolivegreen","olive","darkseagreen","pink","tomato","orangered","darkslategrey","greenyellow","burlywood","seashell","mediumspringgreen","chartreuse","dimgray","black","springgreen","orange","darkslategray","brown","dodgerblue","peru","lawngreen","chocolate","crimson","forestgreen","darkgrey","cyan","mediumorchid","darkviolet","darkgray","darkgreen","darkturquoise","red","deeppink","darkmagenta","gold","hotpink","firebrick"]
times = [time.time()] # For debug: how long each graph takes to load?

####################
# User-editable variables - What you can edit, without looking for ages in the code
nbBins = 24                             # Subdiv per day Useful for Fig3. MUST be a multiple of 24 and dividable by 1440
                                        # Choose between: 24, 48, 72, 96, 120, 144, 240, 288, 360, 480, 720, 1440.
startDate = dt.datetime(2000,12,1)       # When you want to start the stats. Good idea to take the last three months for example.
                                        # Format: dt.datetime(yyyy,m,d) - NO leading zeroes even if it is fancier with!
                                        # 
timeZoneStartTime = 1                   # 1 for UTC+01:00 (Winter time in France) (+1 if DST)
matplotlib.rcParams['font.size'] = 16   #
widthImg = 1024                         # Width of the images on the HTML report. Soon, it will be set automatically ;)  
encoding = 'latin1'                     # If there are accents (for French people), this encoding works fine. 
decoding = 'utf-8'                      # To interpret accent words from json, use this: u'\xc3\x89'.encode('latin1').decode('utf-8')
# Below this line: do NOT edit unless you know what you do!
####################
startTimeStamp = (startDate - dt.datetime(1970,1,1)).total_seconds()-timeZoneStartTime*3600

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
  # Returns nothing
  global name
  global nameFirst
  global nameLast
  global reacActor
  global reacSender
  global listPeople
  name = prettyTxt(name)
  nameFirst = prettyTxt(nameFirst)
  nameLast = prettyTxt(nameLast)
  reacActor = prettyTxt(reacActor)
  reacSender = prettyTxt(reacSender)
  listPeople = list(listPeople)
  for i in range(len(listPeople)):
    listPeople[i] = prettyTxt(listPeople[i])
  
def makeSubplot(N):
  # How to do subplots like a boss (nb, position, etc) ?
  # Check it here!
  if (N<30):
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
      print("WARN: one blank message in position #"+str(i))
  return l

def getLenMsg(data):
  # Ex: simply type m for the whole msg
  l = 0
  try:
    l = len(data['content'])
  except:
    print("WARN: one blank message!")
  return l

def decimize(var, nb):
  # Gives to var nb figures after the decimal point.
  return 1.0*int(var*10**nb)/10**nb
 
def decimizeStr(var, nb):
  # Gives to var nb figures after the decimal point.
  return str(1.0*int(1.0*var*10**nb)/10**nb)

def decimizeList(L, nb):
  # Gives to all vars in L nb figures after the decimal point.
  return [decimize(var, nb) for var in L]

def pareto(nbMsgPart):
  # Returns three values: [0]the %age of biggest users, doing [1](=100-[0])%age of msg sent ([2]: true %age)
  N = len(nbMsgPart)
  S = sum(nbMsgPart)
  n = 0
  s = 0
  while(1.0*s/S+1.0*n/N < 1):
    s += nbMsgPart[n]
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
  
  header = ("Type;Name;Start_Date;Start_Who;End_Date;End_Who;NbPart_curr;NbPart_total;" + 
            "")
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
    with open(csvName, 'ab') as csvFile: # a for append, b for bytes mode
      csvFile.write('\n')
      csvFile.write(res)  
  else: # With Python 3, you must use convert text to bytes to add, hence the .encode()
    with open(csvName, 'ab') as csvFile: # a for append, b for bytes mode
      csvFile.write('\n'.encode())
      csvFile.write(res.encode())

def removeFile(fileName):
  with open(fileName,'w') as f: 
    f.write("This file will be removed") # Erase the figure, if it existed before
  if os.path.isfile(fileName):
    os.remove(fileName)

def saveReportToHtml():
  # Create a HTML file with all the information
  templateLoader = jinja.FileSystemLoader(searchpath="./")
  templateEnv = jinja.Environment(loader=templateLoader)
  
  #Insertion of images (miniature or full)
  try:
    # If we can create miniatures for a better webpage
    from PIL import Image
    # Resize images and add '_mini' after (TODO)
    sizeImg="_mini"
  except:
    # If PIL is not installed, I will not use miniatures but the full img (For tests only!!!)
    sizeImg=""
  sizeImg="" # TEMPorary (TODO: correct that)
  if(typ == "RegularGroup"):
    TEMPLATE_FILE = "templateGroup.html"
  else:
    TEMPLATE_FILE = "templatePrivate.html"
  template = templateEnv.get_template(TEMPLATE_FILE)
  
  outputText = template.render(encoding=encoding, sizeImg=sizeImg, widthImg=widthImg, name=name, N=N, N2=N2, 
                               dateCreation= dt.datetime.isoformat(dt.datetime.now()), 
                               firstMsg=firstMsg, lastMsg=lastMsg, nameFirst=nameFirst, nameLast=nameLast, 
                               firstMsgShort=firstMsgShort, lastMsgShort=lastMsgShort,
                               silenceTime=totalSecondsToStr(silenceTime.total_seconds()),
                               nbMsg=nbMsg, avgNbMsg=decimizeStr(1.0*nbMsg/(1.0*N), 2),
                               Q2=Q2, Q1=Q1, Q3=Q3, nbConv=sum(convStartedBySender),
                               nbMsgReac=nbMsgReac, percentMsgReac=decimizeStr(100*nbMsgReac/nbMsg,1), nbReac=nbReac, reacPerMsg=decimizeStr(nbReac/nbMsgReac, 2),
                               pareto0=paretoRes[0], pareto1=paretoRes[1], pareto2=paretoRes[2], lenMsgConv=decimizeStr(nbMsg/sum(convStartedBySender), 1), 
                               totalTimeConv=totalSecondsToStr(convoTimeSpent.total_seconds()))
  html_file = open('stats.html', 'wb')
  html_file.write(outputText.encode(encoding))
  html_file.close()

###### Using the functions for stats
typ = j['thread_type']
name = j['title']
N = len(j['participants'])
listPeople = getListPeople(j, N)
reacSentPerActor = [[0]*8 for x in range(N)] # Position k for listPeople[k] - reactions SENT
reacReceivedPerSender = [[0]*8 for x in range(N)] # Position k for listPeople[k] - reactions RECEIVED
hrPerSender = [[0]*24 for x in range(N)] # Position k for listPeople[k] - hour msg # Hourly distribution per user
nbMsgPart = [0]*N # Messages sent by Sender
lenMsgPerSender = [0]*N # Length of msg written by Sender
convStartedBySender = [0]*N # Who starts conversations? (Used so far if N==2)
ignoredMessagesPerUser = [0]*N # Who ignores their friend? (Used so far if N==2)
nbHeart = [0]*N
nbJe = [0]*N
nbTu = [0]*N
nbDuCoup = [0]*N
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
nbReac = 0
nbMsgReac = 0
reacMean =["Love","Haha","Wow!","Sad ","Grrr"," +1 "," -1 ","Misc"]
reacHex  =["98 8d","98 86","98 ae","98 a2","98 a0","91 8d","91 8e","00 00"]
reacNb = [0]*8
heartHex = "e2 9d a4" # This variable represents a heart

# Stats of participation / Analyze per message
for m in j['messages']:
  # Date filter
  if (m['timestamp_ms']/1000. > startTimeStamp):
    # Count number of messages
    nbMsg += 1
    lenMsg += getLenMsg(m)
    try:
      idUser = listPeople.index(m['sender_name']) # idUser is between 0 and N-1 and identifies an user
      nbMsgPart[idUser] += 1
      hourCurrentMsg = dt.datetime.fromtimestamp(m['timestamp_ms']/1000).hour # Refers to the hour of the msg sent
      hrPerSender[idUser][hourCurrentMsg] += 1
      lenMsgPerSender[idUser] += getLenMsg(m)
    except ValueError:
      # If the user does not belong to the conv anymore
      # print("INFO: "+m['sender_name']+" is not in the conv anymore. Added to the list.")
      listPeople.append(m['sender_name'])
      nbMsgPart.append(1)
      reacReceivedPerSender.append([0]*8)
      reacSentPerActor.append([0]*8)
      hrPerSender.append([0]*24)
      lenMsgPerSender.append(getLenMsg(m))
      convStartedBySender.append(0)
      ignoredMessagesPerUser.append(0)
      nbHeart.append(0)
      nbDuCoup.append(0)
      nbJe.append(0)
      nbTu.append(0)
      idUser = listPeople.index(m['sender_name']) # Now, the user is added :) 
    except KeyError:
      # The user does not exist anymore (removed account, ...)
      if "UNKNOWN" in listPeople:
        # We already analysed a message from a deleted account
        unk = listPeople.index("UNKNOWN")
        nbMsgPart[unk] += 1
        idUser = unk
      else:
        # Oh, just discovered a removed account. Let's count it!
        listPeople.append(u"UNKNOWN")
        nbMsgPart.append(1)
        reacReceivedPerSender.append([0]*8)
        reacSentPerActor.append([0]*8)
        hrPerSender.append([0]*24)
        lenMsgPerSender.append(getLenMsg(m))
        convStartedBySender.append(0)
        ignoredMessagesPerUser.append(0)
        nbHeart.append(0)
        nbDuCoup.append(0)
        nbJe.append(0)
        nbTu.append(0)
        idUser = listPeople.index("UNKNOWN") # Now, the user is added :) 
    
    # Classic procedure for each message (retrieving date of the msg, the hour, etc)
    hourMsg.append(dt.datetime.fromtimestamp(m['timestamp_ms']/1000))
    d=dt.datetime.fromtimestamp(m['timestamp_ms']/1000).date() # date in the form of datetime.date(2018,12,25)
    hourMsgD.append(d)
    hourMsgMo.append(dt.date(d.year, d.month, 1))  # We create a distribution depending on the month (day of the month=1)
    
    # Count nb of certain words.
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
    
    # Reactions!  
    try:
      reacs = m['reactions']
      nbReac = nbReac + len(m['reactions'])
      nbMsgReac = nbMsgReac + 1
      for reac in reacs:
        ch = reac['reaction'][2:]
        reacMsgHex = (" ".join("{:02x}".format(ord(c)) for c in ch)) # Convert weird chars into (0x)98 for example.
        reacActor = reac['actor'] # Get actor of the reaction
        reacActorIndex = listPeople.index(reacActor)
        reacSender = m['sender_name'] # Get the sender of the message provoking reac(s)
        reacSenderIndex = listPeople.index(reacSender)
        try:
          reacNb[reacHex.index(reacMsgHex)] += 1 # Update overall nb of reactions
          reacSentPerActor[reacActorIndex][reacHex.index(reacMsgHex)] += 1
          reacReceivedPerSender[reacSenderIndex][reacHex.index(reacMsgHex)] += 1
        except ValueError:
          # Remember when ya put custom reactions? Now, think about them!
          print("Note: someone reacted with a weird emoji.")
          reacNb[7] += 1
          reacSentPerActor[reacActorIndex][7] += 1
          reacReceivedPerSender[reacSenderIndex][7] += 1
    except KeyError:
      False # No reactions
  # else:
    # Not counted. Out of date bounds.

N2 = len(listPeople)
reacReceived = [sum(reacReceivedPerSender[i]) for i in range(N2)]
reacSent = [sum(reacSentPerActor[i]) for i in range(N2)]
if(len(hourMsgD) == 0):
  print("[FATAL] Date bounds too tight or empty conversation! Change the value of startDate or reset it by choosing year 2000")
  print("The next line will yield a IndexError exception: this is a logic consequence.")
# Silence time
for i in range(1, nbMsg):
  a,b = hourMsg[i-1], hourMsg[i]
  if (a-b > silenceTime):
    silenceTime = a-b
# Now, we have the good value for silenceTime.

# Who starts first and Fig8
for i in range(1, nbMsg):
  a,b = hourMsg[i-1], hourMsg[i] # a is more recent than b ([0]: most recent)
  if (a-b > dt.timedelta(1,60)): # There is more than 24h between two msgs
    idUser = listPeople.index(j['messages'][i-1]['sender_name']) # id of the guy who started the conv.
    convStartedBySender[idUser] += 1
    silenceArray[0].append(a)
    silenceArray[1].append(a-b)
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
for i in range(N2):
  if (sum(hrPerSender[i]) == 0):
    avgLengthPerSender.append(0)
  else:
    avgLengthPerSender.append(decimize(lenMsgPerSender[i]/sum(hrPerSender[i]), 1))

# First thing, last thing (+by ...)
firstMsgTS = j['messages'][nbMsg-1]['timestamp_ms']/1000. 
firstMsg = dt.datetime.fromtimestamp(firstMsgTS).isoformat()
firstMsgShort = str(dt.datetime.fromtimestamp(firstMsgTS).date())
lastMsgTS = j['messages'][0]['timestamp_ms']/1000. # FB logic: the last message is 1st
lastMsg = dt.datetime.fromtimestamp(lastMsgTS).isoformat()
lastMsgShort = str(dt.datetime.fromtimestamp(lastMsgTS).date())
nameFirst = j['messages'][nbMsg-1]['sender_name']
nameLast = j['messages'][0]['sender_name']

# Sort everything
nbMsgPart, listPeople, reacSentPerActor, reacSent, reacReceived, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup, nbHeart = zip(*sorted(zip(nbMsgPart, listPeople, reacSentPerActor, reacSent, reacReceived, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup, nbHeart), reverse=False))
msgPerDayX, msgPerDayY = nbDailyMsg(hourMsgD)
msgPerMonthX, msgPerMonthY = nbDailyMsg(hourMsgMo)
times.append(time.time())

# Correcting the encoding before displaying everything
prettyAllTxt()

print("Process done in "+str(times[-1]-times[-2])+"+ sec")

times.append(time.time())
# Display everything (or export them - up to you!)
textFile = open('Stats.txt','wb')
#textFile = 'Stats.txt'
print("####################")
if (typ=="RegularGroup"):
  printToFile("Stats of the conversation ["+name+"]:", textFile)
  printToFile("> Number of current participants: "+str(N) + ", plus "+str(N2-N)+" former participants.", textFile)
else:
  printToFile("Your interaction with "+name+":", textFile)
# Generic information
printToFile("> The 1st message has been written on "+firstMsg+" by "+nameFirst+".", textFile)
printToFile("> Last message saved: written on "+lastMsg+" by "+nameLast+".", textFile)
printToFile("> Longest silence: "+totalSecondsToStr(silenceTime.total_seconds()), textFile)
printToFile("> "+str(nbMsg)+" messages have been written, making an average of "+decimizeStr(1.0*nbMsg/(1.0*N), 2)+" messages per participant.", textFile)
Q1, Q2, Q3 = findQuarters(msgPerDayX, msgPerDayY) # Dates when quarters have been reached
printToFile("> Half of all messages have been written before/after "+str(Q2), textFile)
printToFile("> Messages are in average "+decimizeStr(lenMsg/nbMsg, 1)+" characters long.", textFile)
paretoRes = pareto(nbMsgPart)
if (typ=="RegularGroup"): 
  # If there is more than two participants
  printToFile("> Among the "+str(nbMsgReac)+" messages with reactions ("+decimizeStr(100*nbMsgReac/nbMsg,1)+"%), participants have reacted "+str(nbReac)+" times ("+decimizeStr(nbReac/nbMsgReac, 2)+" times per message).", textFile)
  printToFile("> Pareto: "+paretoRes[0]+"% of users posted more than "+paretoRes[1]+"% of messages ("+paretoRes[2]+"%).", textFile)
else:
  # Private conv
  printToFile("> "+str(nbMsgReac)+" messages led to a reaction ("+decimizeStr(100*nbMsgReac/nbMsg,1)+"%).", textFile)
  printToFile("> On average, each coversation lasted "+decimizeStr(nbMsg/sum(convStartedBySender), 1)+" messages before dying", textFile)
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

def sortList(byThisList, reverse):
  byThisList, reacReceived, avgLengthPerSender, nbMsgPart, listPeople, reacSent, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, nbHeart = zip(*sorted(zip(byThisList, reacReceived, avgLengthPerSender, nbMsgPart, listPeople, reacSent, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, nbHeart), reverse=reverse)) # Get a clean ranking

### Graphes     ###############################################################
#plt.figure(1)  ###############################################################
print("Plotting Fig. 1: participants.")
matplotlib.rcParams['font.size'] = 18
plt.figure(figsize=(12+N/3., 9+N/4.))
plt.pie(nbMsgPart, labels=listPeople, autopct=makeAutopct(nbMsgPart), shadow=False, rotatelabels =True, labeldistance=1.02,  pctdistance=0.8, startangle=90)
plt.axis('equal')
plt.title("Participants of the conversation ("+firstMsgShort+" -> "+lastMsgShort+")\n\n")
plt.savefig("01-participants.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(2) ###############################################################
# Rule of thumb: for high values (>360), prepare a good computer (720: 2GB of RAM + 60'' CPU time, 1440: 5GB + 90'' for the program alone)
hr=hourPost(hourMsg, nbBins)
print("Plotting Fig. 2: messages per hour.")
matplotlib.rcParams['font.size'] = 12
plt.figure(figsize=(12, 9))
plt.bar(np.arange(24), hr[0], width=1, alpha=.8, align='edge')
for (a,b) in zip(np.arange(24), hr[0]):
  if(b>0):
    plt.text(a+.02, b+.5 if b>10 else 1.05*b, str(b), fontsize=15, weight='bold')
plt.xticks(np.arange(0,24,1))    
plt.grid(axis='x')
plt.title("Hourly repartition of msgs ("+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig("02a-hourUse.png", dpi=100, bbox_inches='tight')
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
plt.savefig("02b-hourlyRadarGraph.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(2c) ##########################################################
if (N < 30):
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
    bars = ax.bar(theta, hrPerSender[i], width=2*np.pi/H, align='edge', color=col) # Width = 2pi divided by nbr of bins (24)
    for (a,b) in zip(theta, hrPerSender[i]):
      plt.text(a+(2*np.pi/24/2.), max(hrPerSender[i]), str(b), fontsize=10, color="black" if b>0 else 'white', weight='bold')
    ax.yaxis.grid(True)
    if(lenMsgPerSender[i]>0 and nbMsgPart[i] > 0):
      plt.title("Hourly messages from "+listPeople[i]+"\nSum = "+str(sum(hrPerSender[i]))+" msg / Average length of msg: "+decimizeStr(lenMsgPerSender[i]/nbMsgPart[i], 1)+" characters.")
    else: # Otherwise, you will have the exception ZeroDivisionError and you will kill a mathematician :(
      plt.title("Hourly messages from "+listPeople[i]+"\nSum = "+str(sum(hrPerSender[i]))+" msg")
  plt.savefig("02c-hourlyRadarGraphPerUser.png", dpi=100, bbox_inches='tight')
  plt.close()
else:
  removeFile("02c-hourlyRadarGraphPerUser.png")
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
  plt.savefig("03a-preciseHourUse.png", dpi=100, bbox_inches='tight')
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
  plt.title("Hourly repartition of msgs  ("+firstMsgShort+" -> "+lastMsgShort+" - radar graph)\nTotal = "+str(sum(hr[0]))+" msg!")
  plt.savefig("03b-preciseRadarGraph.png", dpi=100, bbox_inches='tight')
  plt.close()
  times.append(time.time())
  print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
else:
  print("Fig 3 == Fig 2: ignoring.")
  removeFile("03a-preciseHourUse.png")
  removeFile("03b-preciseRadarGraph.png")
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
plt.savefig("04-emptyMoments.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(4)  ###############################################################
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
plt.savefig("05a-dateMsgPerDay.png", dpi=100)
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(5)  ###############################################################
print("Plotting Fig. 5b: monthly repartition of msg.")
plt.figure(figsize=(12,12))
plt.grid(True)
for (a,b) in zip(msgPerMonthX, msgPerMonthY):
  if(b>0): # For better visibility, we hide values below 1
    plt.text(a+dt.timedelta(days=7), b+.5 if b>10 else 1.05*b, str(b), fontsize=16, weight='bold')
#plt.xticks(np.arange(msgPerDayX[0], msgPerDayX[-1],5))
# Plotting quarter labels (+text)
plt.plot([Q1, Q2, Q3], [0,0,0], 'rD')
plt.text(Q1,0,"1/4", fontsize=10, color='red')
plt.text(Q2,0,"1/2", fontsize=10, color='red')
plt.text(Q3,0,"3/4", fontsize=10, color='red')
plt.bar(msgPerMonthX, msgPerMonthY, align='edge', width=31, alpha=1)
plt.title("Monthly repartition of msgs ("+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig("05b-dateMsgPerMonth.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(6) ###############################################################
if nbMsgReac > 0:
  print("Plotting Fig. 6: reactions sent.")
  endList=N2-reacSent.count(0) # We strip away zero values by setting the starting point of our graph
  plt.figure(figsize=(min(200,6+max(reacSent)//10),min(600, 8+endList/2)))
  matplotlib.rcParams['font.size'] = 12
  plt.grid(axis='x')
  colors=['#ff8888','#eeee00','#0000ff','#00eeee','#ff0000','#00cc00','#cc0000','#00cccc']
  # Matplotlib bug: it sorts y axis by alphabetical order automatically, without sorting the other data :(
  reacSent, reacReceived, listPeople, nbMsgPart, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup, nbHeart = zip(*sorted(zip(reacSent, reacReceived, listPeople, nbMsgPart, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup, nbHeart), reverse=False)) # Get a clean ranking
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
  plt.savefig("06a-reacSent.png", dpi=100, bbox_inches='tight')
  plt.close()  
  times.append(time.time())
  print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
  #plt.figure(6b)  ###############################################################
  if(N>2):
    print("Plotting Fig. 6b: reactions received.")
    endList=N2-reacReceived.count(0) # We strip away zero values by setting the starting point of our graph
    plt.figure(figsize=(min(200,6+max(reacReceived)//10),min(600, 8+endList/2)))
    plt.grid(axis='x')
    reacReceived, avgLengthPerSender, nbMsgPart, listPeople, reacSent, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, nbHeart = zip(*sorted(zip(reacReceived, avgLengthPerSender, nbMsgPart, listPeople, reacSent, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, nbHeart), reverse=False)) # Get a clean ranking
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
    plt.savefig("06b-reacReceived.png", dpi=100, bbox_inches='tight')
    plt.close()
  else:
    print("Skipping Fig. 6b: duplicate with Fig6.")
    removeFile("06b-reacReceived.png")
else:
  print("Skipping Fig 6 and 6b: no reactions.")
  removeFile("06a-reacSent.png")
  removeFile("06b-reacReceived.png")
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(7)  ###############################################################
lenMsgPerSender, nbMsgPart, listPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup, nbHeart = zip(*sorted(zip(lenMsgPerSender, nbMsgPart, listPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup, nbHeart), reverse=False)) # Get a clean ranking
print("Plotting Fig. 7: length of msg by participants.")
matplotlib.rcParams['font.size'] = 16
plt.figure(figsize=(12+N/3., 9+N/4.))
plt.pie(lenMsgPerSender, labels=listPeople, autopct=makeAutopct(lenMsgPerSender), rotatelabels =True, shadow=False, labeldistance=1.02,  pctdistance=0.8, startangle=90)
plt.title("Participants of the conversation *by characters written* ("+firstMsgShort+" -> "+lastMsgShort+")\n            Total Length: "+str(lenMsg)+" characters")
plt.axis('equal')
plt.savefig("07-lenMsg.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(9)  ###############################################################
# This figure is special: it will show how often you start a message and how much "winds" you gave.
# A "wind" (ou vent in French) is when you ask a question and it stays without replies within 36h (*cries inside*).
# Warning: Data unreliable, especially if your friend replied in another way (SMS, directly, etc)
# So, don't start an argument from these data, thank you!
matplotlib.rcParams['font.size'] = 12
if (N != 0): # In fact, we can do that for any conversation!
  print("Plotting Fig. 8: conversation starters.")
  convStartedBySender, avgLengthPerSender, nbMsgPart, listPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, nbHeart = zip(*sorted(zip(convStartedBySender, avgLengthPerSender, nbMsgPart, listPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, nbHeart), reverse=False)) # Get a clean ranking
  fig = plt.figure(figsize=(18,9))
  ax = fig.add_subplot(1,2,1)
  ax.pie(convStartedBySender, labels=listPeople, rotatelabels =True, autopct=makeAutopct(convStartedBySender), startangle=90)
  plt.axis('equal')
  plt.title("Who sends the 1st message?\n       Total = "+str(sum(convStartedBySender))+" starts.")
  #plt.text(-1.2,-1.2,"One conversation 'starts' when there is a message sent after 36 hours without messages sent/received.", ha='center')
  # Not quite pertinent... 
  ax = fig.add_subplot(1,2,2)
  nbHeart, convStartedBySender, avgLengthPerSender, nbMsgPart, listPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup = zip(*sorted(zip(nbHeart, convStartedBySender, avgLengthPerSender, nbMsgPart, listPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup), reverse=False)) # Get a clean ranking
  ax.pie(nbHeart, labels=listPeople, autopct=makeAutopct(nbHeart), rotatelabels =True, startangle=90)
  plt.axis('equal')
  plt.title("How many hearts <3 ?\n       Total = "+str(sum(nbHeart)))
  plt.savefig("08-behaviorStats.png", dpi=100, bbox_inches='tight')
  plt.close()
else:
  print("Skipping Fig. 8: Suitable only if there is a F2F conversation.")
  removeFile("08-behaviorStats.png")
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(9)  ##############################################################
print("Plotting Fig. 9: average length of msg.")
avgLengthPerSender, nbMsgPart, listPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, nbHeart = zip(*sorted(zip(avgLengthPerSender, nbMsgPart, listPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, nbHeart), reverse=False)) # Get a clean ranking
plt.figure(figsize=(15,6+N/2.))
plt.grid(axis='x')
width = .8
plt.barh(listPeople, avgLengthPerSender, width, color='#00cc00')
for i in range(N2):
  plt.text(2, i, str(avgLengthPerSender[i]), ha='center',va='center')
plt.title("Average length of each message ("+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig("09-lengthOfMsg.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(10)  ##############################################################
print("Plotting Fig. 10: Length of long silences")
plt.figure(figsize=(12,10))
plt.grid(axis='y')
plt.plot(silenceArray[0][:1:-1], toDaysArray(silenceArray[1][:1:-1]))
plt.title("Length of silences (in days -- "+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig("10-lengthOfSilences.png", dpi=100, bbox_inches='tight')
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(11)  ##############################################################
if(sum(nbDuCoup) > 0):
  print("Plotting Fig. 11: Du coup...")
  nbDuCoup, avgLengthPerSender, nbMsgPart, listPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, nbHeart = zip(*sorted(zip(nbDuCoup, avgLengthPerSender, nbMsgPart, listPeople, reacSent, reacReceived, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, nbJe, nbTu, nbDuCoup, nbHeart), reverse=True)) # Get a clean ranking
  endList=N2-nbDuCoup.count(0) # We strip away zero values by setting the starting point of our graph
  plt.figure(figsize=(15, min(600, 8+endList/2)))
  plt.grid(axis='x')
  width = .8
  plt.barh(listPeople[:endList], nbDuCoup[:endList], width, color='#00dddd')
  for i in range(endList):
    plt.text(0.1*max(nbDuCoup), i, str(nbDuCoup[i]), ha='center',va='center')
  plt.title("Du coup, combien de 'Du coup'? ("+firstMsgShort+" -> "+lastMsgShort+")\nTotal = "+str(sum(nbDuCoup)))
  plt.savefig("11-duCoup.png", dpi=100, bbox_inches='tight')
  plt.close()
else:
  print("Skipping Fig. 11: No 'Du coup' said")
  removeFile("11-duCoup.png")  
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(12)  ##############################################################
#print("Plotting Fig. 12: About the last conversations")

###############################################################################
###############################################################################
# For further analysis: I will do a .csv file for comparing other conversations :) 
# TODO
sendToCsv()
try:
  if (sys.version_info[0] == 2):
    import jinja
  else:
    import jinja2 as jinja
  saveReportToHtml()
except ModuleNotFoundError:
  print("/!\ Jinja lib is not found. You should install it with 'pip install jinja' (no need to have admin rights)")

print("~ Analysis done with love in "+decimizeStr(times[-1]-times[0], 3)+" seconds! ~")
###### END OF PROGRAM ######
