import datetime, time
from .DataStock import *
from .Html import *

''' This class is a bit useless, it will be removed soon '''
class Display:
    def __init__(self) -> None:
        pass
    
    def generateConversationHTML(self, conversationName, messagesList, accountOwner, ConversationFile):
        header = Html.getConversationHeader(conversationName)
        ConversationFile.write(header + '\n<body>\n<div class="container">')
        ancientDate = None
        for message in messagesList:
            txt = ''
            messageDate = timestampToDate(message.timecode)
            anchor_tag = ''
            if not ancientDate or messageDate[:9] != ancientDate[:9]:
                anchor_tag = '<a id="' + str(messageDate)[:10] + '"></a>'
            txt += anchor_tag
            usr = "message user1" if message.sender == accountOwner else "message user2"
            txt += f'<div class="{usr}">\n<span class="user">{message.sender}</span>\n<span class="timestamp">{messageDate}</span>\n<div class="text">{message.content}</div>\n</div>'
            ConversationFile.write(txt)
        ConversationFile.write("</div>\n</body>\n</html>")
