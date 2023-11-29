from .util import *
from .Message import *
from .SelfOtherDic import * 
import math

''' The class that stores all the data for an Instagram discussion '''
class Discussion:
    def __init__(self, discussionName, participants, dirName) -> None:
        self.title = discussionName
        self.dirName = dirName
        self.biggestStreak = 0
        self.participants = participants
        self.messagesList = []
        self.messagesAmount = {'self': 0, 'other':0}
        self.emojisDic = SelfOtherDic()
        self.sharedContent = {'self': 0, 'other':0}
        self.wordsSaidAmount = SelfOtherDic()
        self.sentMessagesDic = SelfOtherDic({f"{hour:02d}h": 0 for hour in range(24)}, {f"{hour:02d}h": 0 for hour in range(24)})
        self.answers = {'self': 0, 'other': 0}
        self.timeBeforeAnswer = {'self': 0, 'other': 0}
        self.biggestStreak = 0
        self.sizeOfMessages = {'sent':0, 'received': 0}
        self.discussionSizePerDay = {}
        self.beginningTimeCode = None
        self.complicityScore = 0

    ''' Returns the length of the messages list '''
    def __len__(self):
        return len(self.messagesList)

    ''' Returns a "complicity score" for the discussion thats scales with the discussion age and the discussion length '''
    def computeComplicityScore(self):
        timecodeDate = datetime.datetime.strptime(timestampToDate(self.beginningTimeCode), "%d/%m/%Y")
        convAge = (datetime.datetime.now() - timecodeDate).days
        self.complicityScore = int(math.sqrt(convAge**2 * self.messagesAmount['self'] * self.messagesAmount['other']) / (1000*len(self.participants)**2))

    ''' Adds Messages to the discussion from a list of Messages'''
    def addMessagesFromList(self, discussionTitle: str, messagesList: dict):
        for message in messagesList[::-1]:
            senderName = message['sender_name'].encode("latin1").decode("utf-8") 
            timestamp = message['timestamp_ms']
            share = message['share'] if 'share' in message else None
            content = message['content'].encode('latin1').decode('utf-8') if 'content' in message else 'Message Vocal' if 'audio_files' in message else 'Image'
            msgObject = Message(senderName, timestamp, discussionTitle, content, 'content' in message, share)
            self.addMessage(msgObject)

    ''' Returns the amount of the Discussion's participants '''
    def getParticipantsAmount(self):
        return len(self.participants)

    ''' Adds a Message to the discussion '''
    def addMessage(self, message):
        self.messagesList.append(message)
    
    ''' Returns the amount of messages sent by a participant '''
    def getMessageAmount(self, participantName):
        messAmount = 0
        for message in self.messagesList:
            if message.getSender() == participantName:
                messAmount += 1
        return messAmount
    
    ''' Returns a dictionnaries with participants names as keys and amount of messages sent as values '''
    def generateMessagesAmount(self):
        messagesAmount = {}
        for personName in self.participants:
            messagesAmount[personName] = self.getMessageAmount(personName)
        self.messagesAmount = messagesAmount
    

