import os, datetime

def timestampToDate(timestamp):
    return datetime.datetime.fromtimestamp(timestamp/1000).strftime("%d/%m/%Y")

''' Stocke le nombre d'occurences d'éléments d'une liste dans un dictionnaire.'''
def updateDict(dict, list: list):
    for elem in list:
        if elem in dict:
            dict[elem] += 1
        else:
            dict[elem] = 1
    return dict

def updateDictFromDict(dict, dict2: dict):
    for key in dict2:
        if key in dict:
            dict[key] += dict2[key]
        else:
            dict[key] = dict2[key]
    return dict

def generateRatio(globalCounterDic, convCounterDic):
  finalDic = {}
  for key in convCounterDic:
    if key not in globalCounterDic or globalCounterDic[key] == convCounterDic[key]:
      finalDic[key] = 0
    else:
      finalDic[key] = (convCounterDic[key]/globalCounterDic[key])
  
  return dict(sorted(finalDic.items(), key=lambda item: item[1], reverse=True))

def getCurrentDirPath(file):
    path = os.path.realpath(file)
    while path[-1] != '\\':
        path = path[:-1]
    return path

def sumOfDict(dic):
  sum = 0
  for key, value in dic.items():
    sum += value
  return sum

def dicToPercentageDic(dic):
  total = sumOfDict(dic)
  percentageDic = {}
  
  for key in dic:
    amountOfMessages = dic[key]
    percentageDic[key] = int(100*amountOfMessages/total)

  return percentageDic

def convertTimeStampDicToDates(timeStampDic):
  timeStampDic = dict(sorted(timeStampDic.items(), key=lambda item: item[1]))
  for key in timeStampDic:
    timeStampDic[key] = timestampToDate(timeStampDic[key])
  return timeStampDic

def msToTime(ms):
  sec = ms//1000

  days = sec // (24 * 3600)
  remaining_sec = sec % (24 * 3600)

  hours = remaining_sec // 3600
  remaining_sec %= 3600

  minutes = remaining_sec // 60
  remaining_sec %= 60

  seconds = remaining_sec

  output = ""
  if days != 0:
    output += f"{int(days)} jours, "
  if hours != 0:
    output += f"{int(hours)} heures, "
  if minutes != 0:
    output += f"{int(minutes)} minutes, "
  if seconds != 0:
    output += f"{int(seconds)} secondes, "
  return output[:-2]

def getInboxDirectories():
        inbox_directories = []
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for root, dirs, files in os.walk(path):
            if "inbox" in dirs:
                inbox_directory = os.path.join(root, "inbox")
                inbox_directories.append(inbox_directory)
        return inbox_directories