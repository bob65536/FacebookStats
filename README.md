# Facebook_Stats
Do you want to make stats about your conversations with your friends on Messenger? I have what you need!

Step 1: Request a copy of your data (https://www.facebook.com/settings?tab=your_facebook_information).  
Step 2: Select the date range you wish (All of my data is great but can take more time).  
Step 3: Important: Use JSON as the format of your data. Otherwise, the program would be useless. The quality of the media does not matter here (high would take more time).   
Step 4: Wait until the archive is available (this can take between one and fifteen days).  

After that, for this version, you need to put the Python program and the message log (file called "message.json") on the same directory.   
This program is both compatible with Python 2.7 and Python 3.   
To run the program: 

Step 1: Retrieve the file message.json created by Facebook, when you request your data (unzip the archive).  
Typically, you will find it on: *\[Download Folder]/facebook-\[yourUsernameId]/messages/inbox/\[yourFriend]*. Copy this file where the program is located (usually, it is on the same place as this readme).  
Note: If you have several message.json files to merge, use jsonMerger.py as shown in my other project: https://github.com/bob65536/JsonMerger . Don't forget to place the files on the same directory as the program makeStats.  
Step 2: Be sure to have on the same directory the **"html" folder**, **makeStats.py** and **messages.json**. Go to this folder.  
Step 3: Run the script: `python makeStats.py` and wait. Usually, it takes between 5 and 120 seconds.  

The results can be found on `./resAnalysis/stats.html`. If you wish to save the report, either export it on PDF or save the folders *html* and *resAnalysis*. Otherwise, pictures won't show.  

Note (not important) about the authors: I am not a master in GitHub (yet!) so different names appear: Easley is the name of my computer and Bob Sleigh is a nickname. Both (and bob65536) are the same person.  

More information will be provided later.
