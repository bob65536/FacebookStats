# Make stats for Facebook
# f: the file (wille be quickly closed anyway)
# content: variable storing f, line by line
# line: the variable content, but on one line
# j: JSON turned into dictionnary. Ready to be used!

from __future__ import division # For old dudes still with Python 2.7
import matplotlib
matplotlib.use('Agg') # When you use Python Shell 
import json
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as pltc
import time
#from random import sample
all_colors = [k for k,v in pltc.cnames.items()]
all_colors2=["steelblue","indianred","darkolivegreen","olive","darkseagreen","pink","tomato","orangered","darkslategrey","greenyellow","burlywood","mediumspringgreen","chartreuse","dimgray","black","springgreen","orange","darkslategray","brown","dodgerblue","peru","lawngreen","chocolate","crimson","forestgreen","darkgrey","cyan","mediumorchid","darkviolet","darkgray","darkgreen","darkturquoise","red","deeppink","darkmagenta","gold","hotpink","firebrick","steelblue","indianred","mistyrose","darkolivegreen","olive","darkseagreen","pink","tomato","orangered","darkslategrey","greenyellow","burlywood","seashell","mediumspringgreen","chartreuse","dimgray","black","springgreen","orange","darkslategray","brown","dodgerblue","peru","lawngreen","chocolate","crimson","forestgreen","darkgrey","cyan","mediumorchid","darkviolet","darkgray","darkgreen","darkturquoise","red","deeppink","darkmagenta","gold","hotpink","firebrick"]
times = [time.time()] # For debug: how long each graph takes to load?

####################
# User-editable variables - What you can edit, without looking for ages in the code
nbBins = 96                             # Subdiv per day Useful for Fig3. MUST be a multiple of 24 (24, 48, 72, ...)
startDate = dt.datetime(2000,9,1)       # When you want to start the stats. Good idea to take the last three months for example.
                                        # Format: dt.datetime(yyyy,m,d) - NO leading zeroes even if it is fancier with!
                                        # 
timeZoneStartTime = 1                   # 1 for UTC+01:00 (Winter time in France) (+1 if DST)
# Below this line: do NOT edit unless you know what you do!
####################
startTimeStamp = (startDate - dt.datetime(1970,01,01)).total_seconds()-timeZoneStartTime*3600

def mergeDicts(*dict_args):
  """
  Given any number of dicts, shallow copy and merge into a new dict,
  precedence goes to key value pairs in latter dicts.
  Adapted from https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression#26853961
  and https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python
  This function is a pain for the CPU...
  """
  res = []
  for dictionary in dict_args:
    for d in dictionary:
      res.append(d)
  # At that point, there may be duplicate entries in res
  res2 = []
  for d in res:
    if d not in res2:
      res2.append(d)
  return res2
  
# Opening and using the JSON file(s)
f = open("message.json",'r')
print("Opening the message.json file")
content = f.readlines() # Content of the whole file (but w/ newlines)
line = ""
f.close()
for i in range(len(content)):
  line += content[i]
j = json.loads(line)    # Now, we have a great thing that can be used :)
del content
del line
# Another file?
# EDIT: painfully slow. Should not be used.
try:
  f2 = open("message2.json",'r')
  print("Opening the message2.json file")
  content2 = f2.readlines()
  line2 = ""
  f2.close()
  for i in range(len(content2)):
    line2 += content2[i]
  j2 = json.loads(line2)
  del line2
  del content2
  j['messages'] = mergeDicts(j2['messages'],j['messages']) #Remember: the 1st element is the most recent
except IOError:
  # Ok, no other message file to merge!
  print("No other files to open!")
  
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
  return long(var*10**nb)//10**nb
 
def decimizeStr(var, nb):
  # Gives to var nb figures after the decimal point.
  return str(long(1.0*var*10**nb)/10**nb)
 
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
  return (decimizeStr(100.*n/N,1), decimizeStr(100.*(1-n/N)+.1,1), decimizeStr(100.*s/S,1))

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
  # hourMsg are dates under the form datetime.datetime(2001,31,3,3,4,1,10101)
  hr = [0]*24
  hrDetailed = [0]*nbBins # one segment every 15 min
  for h in hourMsg:
    hr[h.hour] += 1 # Increase the hth value of counter (msg between h:00 and h:59)
    hrDetailed[int((nbBins/24))*h.hour+h.minute//int(60*24/nbBins)]+= 1
  return hr, hrDetailed
 
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
  print(text)
  outFile.write(text.encode("ascii", "ignore")+'\n')
  
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
silenceArray = [] # Length of silences. Can be used to foresee a future interaction
convoTimeSpent = dt.timedelta(0,0) # (days, seconds)
# Reactions
nbReac = 0
nbMsgReac = 0
reacMean =["Love","Haha","Wow!","Sad ","Grrr"," +1 "," -1 ","Misc"]
reacHex  =["98 8d","98 86","98 ae","98 a2","98 a0","91 8d","91 8e","00 00"]
reacNb = [0]*8

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
        listPeople.append("UNKNOWN")
        nbMsgPart.append(1)
        reacReceivedPerSender.append([0]*8)
        reacSentPerActor.append([0]*8)
        hrPerSender.append([0]*24)
        lenMsgPerSender.append(getLenMsg(m))
        convStartedBySender.append(0)
        ignoredMessagesPerUser.append(0)
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
      occ += (keyword in m['content'].lower())
    nbJe[idUser] += min(1, occ)
    occ = 0
    for keyword in ["tu", "toi", "t'", "te"]:
      occ += (keyword in m['content'].lower())
    nbTu[idUser] += min(1, occ)
    nbDuCoup[idUser] += ("du coup" in m['content'].lower()) 
    
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
if(N==2):
  for i in range(1, nbMsg):
    a,b = hourMsg[i-1], hourMsg[i] # a is more recent than b ([0]: most recent)
    if (a-b > dt.timedelta(1,43200)): # There is more than 36h between two msgs
      idUser = listPeople.index(j['messages'][i-1]['sender_name']) # id of the guy who started the conv.
      convStartedBySender[idUser] += 1
      silenceArray.append(a-b)
      if ('?' in j['messages'][i]['content']):
        # Now, we had an unanswered question = Ignored :(
        idUser2 = listPeople.index(j['messages'][i]['sender_name']) # id of the guy poor ignored
        ignoredMessagesPerUser[idUser2] += 1
      else:
        True
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
nbMsgPart, listPeople, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup = zip(*sorted(zip(nbMsgPart, listPeople, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender, nbJe, nbTu, nbDuCoup), reverse=True)) # Get a clean ranking
msgPerDayX, msgPerDayY = nbDailyMsg(hourMsgD)
msgPerMonthX, msgPerMonthY = nbDailyMsg(hourMsgMo)

times.append(time.time())
# Display everything (or export them - up to you!)
textFile = open('Stats.txt','w')
print("####################")
if (typ=="RegularGroup"):
  printToFile("Stats of the conversation ["+name+"]:", textFile)
  printToFile("> Number of current participants: "+str(N) + ", plus "+str(N2-N)+" former participants.", textFile)
else:
  printToFile("Your interaction with "+name+":", textFile)
# Generic information
printToFile("> The 1st message has been written on "+firstMsg+" by "+nameFirst+".", textFile)
printToFile("> Last message saved: written on "+lastMsg+" by "+nameFirst+".", textFile)
printToFile("> Longest silence: "+str(silenceTime.days) +" days, "+str(silenceTime.seconds//3600)+" hours and "+str(decimize((silenceTime.seconds % 3600)/60.0,1))+" minutes.", textFile)
printToFile("> "+str(nbMsg)+" messages have been written, making an average of "+decimizeStr(1.0*nbMsg/(1.0*N), 2)+" messages per participant.", textFile)
Q1, Q2, Q3 = findQuarters(msgPerDayX, msgPerDayY) # Dates when quarters have been reached
printToFile("> Half of all messages have been written before/after "+str(Q2), textFile)
printToFile("> Messages are in average "+decimizeStr(lenMsg/nbMsg, 1)+" characters long.", textFile)
if (typ=="RegularGroup"): 
  # If there is more than two participants
  printToFile("> Among the "+str(nbMsgReac)+" messages with reactions ("+decimizeStr(100*nbMsgReac/nbMsg,1)+"%), participants have reacted "+str(nbReac)+" times ("+decimizeStr(nbReac/nbMsgReac, 2)+" times per message).", textFile)
  paretoRes = pareto(nbMsgPart)
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
    printToFile("> "+listPeople[0]+" talked about himself "+str(nbJe[0])+" times and about his friend "+str(nbTu[0])+" times (r="+decimizeStr(nbTu[0]/nbJe[0],2)+") and said 'Du coup' "+str(nbDuCoup[0])+" times.", textFile)
    printToFile("> "+listPeople[1]+" talked about himself "+str(nbJe[1])+" times and about his friend "+str(nbTu[1])+" times (r="+decimizeStr(nbTu[1]/nbJe[1],2)+") and said 'Du coup' "+str(nbDuCoup[1])+" times.", textFile)
  else:
    # Avoid a ZeroDivisionError: do not do the division by zero...
    printToFile("> "+listPeople[0]+" talked about himself "+str(nbJe[0])+" times and about his friend "+str(nbTu[0])+" times and said 'Du coup' "+str(nbDuCoup[0])+" times.", textFile)
    printToFile("> "+listPeople[1]+" talked about himself "+str(nbJe[1])+" times and about his friend "+str(nbTu[1])+" times and said 'Du coup' "+str(nbDuCoup[1])+" times.", textFile)
  printToFile("> Overall, "+totalSecondsToStr(convoTimeSpent.total_seconds())+" were spent on this conversation (plus passive participation).", textFile)
textFile.close()
times.append(time.time())
print("Process done in "+str(times[-1]-times[-2])+"+ sec")
### Graphes     ###############################################################
#plt.figure(1)  ###############################################################
print("Plotting Fig. 1: participants.")
plt.figure(figsize=(12+N/3., 9+N/4.))
plt.pie(nbMsgPart, labels=listPeople, autopct='%1.1f%%', shadow=False, startangle=90)
plt.axis('equal')
plt.title("Participants of the conversation ("+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig("01-participants.png", dpi=100)
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(2) ###############################################################
# Rule of thumb: for high vvalues (>360), prepare a good computer (720: 2GB of RAM + 60'' CPU time, 1440: 5GB + 90'' for the program alone)
hr=hourPost(hourMsg, nbBins)
print("Plotting Fig. 2: messages per hour.")
plt.figure(figsize=(12, 9))
plt.bar(np.arange(24), hr[0], width=1, alpha=.8, align='edge')
for (a,b) in zip(np.arange(24), hr[0]):
  if(b>0):
    plt.text(a+.02, b+1, str(b), fontsize=15, weight='bold')
plt.xticks(np.arange(0,24,1))    
plt.title("Hourly repartition of msgs ("+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig("02a-hourUseS.png", dpi=100)
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
  plt.text(a+(2*np.pi/24/2.), max(hr[0])*1.1, str(b), fontsize=20, color="red", weight='bold', ha='center',va='center')
ax.yaxis.grid(True)
plt.title("Hourly repartition of msgs ("+firstMsgShort+" -> "+lastMsgShort+" - radar graph)\nTotal = "+str(sum(hr[0]))+" msg!")
plt.savefig("02b-hourlyRadarGraph.png", dpi=100)
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(2quater) ##########################################################
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
      plt.text(a+(2*np.pi/24/2.), max(hrPerSender[i]), str(b), fontsize=10, color="black", weight='bold')
    ax.yaxis.grid(True)
    if(lenMsgPerSender[i]>0):
      plt.title("Hourly messages from "+listPeople[i]+"\nSum = "+str(sum(hrPerSender[i]))+" msg / Average length of msg: "+decimizeStr(lenMsgPerSender[i]/sum(hrPerSender[i]), 1)+" characters.")
    else: # Otherwise, you will have the exception ZeroDivisionError and you will kill a mathematician :(
      plt.title("Hourly messages from "+listPeople[i]+"\nSum = "+str(sum(hrPerSender[i]))+" msg")
  plt.savefig("02c-hourlyRadarGraphPerUser.png", dpi=100)
  plt.close()
else:
  print("Skipping Fig. 2ter: too many users...")
  with open("02c-hourlyRadarGraphPerUser.png",'w') as f: 
    f.write(" ") # Erase the figure, if it existed before
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
# Fig 3         ###############################################################
print("Plotting Fig. 3: messages per 1/4h.")
plt.figure(figsize=(24,9))
plt.bar(np.linspace(0,24-(24./nbBins),nbBins), hr[1], width=24.0/nbBins, alpha=.8, align='edge')
# 3rd argument: bin every x=.25 (for every 15 min)
# Example: np.linspace(0,23.75,96)
for (a,b) in zip(np.linspace(0,24-(24./nbBins),nbBins), hr[1]):
  if(b>0): # For better visibility, we hide values below 10
    plt.text(a, b+.5, str(b), fontsize=11)
plt.xticks(np.arange(0,24,1))  
plt.title("More accurate hourly repartition of msgs ("+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig("03a-hourUseL.png", dpi=100)
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(3bis) #############################################################
print("Plotting Fig. 3bis: precise radar graph for active hours.")
# Taken from SO #
fig = plt.figure(figsize=(12+nbBins/8,12+nbBins/8))
ax = fig.add_subplot(111,polar=True)
H = len(hr[1]) 
theta = np.arange(0, 2*np.pi, 2*np.pi/H) 
ax.set_theta_zero_location('S') # To start with 0 on the bottom, 12 on the top
bars = ax.bar(theta, hr[1], width=2*np.pi/H, align='edge') # Width = 2pi divided by nbr of bins (24)
ax.set_xticks(theta)
ax.set_xticklabels(np.linspace(0,24-(24./nbBins),nbBins), fontsize=10)
for (a,b) in zip(theta, hr[1]):
  plt.text(a+(2*np.pi/nbBins/3.), max(hr[1])*1.03, str(b), fontsize=14, color="red", weight='bold', ha='center',va='center')
ax.yaxis.grid(True)
plt.title("Hourly repartition of msgs  ("+firstMsgShort+" -> "+lastMsgShort+" - radar graph)\nTotal = "+str(sum(hr[0]))+" msg!")
plt.savefig("03b-preciseRadarGraph.png", dpi=100)
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(3ter) #############################################################
print("Plotting Fig. 3ter: stressing inactive moments.")
# Taken from SO #
fig = plt.figure(figsize=(min(48,12+nbBins/8),min(48,12+nbBins/8)))
ax = fig.add_subplot(111,polar=True)
H = len(hr[1]) 
theta = np.arange(0, 2*np.pi, 2*np.pi/H) 
ax.set_theta_zero_location('S') # To start with 0 on the bottom, 12 on the top
bars = ax.bar(theta, [min(hr[1][i],1) for i in range(nbBins)], width=2*np.pi/H, align='edge') # Width = 2pi divided by nbr of bins (24)
ax.set_xticks(theta)
ax.set_xticklabels(np.linspace(0,24-(24./nbBins),nbBins), fontsize=10)
ax.yaxis.grid(True)
plt.title("Number of empty bins (no message during moment): "+str(hr[1].count(0))+" empty bins out of "+str(nbBins)+".\nTotal = "+str(sum(hr[0]))+" msg!", fontsize=40)
plt.savefig("03c-emptyMoments.png", dpi=100)
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(4)  ###############################################################
print("Plotting Fig. 4: daily repartition of msg.")
plt.figure(figsize=(24,9))
for (a,b) in zip(msgPerDayX, msgPerDayY):
  if(b>0): # For better visibility, we hide values below 10
    plt.text(a, b+.5, str(b), fontsize=10, ha='center',va='center')
#plt.xticks(np.arange(msgPerDayX[0], msgPerDayX[-1],5))
Q1, Q2, Q3 = findQuarters(msgPerDayX, msgPerDayY) # Dates when quarters have been reached
# Plotting quarter labels (+text)
plt.plot([Q1, Q2, Q3], [0,0,0], 'rD')
plt.text(Q1,0,"1/4", fontsize=10, color='red')
plt.text(Q2,0,"1/2", fontsize=10, color='red')
plt.text(Q3,0,"3/4", fontsize=10, color='red')
plt.bar(msgPerDayX, msgPerDayY, width=1, alpha=.8)
plt.title("Daily repartition of msgs ("+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig("04-dateMsgDay.png", dpi=100)
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(5)  ###############################################################
print("Plotting Fig. 5: monthly repartition of msg.")
plt.figure(figsize=(12,12))
for (a,b) in zip(msgPerMonthX, msgPerMonthY):
  if(b>0): # For better visibility, we hide values below 1
    plt.text(a+dt.timedelta(days=7), b+3, str(b), fontsize=16, weight='bold')
#plt.xticks(np.arange(msgPerDayX[0], msgPerDayX[-1],5))
# Plotting quarter labels (+text)
plt.plot([Q1, Q2, Q3], [0,0,0], 'rD')
plt.text(Q1,0,"1/4", fontsize=10, color='red')
plt.text(Q2,0,"1/2", fontsize=10, color='red')
plt.text(Q3,0,"3/4", fontsize=10, color='red')
plt.bar(msgPerMonthX, msgPerMonthY, align='edge', width=31, alpha=1)
plt.title("Monthly repartition of msgs ("+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig("05-dateMsgMonth.png", dpi=100)
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(6) ###############################################################
print("Plotting Fig. 6: reactions sent.")
plt.figure(figsize=(15,6+N/2.))
colors=['#ff8888','#eeee00','#0000ff','#00eeee','#ff0000','#00cc00','#cc0000','#00cccc']
# Matplotlib bug: it sorts y axis by alphabetical order automatically, without sorting the other data :(
listPeople, nbMsgPart, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender = zip(*sorted(zip(listPeople, nbMsgPart, reacSentPerActor, reacReceivedPerSender, hrPerSender, lenMsgPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender), reverse=False)) # Get a clean ranking

width = .8
#plt.xticks(np.arange(msgPerDayX[0], msgPerDayX[-1],5))
y = []
p = []
offset = [0]*N2
for k in range(8): # For each reaction
  y.append([reacSentPerActor[i][k] for i in range(N2)])
  p.append([plt.barh(listPeople, y[k], width, color=colors[k], left=offset)])
  for i in range(len(y[0])): # For each person
    if(y[k][i]!=0): 
      plt.text(y[k][i]/2.+offset[i], i, y[k][i], ha='center',va='center')
  offset = addList(offset, y[k])
plt.legend([p[i][0] for i in range(8)], reacMean)
plt.title("Reactions sent by participant ("+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig("06-reacSent.png", dpi=100)
plt.close()  
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(7)  ###############################################################
if(N>2):
  print("Plotting Fig. 7: reactions received.")
  plt.figure(figsize=(15,6+N/2.))
  y = []
  p = []
  offset = [0]*N2
  for k in range(8):
    y.append([reacReceivedPerSender[i][k] for i in range(N2)])
    p.append([plt.barh(listPeople, y[k], width, color=colors[k], left=offset)])
    for i in range(len(y[0])): # For each participant
      if(y[k][i]!=0):
        plt.text(y[k][i]/2.+offset[i], i, y[k][i], ha='center',va='center')
    offset = addList(offset, y[k])
  plt.legend([p[i][0] for i in range(8)], reacMean)
  plt.title("Reactions received for participants ("+firstMsgShort+" -> "+lastMsgShort+")")
  plt.savefig("07-reacReceived.png", dpi=100)
  plt.close()
else:
  print("Skipping Fig. 7: duplicate with Fig6.")
  with open("07-reacReceived.png",'w') as f: 
    f.write(" ") # Erase the figure, if it existed before
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(8)  ###############################################################
#Restoring the older order
lenMsgPerSender, nbMsgPart, listPeople, reacSentPerActor, reacReceivedPerSender, hrPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender = zip(*sorted(zip(lenMsgPerSender, nbMsgPart, listPeople, reacSentPerActor, reacReceivedPerSender, hrPerSender, convStartedBySender, ignoredMessagesPerUser, avgLengthPerSender), reverse=True)) # Get a clean ranking
print("Plotting Fig. 8: length of msg by participants.")
plt.figure(figsize=(12+N/3., 9+N/4.))
plt.pie(lenMsgPerSender, labels=listPeople, autopct='%1.1f%%', shadow=False, startangle=90)
plt.title("Participants of the conversation *by characters written* ("+firstMsgShort+" -> "+lastMsgShort+")\nTotal Length: "+str(lenMsg)+" characters")
plt.axis('equal')
plt.savefig("08-lenMsg.png", dpi=100)
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(9)  ###############################################################
# This figure is special: it will show how often you start a message and how much "winds" you gave.
# A "wind" (ou vent in French) is when you ask a question and it stays without replies within 36h (*cries inside*).
# Warning: Data unreliable, especially if your friend replied in another way (SMS, directly, etc)
# So, don't start an argument from these data, thank you!
if (N == 2):
  print("Plotting Fig. 9: behaviors: starting and ignoring.")
  fig = plt.figure(figsize=(18,9))
  ax = fig.add_subplot(1,2,1)
  ax.pie(convStartedBySender, labels=listPeople, autopct='%1.1f%%', startangle=90)
  plt.axis('equal')
  plt.title("Who sends the 1st message?\nTotal = "+str(sum(convStartedBySender))+" starts.")
  ax = fig.add_subplot(1,2,2)
  ax.pie(ignoredMessagesPerUser, labels=listPeople, autopct='%1.1f%%', startangle=90)
  plt.axis('equal')
  plt.title("How many times your questions stay unanswered?\nTotal = "+str(sum(ignoredMessagesPerUser))+".")
  plt.savefig("09-behaviorStats.png", dpi=100)
  plt.close()
else:
  print("Skipping Fig. 9: Suitable only if there is a F2F conversation.")
  with open("09-behaviorStats.png",'w') as f: 
    f.write(" ") # Erase the figure, if it existed before
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(10)  ##############################################################
print("Plotting Fig. 10: average length of msg.")
plt.figure(figsize=(15,6+N/2.))
width = .8
plt.barh(listPeople, avgLengthPerSender, width, color='#00cc00')
plt.title("Average length of each message ("+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig("10-lengthOfMsg.png", dpi=100)
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
#plt.figure(11)  ##############################################################
print("Plotting Fig. 11: Length of long silences")
plt.figure(figsize=(12,10))
plt.plot(toDaysArray(silenceArray)[::-1])
plt.title("Length of silences (in days -- "+firstMsgShort+" -> "+lastMsgShort+")")
plt.savefig("11-lengthOfSilences.png", dpi=100)
plt.close()
times.append(time.time())
print("Fig done in "+str(times[-1]-times[-2])+"+ sec")
print("~ Analysis done with love in "+decimizeStr(times[-1]-times[0], 3)+" seconds! ~")
###### END OF PROGRAM ######
