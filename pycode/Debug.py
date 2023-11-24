class Debug:
    def __init__(self) -> None:
        pass
    
    def detectBadOrder(self, data):
        for discussion in data.discussionsList:
            last = discussion.messagesList[0].timecode
            for message in discussion.messagesList:
                time = message.timecode
                if time < last:
                    print(f"probleme {discussion.title}: {time}, {last}")