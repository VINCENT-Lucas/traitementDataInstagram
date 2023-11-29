class Emoji:
    def __init__(self) -> None:
        self.notEmojiList = '‘…ɐ€’œ'
    ''' Estimates if a given string is an emoji (not very precise but I prefer not to use libraries)'''
    def isEmoji(self, str):
        if len(str) != 1 or ord(str)<8000:
            return False
        return str.lower() not in self.notEmojiList
