from pycode import *

data = DataStock()

fileManager = FileManager(getCurrentDirPath(__file__), data)
data.loadData(fileManager, display=True)
#data.printDiscussionNames()
