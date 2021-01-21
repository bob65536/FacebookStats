"""
Python Toolbox.
All the functions you need are here! 
"""

import datetime as dt
import pytz

# General Settings used in the whole project
encoding = 'latin1'                     # If there are accents (for French people), this encoding works fine. 
decoding = 'utf-8'                      # To interpret accent words from json, use this: u'\xc3\x89'.encode('latin1').decode('utf-8')

### Utilities ###

def sumTwoLists(L1, L2):
    """
    Sums values of each member of a list
    e.g. [1, 2, 3] , [1, 2, 3] -> [2, 4, 6]
    """
    if (len(L1) == len(L2)):
        N = len(L1)
        res = [0]*N
        for i in range(N):
            res[i] = L1[i]+L2[i]
        return res
    else:
        print("ERROR: arguments do not have same length!")

def divideList(listToDivide, denominator):
    """Divide every term of listToDivide by denominator  
    e.g. [10, 20, 25], 10 -> [1, 2, 2.5]"""
    # For multiplying, divide by 1/denominator.
    if (denominator == 0):
        print("WARN: DIV/0. List will not be changed.")
        denominator = 1
    return [(itemInList * 1.0 / denominator) for itemInList in listToDivide]

### Handling strings and displaying info ###

def prettyTxt(msg):
    """Correct the unicode text to interpret accents properly"""
    return msg.encode(encoding).decode(decoding)

def roundToN_str(var, N):
    """Return a string where var is rounded to N figures after decimal point."""
    return str(round(var, N))

def roundToN_list(listToRound, N):
    """Return a list where all vars in listToRound are rounded to N figures after decimal point."""
    return [round(var, N) for var in listToRound]

### Time handling ###

def TZtoTimestamp_ms(TZdata):
    """Convert data in TZ format ("2020-03-14T15:09:26Z") into timestamp in milliseconds (1584194966000)"""
    dtFormat = dt.datetime.strptime(TZdata,"%Y-%m-%dT%H:%M:%SZ") 
    timestamp_ms = dt.datetime.timestamp(dtFormat)
    return int(timestamp_ms * 1000)


def isDST(date=None, timezone="Europe/Paris"):
    """ Tells if date is on DST or not """
    if date is None:
        date = dt.datetime.utcnow()
    timezone = pytz.timezone(timezone)
    timezone_aware_date = timezone.localize(date, is_dst=None)
    return timezone_aware_date.tzinfo._dst.seconds != 0


def getUTCOffset(date):
    """ Get timezone for any date (available for continental France! Change it below if not the case) """
    if isDST(date, "Europe/Paris"):
        return 2
    else:
        return 1


### For Matplotlib and plotting nice figures ###

def makeSubplot(N):
    """
        Divide subplots into an optimized grid  
        in: N: number of subplots  
        out: (y,x) where x is the number of graphs in X axis and y in Y axis 
    """
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

# Extracting data
def getListPeople(data):
    """Get list of participants in a FB conversation (returns a list containing all names)"""
    ppl=[]
    for person in data['participants']:
        ppl += [person['name']]
    return ppl