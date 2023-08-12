import os, json
import datetime

# --------------------- OS ------------------------- #

# Récupère la liste des usernames d'une discussion.
def get_usernames(file_path):
  with open(file_path, "r", encoding="utf-8") as file:
    json_data = json.load(file)
    list = json_data["participants"]
    namesList = []
    for elem in list:
        namesList.append(elem["name"])
    return namesList

# Récupère le nom d'utilisateur du propriétaire du compte.
def get_self_username(inbox_directories):
    possibilities = []
    for inbox_directory in inbox_directories:
        for root, dirs, files in os.walk(inbox_directory):
                for file_name in files:
                    if file_name.endswith(".json"):
                        file_path = os.path.join(root, file_name)
                        usernames = get_usernames(file_path)
                        # On cherche l'intersection entre toutes les conversations (l'utilisateur qui apparaît toujours)
                        if possibilities == []:
                            possibilities = usernames
                        else:
                            possibilities = list(set(possibilities) & set(usernames))
                        
                        if len(possibilities) == 1:
                            return possibilities[0]
    print("Erreur: il est impossible de récupérer un userName.")
 
''' Trie les différents fichiers de conversations d'un seul utilisateur des plus récents aux plus anciens.'''
def order_files(jsonList):
    unSortedDict = {}
    for jsonPath in jsonList:
        with open(jsonPath, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            messages = json_data["messages"]
            last_message = messages[-1]
            time = last_message['timestamp_ms']
            unSortedDict[jsonPath] = time
    sorted_dict = dict(sorted(unSortedDict.items(), key=lambda x: x[0], reverse=True))
    return sorted_dict

# --------------------- Utilitaries ------------------

''' Trouve le chemin du dossier de ce fichier '''
def getCurrentDirPath(file):
    path = os.path.realpath(file)
    while path[-1] != '\\':
        path = path[:-1]
    return path

''' On associe à un nom de fichier le nom de la conversation.'''
def updateUserInfo(userInfo, fileName, conversationName):
    if fileName not in userInfo:
        userInfo[fileName] = conversationName

''' On actualise le compteur de messages pour chaque utilisateurs'''
def updateMessageAmount(messageAmountDic, convData):
    if convData["conversationName"] in messageAmountDic:
      messageAmountDic[convData["conversationName"]] = (messageAmountDic[convData["conversationName"]][0] + convData["amountOfSentMsg"],
      messageAmountDic[convData["conversationName"]][1] + convData["amountOfReceivedMsg"])
    else:
      messageAmountDic[convData["conversationName"]] = (convData["amountOfSentMsg"], convData["amountOfReceivedMsg"])

''' On convertit un nombre de ms en Jours, Heures, Minutes, Secondes'''
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

def extractDays(calendarList):
  daysList = []
  calendarList.sort()
  for timecode in calendarList:
    date = datetime.datetime.fromtimestamp(timecode/1000).strftime("%d/%m/%Y")
    daysList.append(date)
  return daysList

''' Trouve l'élément le plus présent dans une liste'''
def mostCommonElement(liste):
    compteurs = {}
    
    for element in liste:
      if element in compteurs:
        compteurs[element] += 1
      else:
        compteurs[element] = 1
    
    element_recurrent = None
    max_repetitions = 0
    
    for element, repetitions in compteurs.items():
      if repetitions > max_repetitions:
        element_recurrent = element
        max_repetitions = repetitions
    
    return element_recurrent, max_repetitions

''' Incrémentation d'une date sous forme de string via datetime'''
def nextDay(date_str):
  dateObj = datetime.datetime.strptime(date_str, '%d/%m/%Y')
  newDate = dateObj + datetime.timedelta(days=1)
  newDateStr = newDate.strftime('%d/%m/%Y')
  return newDateStr

''' Reformate une date au format JJ/MM/YYYY HH/MM'''
def convertTimestamp(dateTime):
    return dateTime.strftime("%d/%m/%Y, %Hh%M")

''' Convertit un dateTime en nombre de jours'''
def dateTimeToDays(dateTime):
  return int((datetime.datetime.now()-dateTime).days)

''' Renvoie l'heure associée à un timestamp, au format HH/MM '''
def timeStampToHour(timestamp):
    return datetime.datetime.fromtimestamp(timestamp/1000).strftime("%Hh%M")
  

''' Supprétion puis création des dossiers Conversations, Données'''
def create_dirs(path):
    dirPaths = {"Root": path}
    nameList = ["Conversations", "Données", "Calendar", "Menus", "Words"]
    for name in nameList:
      folder_path = os.path.join(path, name)
      if os.path.exists(folder_path):
          for file in os.listdir(folder_path):
              filePath = os.path.join(folder_path, file)
              if os.path.isfile(filePath):
                os.remove(filePath)
          os.rmdir(folder_path)
      os.makedirs(folder_path)
      dirPaths[name] = folder_path
    
    return dirPaths

# --------------------- Dictionnaires ------------------
'''Calcule la somme des valeurs d'un dictionnaire'''
def sumOfDict(dic):
  sum = 0
  for key, value in dic.items():
    sum += value
  return sum

''' Trie un dictionnaire par ordre décroissant de ses valeurs'''
def orderDic(dic, reversed=True):
   return dict(sorted(dic.items(), key=lambda x: x[1], reverse=reversed))

''' Trie un dictionnaire par rapport à ses clefs'''
def orderDicKeys(dic):
    return {k: dic[k] for k in sorted(dic.keys())}

''' Récupère la liste de tous les fichiers json de conversations. '''
def getAllConversationFiles(inbox_directories):
  jsonList = []
  for inbox_directory in inbox_directories:
    for root, dirs, files in os.walk(inbox_directory):
      for file_name in files:
          if file_name.endswith(".json"):
            file_path = os.path.join(root, file_name)
            jsonList.append(file_path)
  return jsonList

''' Convertit les clefs d'un dictionnaire en leur pourcentage '''
def dicToPercentageDic(dic):
  total = sumOfDict(dic)
  percentageDic = {}
  
  for key in dic:
    amountOfMessages = dic[key]
    percentageDic[key] = int(100*amountOfMessages/total)

  return percentageDic

''' Renvoie le maximal des valeurs d'un dictionnaire '''
def dicGetMaxValue(dic):
  return max(dic.values())

''' Renvoie le minimal des valeurs d'un dictionnaire '''
def dicGetMinValue(dic):
  return min(dic.values())

''' Renvoie la clef associée à la valeur max. d'un dictionnaire '''
def dicGetMaxKey(dic):
  max = dicGetMaxValue(dic)
  for key in dic:
     if dic[key] == max:
        return key

''' Renvoie la clef associée à la valeur min. d'un dictionnaire '''
def dicGetMinKey(dic):
  min = dicGetMinValue(dic)
  for key in dic:
     if dic[key] == min:
        return key

''' Stocke le nombre d'occurences d'éléments d'une liste dans un dictionnaire.'''
def updateDict(dict, list):
    for elem in list:
        if elem in dict:
            dict[elem] += 1
        else:
            dict[elem] = 1

''' Somme les valeurs des tuples de valeurs d'un dictionnaire '''
def mergeDic(dic):
  merged = {}
  for key in dic:
    merged[key] = dic[key][0] + dic[key][1]
  return merged

''' Renvoie la somme des i-emes valeurs des tuples d'un dictionnaire '''
def sumDicI(dic, i):
  sum = 0
  for key in dic:
    sum += dic[key][i]
  return sum
