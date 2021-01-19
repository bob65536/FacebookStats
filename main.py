"""
Main program.
"""

from Participant import *

user1 = Participant("John Smith", 1)

print(user1.nbTotalMessages['nbWords'])
print(user1.description())

print(user1)