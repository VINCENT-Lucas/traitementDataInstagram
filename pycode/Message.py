''' Represents an Instagram Message, with all the informations it has'''
class Message:
    def __init__(self, sender, timecode, discussionName, content, isARealMessage=True, share=None) -> None:
        self.sender = sender
        self.timecode = timecode
        self.discussionName = discussionName
        self.content = content
        self.isARealMessage = isARealMessage
        self.share = share
    
    def __len__(self):
        return len(self.content) if self.isARealMessage else 0

    def getContent(self):
        return self.content

    def getSender(self):
        return self.sender