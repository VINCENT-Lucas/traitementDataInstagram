from .util import *
from .Message import *
from .SelfOtherDic import * 
import math

class Discussion:
    def __init__(self, discussionName, participants, dirName) -> None:
        self.title = discussionName
        self.dirName = dirName
        self.biggestStreak = 0
        self.participants = participants
        self.messagesList = []
        self.messagesAmount = {'self': 0, 'other':0}
        self.emojisDic = SelfOtherDic()
        self.wordsSaidAmount = SelfOtherDic()
        self.sentMessagesDic = SelfOtherDic({f"{hour:02d}h": 0 for hour in range(24)}, {f"{hour:02d}h": 0 for hour in range(24)})
        self.answers = {'self': 0, 'other': 0}
        self.timeBeforeAnswer = {'self': 0, 'other': 0}
        self.biggestStreak = 0
        self.sizeOfMessages = {'sent':0, 'received': 0}
        self.discussionSizePerDay = {}
        self.beginningTimeCode = None
        self.complicityScore = 0

    def __len__(self):
        return len(self.messagesList)

    def computeComplicityScore(self):
        timecodeDate = datetime.datetime.strptime(timestampToDate(self.beginningTimeCode), "%d/%m/%Y")
        convAge = (datetime.datetime.now() - timecodeDate).days
        self.complicityScore = int(math.sqrt(convAge**2 * self.messagesAmount['self'] * self.messagesAmount['other']) / (1000*len(self.participants)**2))

    def addMessagesFromList(self, discussionTitle: str, messagesList: dict):
        for message in messagesList[::-1]:
            senderName = message['sender_name'].encode("latin1").decode("utf-8") 
            timestamp = message['timestamp_ms']
            content = message['content'].encode('latin1').decode('utf-8') if 'content' in message else 'Message Vocal' if 'audio_files' in message else 'Image'
            msgObject = Message(senderName, timestamp, discussionTitle, content, 'content' in message)
            self.addMessage(msgObject)

    def getParticipantsAmount(self):
        return len(self.participants)

    def addMessage(self, message):
        self.messagesList.append(message)
    
    def getMessageAmount(self, participantName):
        messAmount = 0
        for message in self.messagesList:
            if message.getSender() == participantName:
                messAmount += 1
        return messAmount
    
    def generateMessagesAmount(self):
        messagesAmount = {}
        for personName in self.participants:
            messagesAmount[personName] = self.getMessageAmount(personName)
        self.messagesAmount = messagesAmount
    

