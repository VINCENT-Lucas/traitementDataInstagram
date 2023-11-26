from pycode import *
import webbrowser


data = DataStock()
fileManager = FileManager(getCurrentDirPath(__file__), data)

data.loadData(fileManager, display=True)
webbrowser.open('index.html')

'''
New things to implement:
- Evolution of most active conversations throught time
- A best way to measure the "complicity score"

!! Bug ?    DataStock.loadData()
        These lines shouldn't be mandatory, but the dictionnaries are bound: 
            discussion.wordsSaidAmount.own = {}
            discussion.wordsSaidAmount.others = {}
'''
