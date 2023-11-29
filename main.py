from pycode import *
import webbrowser

data = DataStock()

fileManager = FileManager(getCurrentDirPath(__file__), data)

data.loadData(fileManager, display=True)
webbrowser.open('index.html')

'''
New things to implement:
- Display the most active participant of every discussion
- Show some messages sent (or voice messages ?) and you have to guess on which discussion they have been sent

Implemented stuff: 
- Added the amount of reels sent
- Changed all colors
'''
