from code.utilitaries import *
from code.html import *

import datetime, time

''' On met à jour les compteurs de mots'''
def updateWordCounter(msg, username, wordCounterDic):
    if msg["sender_name"] == username and "content" in msg:
        content = msg["content"].encode('latin1').decode('utf-8')
        updateDict(wordCounterDic, content.split())
         
''' On met à jour le compteur de messages reçus à un certain horaire '''
def updateHoursCounter(msg, timeTableDic):
  hour = timeStampToHour(msg["timestamp_ms"])[:3]
  updateDict(timeTableDic, [hour])


''' Traite l'ensemble des données (fichiers json contenant les discussions) '''
def treatment(filesList, username, wordCounterDic, sentMsgTimeTableDic, receivedMsgTimeTableDic, amountOfParticipantsDic):
  for file_path in filesList:
    with open(file_path, "r", encoding="utf-8") as file:
      jsonData = json.load(file)
      conversationName = jsonData["title"].encode('latin1').decode('utf-8')
      messages = jsonData["messages"]

      amountOfParticipantsDic[conversationName] = len(jsonData["participants"])

      for msg in messages:
        updateWordCounter(msg, username, wordCounterDic)
        updateHoursCounter(msg, sentMsgTimeTableDic) if msg["sender_name"] == username else updateHoursCounter(msg, receivedMsgTimeTableDic)
        
   
''' Traitement de tous les fichiers associés à un utilisateur (par exemple messages1, messages2 et messages3 pour User1).
On prend en entrée la liste des json associés à un utilisateur unique.
'''
def ConversationTreatment(jsonList, conversationSizeDic, wordCounterDic, conversationAgeDic, dirName, userInfoDic, username, dirPaths, conversationMaxStreakDic, amountOfMessPerDayDic):
    orderedDiscussions = order_files(jsonList)
    convData = {"amountOfSentMsg":0, "amountOfReceivedMsg":0, "amountOfSentAns":0, "amountOfReceivedAns":0, "lastWhoTalked":None, 
    "timeBeforeAnswering":0, "timeBeforeGettingAnswered":0, "biggestStreak": 0, "sizeOfSentMessages": 0, "sizeOfReceivedMessages": 0,
    "lastSentMessageTime": 0, "lastReceivedMessageTime":0, "conversationName": ""}
    calendarList, daysList = [], []
    conversationWordCounter, hoursDic = {}, {}

    with open(os.path.join(dirPaths['Conversations'], dirName+'.html'), 'w', encoding="utf-8") as ConversationFile:
        ConversationFile.write(getHTMLConvHeader(convData["conversationName"]) + '\n<body>\n<div class="container">')
        
        for file_path in orderedDiscussions:
            with open(file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)

                # Extraction des informations
                convData["conversationName"] = json_data["title"].encode('latin1').decode('utf-8')
                messages = json_data["messages"]

                updateUserInfo(userInfoDic, dirName, convData["conversationName"])

                messagesTreatment(messages, ConversationFile, convData, calendarList, username, conversationAgeDic, conversationWordCounter, hoursDic, amountOfMessPerDayDic)
        ConversationFile.write("</div>\n</body>\n</html>")
    
    updateMessageAmount(conversationSizeDic, convData)
    calendarTreatment(calendarList, daysList)
    writeCalendar(daysList, os.path.join(dirPaths['Calendar'], dirName+'.html'), convData, nextDay, dirPaths, dirName)

    conversationMaxStreakDic[convData["conversationName"]] = convData["biggestStreak"]

    writeMostUsedWords(conversationWordCounter, wordCounterDic, os.path.join(dirPaths['Words'], dirName+'.html'), convData["conversationName"], dirName, dirPaths, hoursDic)

    writeDataConversation(dirName, convData, calendarList, dirPaths, username, hoursDic)
      

''' On effectue tous les traitements sur tous les messages.
C'EST ICI QU'ON ECRIT LES CONVERSATIONS.'''
def messagesTreatment(messages, ConvFile, convData, calendarList, username, conversationAge, conversationWordCounter, hoursDic, amountOfMessPerDayDic):
    conversationName = convData["conversationName"]
    min = 1000*time.time()
    ancientDate = None
    for msg in messages[::-1]:
      messageDate = convertTimestamp(datetime.datetime.fromtimestamp(msg["timestamp_ms"]/1000))
      txt = ''
      
      updateHoursCounter(msg, hoursDic)

      # On récupère le plus ancien message du fichier
      if msg["timestamp_ms"] < min:
        min = msg["timestamp_ms"]
      
      # On met à jour les statistiques
      if "content" in msg:
        calendarList.append(msg["timestamp_ms"])
        if msg["sender_name"] == username:
          updateDict(amountOfMessPerDayDic, [messageDate[:10]])
          updateDict(conversationWordCounter, msg["content"].encode('latin1').decode('utf-8').split(" "))
          convData["amountOfSentMsg"] += 1
          convData["sizeOfSentMessages"] += len(msg["content"])
          if convData["lastWhoTalked"] != msg["sender_name"] and convData["lastWhoTalked"] != None:
            convData["timeBeforeAnswering"] += msg["timestamp_ms"] - convData["lastReceivedMessageTime"] if convData["lastReceivedMessageTime"] != 0 else 0
            convData["amountOfSentAns"] += 1
          convData["lastSentMessageTime"] = msg["timestamp_ms"]
        else:
          convData["amountOfReceivedMsg"] += 1
          convData["sizeOfReceivedMessages"] += len(msg["content"])
          if convData["lastWhoTalked"] != msg["sender_name"] and convData["lastWhoTalked"] != None:
            convData["timeBeforeGettingAnswered"] += msg["timestamp_ms"] - convData["lastSentMessageTime"] if convData["lastSentMessageTime"] != 0 else 0
            convData["amountOfReceivedAns"] += 1
          convData["lastReceivedMessageTime"] = msg["timestamp_ms"]
        convData["lastWhoTalked"] = msg["sender_name"]

      # On crée la conversation dans le dossier Conversations
      if "content" in msg:
          # On ajoute une balise d'encrage si il s'agit d'un nouveau jour (balise accessible depuis le calendrier en suite.)
          anchor_tag = ''
          if not ancientDate or messageDate[:9] != ancientDate[:9]:
            anchor_tag = '<a id="' + str(messageDate)[:10] + '"></a>'  
          usr = "message user1" if msg["sender_name"] == username else "message user2"
          txt = f'<div class="{usr}">\n<span class="user">{msg["sender_name"].encode("latin1").decode("utf-8")}</span>\n<span class="timestamp">{messageDate}</span>\n<div class="text">{msg["content"].encode("latin1").decode("utf-8")}</div>\n</div>'
          ConvFile.write(anchor_tag + txt)
      
      ancientDate = messageDate

    # On actualise la valeur de l'âge de la conversation.
    if conversationName not in conversationAge or conversationAge[conversationName] > datetime.datetime.fromtimestamp(min/1000):
        conversationAge[conversationName] = datetime.datetime.fromtimestamp(min/1000)


''' Traitement de la liste, on extrait d'une liste de timecodes une liste de jours uniques '''
def calendarTreatment(calendarList, daysList):
  calendarList.sort()
  for timecode in calendarList:
    date = datetime.datetime.fromtimestamp(timecode/1000).strftime("%d/%m/%Y")
    if date not in daysList:
      daysList.append(date)

''' Calcule les scores de complicité de toutes les conversations '''
def computeComplicityScores(complicityScore, amountOfParticipantsDic, conversationAgeDic, conversationSizeDic, conversationMaxStreakDic):
   for key in conversationSizeDic:
      if amountOfParticipantsDic[key] == 2:
        complicityScore[key] = dateTimeToDays(conversationAgeDic[key]) * int((conversationSizeDic[key][0] * conversationSizeDic[key][1])**(1/4)) * conversationMaxStreakDic[key]
