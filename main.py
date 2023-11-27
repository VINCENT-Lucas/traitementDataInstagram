from pycode import *
import webbrowser

data = DataStock()

fileManager = FileManager(getCurrentDirPath(__file__), data)

data.loadData(fileManager, display=True)
webbrowser.open('index.html')

timeZone = TimeZones(data, fileManager)
timeZone.writeTimeZones()
'''
New things to implement:
- Evolution of most active conversations throught time: reduce the amount of months if it's too big
'''
