import os, json, time, datetime
from .util import *
from .Discussion import *
from.Timer import * 
    
class DataStock:
    def __init__(self) -> None:
        self.discussionsList = []
        self.amountOfMessagesPerDay = {}
        self.wordsSaidAmount = {}
        self.wordsReceivedAmount = {}
        self.discussionsSizes = {}
        self.discussionsAges = {}
        self.sentMessagesDic = {f"{hour:02d}h": 0 for hour in range(24)}
        self.receivedMessagesDic = {f"{hour:02d}h": 0 for hour in range(24)}
        self.amountOfSentMessages = 0
        self.amountOfReceivedMessages = 0
        self.mostStableDiscussion = None
        self.mostAncientDiscussion = None
        self.biggestDiscussion = None
        

        self.searchJsonFiles()
        self.accountOwner = self.getAccountOwner()
    
    def getAccountOwner(self):
        possibilities = self.discussionsList[0].participants
        for discussion in self.discussionsList[1:]:
            for person in possibilities:
                if person not in discussion.participants:
                    possibilities.remove(person)
            if len(possibilities) == 1:
                return possibilities[0]["name"]

    def searchJsonFiles(self):
        inboxDirectories = getInboxDirectories()
        for inbox_directory in inboxDirectories:
            for root, dirs, files in os.walk(inbox_directory):
                dirName = os.path.basename(root)
                jsonList = []
                discussion = None
                for fileName in files[::-1]:
                    if fileName.endswith(".json"):
                        file_path = os.path.join(root, fileName)
                        jsonList.append(file_path)
                        with open(file_path, "r", encoding="utf-8") as file:
                            jsonData = json.load(file)
                            title = jsonData["title"].encode('latin1').decode('utf-8')
                            participants = jsonData["participants"]
                            if not discussion: discussion = Discussion(title, participants, dirName)
                            discussion.addMessagesFromList(title, jsonData["messages"])
                if discussion: self.addDiscussion(discussion)
    
    def loadData(self, fileManager, display=False):
      discussionAmount = len(self.discussionsList)
      timer = Timer()
      i, strlen=0, 0
      for discussion in self.discussionsList:
        i += 1
        fileManager.writeConversationFile(discussion, self.accountOwner)
        fileManager.generateCalendar(discussion)
        discussion.beginningTimeCode = discussion.messagesList[0].timecode
        self.discussionsSizes[discussion.title] = len(discussion.messagesList)
        self.discussionsAges[discussion.title] = discussion.beginningTimeCode

        for message in discussion.messagesList:
            self.treatMessage(message, discussion)

        updateDictFromDict(self.wordsSaidAmount, discussion.wordsSaidAmount)
        updateDictFromDict(self.wordsReceivedAmount, discussion.wordsReceivedAmount)

        if display:
            str = f"Chargement conversations: {i}/{discussionAmount} {discussion.title}"
            print(f"{str} {(strlen-len(str))*' '}", end='\r')
            strlen = len(str)
        
      self.getRecords()
      self.discussionsSizes = dict(sorted(self.discussionsSizes.items(), key=lambda item: item[1], reverse=True))
      self.discussionsAges = convertTimeStampDicToDates(self.discussionsAges)
      self.wordsSaidAmount = dict(sorted(self.wordsSaidAmount.items(), key=lambda item: item[1], reverse=True))
      self.wordsReceivedAmount = dict(sorted(self.wordsReceivedAmount.items(), key=lambda item: item[1], reverse=True))

      fileManager.writeAllFiles()
      
      if display:
        print(f"\nChargement termine: {timer.stop(2)}s")
    
    def treatMessage(self, message, discussion):
        updateDict(discussion.discussionSizePerDay, [datetime.datetime.fromtimestamp(message.timecode/1000).strftime("%d/%m/%Y")])
        if message.sender == self.accountOwner:
            updateDict(discussion.messagesAmount, ['self']) 
            self.amountOfSentMessages += 1
            self.sentMessagesDic[datetime.datetime.fromtimestamp(message.timecode/1000).strftime("%Hh")] += 1
            discussion.sentMessagesDic[datetime.datetime.fromtimestamp(message.timecode/1000).strftime("%Hh")] += 1
            updateDict(self.amountOfMessagesPerDay, [datetime.datetime.fromtimestamp(message.timecode/1000).strftime("%d/%m/%Y")])
            if message.isARealMessage:
                updateDict(discussion.wordsSaidAmount, message.content.split(" "))
                discussion.sizeOfMessages['sent'] += len(message)
        else:
            updateDict(discussion.messagesAmount, ['other']) 
            self.amountOfReceivedMessages += 1
            self.receivedMessagesDic[datetime.datetime.fromtimestamp(message.timecode/1000).strftime("%Hh")] += 1
            discussion.receivedMessagesDic[datetime.datetime.fromtimestamp(message.timecode/1000).strftime("%Hh")] += 1
            if message.isARealMessage:
                updateDict(discussion.wordsReceivedAmount, message.content.split(" "))
                discussion.sizeOfMessages['received'] += len(message)

    def addDiscussion(self, discussion: Discussion):
        self.discussionsList.append(discussion)
    
    def getDiscussionAmount(self):
        return len(self.discussionsList)
    
    def getRecords(self):
        biggestStreakName, biggestStreakAmount = self.discussionsList[0].title, self.discussionsList[0].biggestStreak
        oldestDiscussionName, oldestDiscussionValue = self.discussionsList[0].title, self.discussionsList[0].beginningTimeCode
        biggestDiscussionName, biggestDiscussionValue = self.discussionsList[0].title, len(self.discussionsList[0].messagesList)
        for discussion in self.discussionsList:
            if discussion.biggestStreak > biggestStreakAmount:
                biggestStreakName, biggestStreakAmount = discussion.title, discussion.biggestStreak
            if discussion.beginningTimeCode < oldestDiscussionValue:
                oldestDiscussionName, oldestDiscussionValue = discussion.title, discussion.beginningTimeCode
            if len(discussion.messagesList) > biggestDiscussionValue:
                biggestDiscussionName, biggestDiscussionValue = discussion.title, len(discussion.messagesList)

        self.mostStableDiscussion = (biggestStreakName, biggestStreakAmount)
        self.mostAncientDiscussion = (oldestDiscussionName, oldestDiscussionValue)
        self.biggestDiscussion = (biggestDiscussionName, biggestDiscussionValue)

    def printDiscussionNames(self):
        for discussion in self.discussionsList:
            print(discussion.title)
