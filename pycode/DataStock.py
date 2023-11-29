import os, json, time, datetime
from .util import *
from .Discussion import *
from.Timer import * 
from .Emoji import *
from .SelfOtherDic import *

''' The class that stores all the data of an Instagram account '''
class DataStock:
    def __init__(self) -> None:
        self.discussionsList = []
        
        self.wordsSaidAmount = SelfOtherDic()
        self.sentMessagesDic = SelfOtherDic({f"{hour:02d}h": 0 for hour in range(24)}, {f"{hour:02d}h": 0 for hour in range(24)})
        
        self.emojisDic = {}
        self.amountOfMessagesPerDay = {}
        self.discussionsSizes = {}
        self.discussionsAges = {}
        self.amountOfSentMessages = {'self': 0, 'other': 0}
        self.bestFriend = {}

        self.sumOfWordsSaid = 0
        self.mostStableDiscussion = None
        self.mostAncientDiscussion = None
        self.biggestDiscussion = None
        
        self.searchJsonFiles()
        self.accountOwner = self.getAccountOwner()

    ''' Navigates through all the discussions of the DataStock to find the userName of the account owner '''   
    def getAccountOwner(self):
        if len(self.discussionsList) == 0:
            print("Pas de discussions détectées")
        possibilities = self.discussionsList[0].participants
        for discussion in self.discussionsList[1:]:
            for person in possibilities:
                if person not in discussion.participants:
                    possibilities.remove(person)
            if len(possibilities) == 1:
                return possibilities[0]["name"]

    ''' Navigates through all the files of the root directory and reads the datas from all json files '''
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
    
    ''' Navigates through all the discussions to extract the data '''
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
        
        self.wordsSaidAmount.addAll('self', discussion.wordsSaidAmount.own)

        discussion.computeComplicityScore()
        if self.bestFriend == {} or list(self.bestFriend.values())[0] < discussion.complicityScore:
            self.bestFriend = {discussion.title: discussion.complicityScore}
        
        if display:
            str = f"Chargement conversations: {i}/{discussionAmount} {discussion.title}"
            print(f"{str}  {(strlen-len(str))*' '}", end='\r')
            strlen = len(str)
        
      self.getRecords()
      self.discussionsSizes = dict(sorted(self.discussionsSizes.items(), key=lambda item: item[1], reverse=True))
      self.discussionsAges = convertTimeStampDicToDates(self.discussionsAges)
      
      self.sumOfWordsSaid = sumOfDict(self.wordsSaidAmount.own)
      self.wordsSaidAmount.sort()
      self.emojisDic = dict(sorted(self.emojisDic.items(), key=lambda item: item[1], reverse=True))

      fileManager.writeAllFiles()
      
      if display:
        print(f"\nChargement termine: {timer.stop(2)}s")
    
    ''' Stores the data of a given message '''
    def treatMessage(self, message, discussion):
        updateDict(discussion.discussionSizePerDay, [datetime.datetime.fromtimestamp(message.timecode/1000).strftime("%d/%m/%Y")])
        emoji = Emoji()
        if message.sender == self.accountOwner:
            user, verb = 'self', 'sent'
            updateDict(self.amountOfMessagesPerDay, [datetime.datetime.fromtimestamp(message.timecode/1000).strftime("%d/%m/%Y")])
        else:
            user, verb = 'other', 'received'
        self.sentMessagesDic.add(user, datetime.datetime.fromtimestamp(message.timecode/1000).strftime("%Hh"))
        discussion.sentMessagesDic.add(user, datetime.datetime.fromtimestamp(message.timecode/1000).strftime("%Hh"))
        updateDict(discussion.messagesAmount, [user])
        self.amountOfSentMessages[user] += 1

        if message.isARealMessage:
            if message.share:
                discussion.sharedContent[user] += 1
            else:
                for word in message.content.split(" "):
                    discussion.wordsSaidAmount.add(user, word)
                    for letter in word:
                        if emoji.isEmoji(letter):
                            discussion.emojisDic.add(user, letter)
                            if user == 'self':
                                updateDict(self.emojisDic, [letter])
                discussion.sizeOfMessages[verb] += len(message)

    ''' Adds a discussion to the discussions list'''
    def addDiscussion(self, discussion: Discussion):
        self.discussionsList.append(discussion)
    
    ''' Returns the length of the discussion list '''
    def getDiscussionAmount(self):
        return len(self.discussionsList)
    
    ''' Updates all the records of the discussions '''
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

