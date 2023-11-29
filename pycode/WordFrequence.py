import math

''' A class that calculates the representativeness of words within the discussions in which they are sent. '''
class WordFrequence:
    '''For a word and a Discussion we have:
        - Camount = the amount of the word's apparitions in the discussion
        - Tamount = the amount of the word's apparitions in all discussions
        - Csize = the discussion's size
        - Tsize = the sum of all discussions sizes
        '''
    def __init__(self, word, Camount, Tamount, Csize, Tsize) -> None:
        self.word = word
        self.Camount = Camount
        self.Tamount = Tamount
        self.Csize = Csize
        self.Tsize = Tsize

    def __str__(self) -> str:
        return f"[{self.word}]  -Conversation: {self.Camount}/{self.Csize}    - Global: {self.Tamount}/{self.Tsize}"

    def convPercentage(self):
        return 100*self.Camount/self.Tamount

    def convCoeff(self):
        return self.Camount*self.Tsize/(self.Tamount*self.Csize)

    ''' Returns the representativeness of a word '''
    def getWeight(self):
        cPerc = self.convPercentage()
        cCoeff = self.convCoeff()
        if self.Tamount < self.Tsize/10000:
            cCoeff /= (self.Tsize/10000 - self.Tamount)**4
        
        return cPerc * math.sqrt(cCoeff)