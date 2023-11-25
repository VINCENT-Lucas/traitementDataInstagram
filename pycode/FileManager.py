import os, datetime
from .Calendar import *
from .Html import *
from .Display import *
from .WordFrequence import *
from .OrderedDict import *

class FileManager:
    def __init__(self, root, data) -> None:
        self.rootPath = root
        self.data = data
        dic = self.reCreateDirs()
        self.conversationsPath = dic['Convs']
        self.dataPath = dic['Données']
        self.calendarPath = dic['Calendrier']
        self.menusPath = dic['Menus']
        self.wordsPath = dic['Mots']

    def writeAllFiles(self):
      self.writeIndex()
      self.writeConvMenu()
      self.generateAccountData()
      self.generateRankingFile(self.menusPath, self.data.discussionsSizes, 'Top conversations.', 'messageCount')
      self.generateRankingFile(self.menusPath, self.data.discussionsAges, 'Plus anciennes conversations', 'convAge')
      self.generateRankingFile(self.menusPath, self.data.wordsSaidAmount, 'Mots les plus employés', 'wordCounter')
      for discussion in self.data.discussionsList:
        self.writeDataConversation(discussion)
        self.writeDiscMostUsedWords(discussion)

    def reCreateDirs(self):
      dirPaths = {}
      nameList = ["Convs", "Données", "Calendrier", "Menus", "Mots"]
      for name in nameList:
        folder_path = os.path.join(self.rootPath, name)
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                filePath = os.path.join(folder_path, file)
                if os.path.isfile(filePath):
                  os.remove(filePath)
            os.rmdir(folder_path)
        os.makedirs(folder_path)
        dirPaths[name] = folder_path
      
      return dirPaths

    def generateRankingFile(self, root, dictionary, title, fileName):
      count = 1
      with open(root + "\\"+ fileName + ".html", 'w', encoding="utf-8") as file:
        file.write(Html.getRankingHeader(title))
        for key in dictionary:
          htmlContent = f'    <div class="row">\n'
          htmlContent += f'        <div class="box">{count}</div>\n'
          htmlContent += f'        <div class="box">{key}</div>\n'
          htmlContent += f'        <div class="box">{dictionary[key]}</div>\n'
          htmlContent += f'    </div>\n'
          count += 1
          file.write(htmlContent)
        
        file.write("</body>\n</html>")

    def generateCalendar(self, discussion):
      daysList = []
      prevDate = None
      for message in discussion.messagesList:
          date = datetime.datetime.fromtimestamp(message.timecode/1000).strftime("%d/%m/%Y")
          if date != prevDate:
            daysList.append(date)
          prevDate = date
      calendar = Calendar()
      calendar.writeCalendar(daysList, discussion, self)
      discussion.biggestStreak = calendar.biggestStreak
    
    def generateAccountData(self):
      # Début de la construction du code HTML
      htmlCode = Html.getAccountDataHeader()

      htmlCode += '<body>\n'
      htmlCode += f'\t<header>\n<h1> {self.data.accountOwner} </h1>\n</header>\n'

      htmlCode += f'<div class="highlight"> Meilleure conversation: <span style="text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">{"None"}</span> ({"None"}☆)</div>\n'
      htmlCode += f'<div class="highlight"> Plus ancienne conversation: <span style="text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">{self.data.mostAncientDiscussion[0]}</span> ({(datetime.datetime.now() - datetime.datetime.fromtimestamp(self.data.mostAncientDiscussion[1]/1000)).days}j)</div>\n'
      htmlCode += f'<div class="highlight"> Plus longue conversation: <span style="text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">{self.data.biggestDiscussion[0]}</span> ({self.data.biggestDiscussion[1]} messages)</div>\n'
      htmlCode += f'<div class="highlight"> Conversation la plus stable: <span style="text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">{self.data.mostStableDiscussion[0]}</span> ({self.data.mostStableDiscussion[1]}j de conversation à la suite)</div>\n'

      htmlCode += f'<div class="highlight"> Nombre de messages envoyés: {self.data.amountOfSentMessages}</div>'
      htmlCode += f'<div class="highlight"> Nombre de messages reçus: {self.data.amountOfReceivedMessages}</div>'
      htmlCode += f'<div class="highlight"> Nombre de conversations: {len(self.data.discussionsList)}</div>'
      htmlCode += f'<div class="highlight"> Jour le plus actif: {max(self.data.amountOfMessagesPerDay, key=self.data.amountOfMessagesPerDay.get)}: {max(self.data.amountOfMessagesPerDay.values())} messages envoyés</div>'
      htmlCode += f'<div class="highlight"> Période la plus active de la journée: {max(self.data.sentMessagesDic, key=self.data.sentMessagesDic.get)} ({int(100*max(self.data.sentMessagesDic.values())/sum(self.data.sentMessagesDic.values()))}% des messages)</div>'

      # Ajout du titre
      htmlCode += '\t<header>\n<h1> Nombre de messages envoyés par heure. </h1>\n</header>\n'
      
      # Ajout d'un graphe
      htmlCode += Html.generateGraph(self.data.sentMessagesDic)

      htmlCode += '\t<header>\n<h1> Nombre de messages reçus par heure. </h1>\n</header>\n'
      htmlCode += Html.generateGraph(self.data.receivedMessagesDic)
      
      # Fin du body 
      htmlCode += '\n</body>'

      with open(os.path.join(self.menusPath, "accountData.html"), 'w', encoding="utf-8") as writingFile:
        writingFile.write(htmlCode)
  
    def writeConversationFile(self, discussion, accountOwner):
        display = Display()
        with open(os.path.join(self.conversationsPath, discussion.dirName + '.html'), 'w', encoding="utf-8") as ConversationFile:
            display.generateConversationHTML(discussion.dirName, discussion.messagesList, accountOwner, ConversationFile)

    def writeConvMenu(self):
      with open(f"{self.menusPath}\convMenu.html", 'w', encoding="utf-8") as file:
        file.write(Html.getConvMenuHeader())
        for discussion in self.data.discussionsList:
              button = f'<a href={os.path.join(self.dataPath, discussion.dirName +".html")} class="button">Détails</a>'
              file.write(f'<li><a href="{os.path.join(self.conversationsPath, discussion.dirName+".html")}">{discussion.title}</a>\n{button}</li>')

        file.write("</ul>\n</body>\n</html>")

    def writeIndex(self):
       with open(f"{self.rootPath}\index.html", 'w', encoding="utf-8") as indexFile:
        html = Html
        indexFile.write(html.getIndex(self))

    def writeDataConversation(self, discussion):
        with open(os.path.join(self.dataPath, discussion.dirName + '.html'), 'w', encoding="utf-8") as writingFile:

            msgSentAmount = discussion.messagesAmount['self']
            msgReceivedAmount = discussion.messagesAmount['other']
            listUser1 = [f"Nombre de messages envoyés: {msgSentAmount}."]
            listUser2 = [f"Nombre de messages envoyés: {msgReceivedAmount}."]

            meanAnsLength = discussion.sizeOfMessages['sent']/msgSentAmount if msgSentAmount != 0 else 0
            listUser1.append(f"Taille moyenne des messages: {int(meanAnsLength)} caractères.")
            meanAnsLength = discussion.sizeOfMessages['received']/msgReceivedAmount if msgReceivedAmount !=0 else 0
            listUser2.append(f"Taille moyenne des messages: {int(meanAnsLength)} caractères.")

            listGlobal = []
            mostActiveDay, messageAmount = max(discussion.discussionSizePerDay, key=discussion.discussionSizePerDay.get), max(discussion.discussionSizePerDay.values())
            if mostActiveDay:
                listGlobal.append(f"Jour de la plus longue discussion: {mostActiveDay}: {messageAmount} messages.")
            else:
                listGlobal.append(f"Jour de la plus longue discussion: Aucun.")
            
            listGlobal.append(f"Plus grande période de conversation: {discussion.biggestStreak} jours.\n")
            writingFile.write(Html.dataGetHeader() + f'<body>\n<header>\n\t<h1>Données de conversation: {discussion.title}</h1>\n</header>\n')
        
            # Partie user1
            txt = f'<div class="container">\n<div class="column">\n<h2>{self.data.accountOwner}</h2>\n<ul>\n'
            for line in listUser1:
                txt += f'<li>{line}</li>\n'
            txt += '</ul>\n</div>\n'
            writingFile.write(txt)

            # Partie user2
            txt = f'<div class="column">\n<h2>{discussion.title}</h2>\n<ul>\n'
            for line in listUser2:
                txt += f'<li>{line}</li>\n'
            txt += '</ul>\n</div>\n</div>\n'
            writingFile.write(txt)

            # Partie globale
            txt = '<div class="container">\n<div class="column">\n<ul>\n'
            for line in listGlobal:
                txt += f'<li>{line}</li>\n'
            txt += '</ul>\n</div>\n</div>\n'
            writingFile.write(txt)

            txt = '<div class="button-container">\n'
            txt += f'\t<a href="{os.path.join(self.calendarPath, discussion.dirName + ".html")}" class="button">Voir le calendrier</a>\n'
            txt += f'\t<a href="{os.path.join(self.wordsPath, discussion.dirName+".html")}" class="button">Mots les plus utilisés</a>\n</div>\n'

            txt += '\n<header>\n<h1>Répartition des messages</h1>\n</header>\n'
            txt += Html.generateGraph(updateDictFromDict(discussion.sentMessagesDic, discussion.receivedMessagesDic))

            txt += "</body>\n</html>"
            writingFile.write(txt)

    def writeDiscMostUsedWords(self, discussion):
        orderedDict = OrderedDict(length=50)
        cSize = sumOfDict(discussion.wordsSaidAmount)
        for word, quantity in discussion.wordsSaidAmount.items():
            wordFreq = WordFrequence(word, quantity, self.data.wordsSaidAmount[word], cSize, self.data.sumOfWordsSaid)
            wordWeight = wordFreq.getWeight()
            orderedDict.add(word, wordWeight)
        
        dic = {}
        for key in orderedDict.getDict():
          quantity = discussion.wordsSaidAmount[key]
          wf = WordFrequence(key, quantity, self.data.wordsSaidAmount[key], cSize, self.data.sumOfWordsSaid)
          dic[key] = f"{wf.convPercentage():.2f}%, *{wf.convCoeff():.2f}"

        self.generateRankingFile(self.wordsPath, dic, f"{discussion.title}: Mots les plus représentatifs", discussion.dirName)
       
