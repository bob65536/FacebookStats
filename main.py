"""
Main program. 
"""

import Participant
import P2P_Chat
from Toolbox import *

# Create an instance with the chat in question
# TODO Add path to logs
chatToAnalysis = P2P_Chat.P2PChat()

# Just to give a fancy name!
chatToAnalysis.setNameChat(f"My chat with {chatToAnalysis.friend.name}: Analysis")

# test
print(chatToAnalysis)

