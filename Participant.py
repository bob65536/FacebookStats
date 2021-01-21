"""
Definition of class Participant
In this class, we will define all the attributes a participant has
(e.g. name, reactions sent/received, nb of messages, etc) 
"""

from Toolbox import *

# Global constants: Adjust them to your needs
numberBins = 96 # How many subdivisions in a day

class Participant:
    # Attributes (same value for all participants)
    # First 5: official types (on JSON). Next: I created them (cf categorizeMsg()). 
    possibleTypeMessagesFB = ["Generic", "Share", "Subscribe", "Unsubscribe", "Call", "Plan",
            "Photos", "Stickers", "GIF", "Videos", "Audio Msgs",
            "Files", "Links", "Calls", "Blank/Removed Msgs", "Waving",
            "Waving Back", "App used", "Adding someone", "Leave", "Kicking someone", 
            "Create poll", "Participate poll", "Change group photo", "Change nicknames", "Change group name",
            "Change chat colors", "Change emoji", "Group admin", "Plan", "Misc"]


    # Initializer
    def __init__(self, name, id):
        self.name = name
        self.id = id
        
        # Reactions (Facebook / Signal when implemented)
        self.reacReceived = {'Love': 0, 'Haha': 0, 'Wow': 0, 'Sad': 0, 'Grrr': 0, '+1': 0, '-1': 0, 'Misc': 0}
        self.reacSent = {'Love': 0, 'Haha': 0, 'Wow': 0, 'Sad': 0, 'Grrr': 0, '+1': 0, '-1': 0, 'Misc': 0}
        
        # Stats
        self.convStarted = 0
        self.ignoredMessages = 0

        # Stats determined by other data in this class
        self.averageLengthMessages = 0

        # Emoji and contents
        self.nbPronouns = {'Je': 0, 'Tu': 0, 'Du coup': 0}
        self.emojiUsed = {} # include the hearts in all kinds
        # Create dictionnary from list as attribute
        self.contentType = dict.fromkeys(self.possibleTypeMessagesFB, 0)

        # Number of messages
        self.nbTotalMessages = {'nbMessages': 0, 'nbWords': 0, 'nbCharacters': 0}
        self.nbMessagesHour = [0]*numberBins # Finite array
        self.nbMessagesDay = {} # With a dictionary, where each day is a key

        # Analysis per messages (big arrays!)
        self.timeToReply = []
        self.vaderAnalysis = []

    def __str__(self):
        """ Display all the information concerning the instance """
        return f"{self.name} has ID#{self.id}."


    pass