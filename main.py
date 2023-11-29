from pycode import *
import webbrowser

data = DataStock()

fileManager = FileManager(getCurrentDirPath(__file__), data)

data.loadData(fileManager, display=True)
webbrowser.open('index.html')

'''
New things to implement:
- Display the most active participant of every discussion ?
- Remove the Display class

Done:
- Generate the graph on the writeAllFiles() method
- Remove the perdios where no discussion were active on the graph
'''
