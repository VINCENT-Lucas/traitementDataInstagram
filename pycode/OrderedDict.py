''' Just an Ordered Dictionnary that implements the add() method '''
class OrderedDict:
    def __init__(self, length) -> None:
        self.length = length
        self.list = []
    
    def add(self, key, value):
        if self.list == []:
            self.list.append((key, value))
            return
        
        for i in range(len(self.list)):
            if value > self.list[i][1]:
                self.list.insert(i, (key, value))
                self.list = self.list[:self.length]
                return
    
    def getDict(self):
        dict = {}
        for key, value in self.list:
            dict[key] = value
        return dict

