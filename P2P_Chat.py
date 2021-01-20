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


    def __init__(self, friendName="Alice", yourName="Bob", title="Chat analysis"):
        """
        Define participants in this chat (you can overwrite placeholder names, with friendName, yourName and title)  
        ID will be useful for getting the author for WA mesages (field 'fromMe')
        """
        self.friend = Participant.Participant(friendName, 0)
        self.myself = Participant.Participant(yourName, 1)
        self.title = title

    def __str__(self):
        """Display a quick summary of the chat"""
        description = f"This P2P chat has two particpants: {self.friend.name} and you ({self.myself.name}).\n" + \
            f"The name of the report is [{self.title}]."
        return description

    def setNameChat(self, newName):
        self.title = newName
    
    def getLogsFB(self, logFileFB):
        """Extract logs from Messenger (logFileFB is a path)"""
        if sys.version_info[0] == 2: # For Python2 (discouraged)
            import io
            with io.open(logFileFB, 'r') as f:
                self.chatContent_json = json.load(f)
        else:
            with open(logFileFB, 'r', encoding=encoding) as f:
                self.chatContent_json = json.load(f)


    def getLogsWA(self, logFileWA):
        """Extract logs from WhatsApp (logFileWA is a path)"""
        pass

    pass