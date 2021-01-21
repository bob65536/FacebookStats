"""
Main program. 
"""

import Participant
import P2P_Chat
from Toolbox import *

# Create an instance with the chat in question
# TODO Add path to logs
path = "/media/lovelace/HDD1_Secret/Backup/Messages/Facebook/2020/messages/inbox/botdepersyl_uononcp4xa/message_1.json"
chatToAnalysis = P2P_Chat.P2PChat()

# Just to give a fancy name!
chatToAnalysis.setNameChat(f"My chat with {chatToAnalysis.friend.name}: Analysis")

# Load FB archive
chatToAnalysis.getLogsFB(path)
chatToAnalysis.loadJsonDataFB()
chatToAnalysis.doTheAnalysisFB()
# test
print(chatToAnalysis.numberParticipants)

