import math

class WordFrequence:
    '''Pour un mot et une conversation donnés on a:
        - Camount = le nombre de fois que le mot apparaît dans la conversation
        - Tamount = le nombre de fois que le mot apparaît dans l'ensemble des conversations
        - Csize = la taille de la conversation
        - Tsize = la taille de l'ensemble des conversations
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

    def getWeight(self):
        cPerc = self.convPercentage()
        cCoeff = self.convCoeff()
        if self.Tamount < self.Tsize/10000:
            cCoeff /= (self.Tsize/10000 - self.Tamount)**4
        
        return cPerc * math.sqrt(cCoeff)