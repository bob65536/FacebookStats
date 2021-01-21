"""
Definition of class P2P_Chat (PersonToPerson chat)
In this class, we will define all the attributes a person-to-person chat has
(e.g. name of the partner, title, range of date, etc) 

Terminology: 
- Each instance of P2PChat is a *chat*: there is only one chat between two participants.
- In a chat, there can be 0 to N conversations: a *conversation* is a sequence of messages
in which two consecutive messages was sent at most within [timeoutConversation_s] seconds (default: 1 day).
- A *message* is a content sent, let it be text, image, video or link; and sent to receiver. 
There can be several messages sent successively (to improve readability, to add content, etc). 
- Silence moments are moments between conversations.
- A conversation is *active* (and counted in *activity time*) when two consecutive messages are sent
at most within [timeoutActivity_s] seconds (default: 5 minutes).
"""

import Participant
from Toolbox import *
import sys
import json

class P2PChat():
    """
    Class with objects to interest for FaceToFace chats
    """

    # Attributes (same value for all chats)
    #: Time before considering a conversation over (in sec)
    timeoutConversation_s = 86400
    #: Time after sending a message before being considered as inactive (in sec)
    timeoutActivity_s = 300

    #: When to start and end the analysis
    startTimeStamp = dt.datetime(2000,1,1)
    endTimeStamp = dt.datetime(2099,1,1)

    def __init__(self):
        """
        Define participants in this chat (you can overwrite placeholder names, with friendName, yourName and title)  
        ID will be useful for getting the author for WA mesages (field 'fromMe')
        """
        self.friend = Participant.Participant("Alice", 0)
        self.myself = Participant.Participant("Bob", 1)
        self.title = "A great chat: analysis"
        self.totalActiveTime_s = 0 # Time spent on chat (in sec)

    # def __str__(self):
    #     """Display a quick summary of the chat"""
    #     description = f"This P2P chat has two particpants: {self.friend.name} and you ({self.myself.name}).\n" + \
    #         f"The name of the report is [{self.title}]."
    #     return description


    def setNameChat(self, newName):
        self.title = newName

    def getLogsFB(self, logFileFB):
        """Extract logs from Messenger (logFileFB is a path)"""
        if sys.version_info[0] == 2: # For Python2 (discouraged)
            import io
            with io.open(logFileFB, 'r') as f:
                self.fbChatContent_json = json.load(f)
        else:
            with open(logFileFB, 'r', encoding=encoding) as f:
                self.fbChatContent_json = json.load(f)
        
        # Extract data (do it in another function)
        # self.loadJsonDataFB()


    def loadJsonDataFB(self):
        """ Fetch data from json file. Run this after getLogsFB (for group conversations) """
        self.nameChatFB = self.fbChatContent_json['title']
        self.numberParticipants = len(self.fbChatContent_json['participants'])
        self.listParticipants = getListPeople(self.fbChatContent_json)
        self.totalNumberMessages = len(self.fbChatContent_json['messages'])
        # self.typeOfChat = self.fbChatContent_json['thread_type'] # Regular (this case) or RegularGroup
        if (self.numberParticipants == 2):
            # We are in a F2F chat. Overwrite names.
            self.friend.name = self.fbChatContent_json['participants'][0]
            self.myself.name = self.fbChatContent_json['participants'][1]
        messageToPrint = f"JSON loading done. \n\
    > Chat name: {self.nameChatFB}\n\
    > Nb of participants: {self.numberParticipants}: {self.listParticipants}\n\
    > Nb of messages: {self.totalNumberMessages}."
        print(messageToPrint) # Do it for debug

    def doTheAnalysisFB(self):
        """ Go through each message to do the analysis """
        for m in self.fbChatContent_json['messages']:
            break # WIP



    def getLogsWA(self, logFileWA):
        """Extract logs from WhatsApp (logFileWA is a path)"""
        pass

    pass