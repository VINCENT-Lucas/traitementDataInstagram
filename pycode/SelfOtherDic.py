from .util import *

class SelfOtherDic:
    def __init__(self, ownInit={}, othersInit={}) -> None:
        self.own = ownInit
        self.others = othersInit
    
    def update(self, dic, key, amount):
        if key not in dic:
            dic[key] = amount
        else:
            dic[key] += amount
        return dic

    def addSelf(self, *args):
        if len(args) == 1:
            if type(args[0]) == dict:
                for key in args[0]:
                    self.own = self.update(self.own, key, args[0][key])
            elif type(args[0]) == list:
                for elem in args[0]:
                    self.own = self.update(self.own, elem, 1)
            else:
                self.own = self.update(self.own, args[0], 1)
        else:
            self.own = self.update(self.own, args[0], args[1])
        return self.own
    
    def addOther(self, *args):
        if len(args) == 1:
            if type(args[0]) == dict:
                for key in args[0]:
                    self.others = self.update(self.others, key, args[0][key])
            elif type(args[0]) == list:
                for elem in args[0]:
                    self.others = self.update(self.others, elem, 1)
            else:
                self.others = self.update(self.others, args[0], 1)
        else:
            self.others = self.update(self.others, args[0], args[1])
    
    def merge(self, *args):
        if len(args) == 1:
            self.addSelf(args[0].own)
            self.addOther(args[0].others)
        else:
            self.addSelf(args[0])
            self.addOther(args[1])

    def add(self, selfOrOther, arg):
        if selfOrOther == 'self':
            self.addSelf(arg)
        else:
            self.addOther(arg)

    def sort(self):
        self.own = dict(sorted(self.own.items(), key=lambda item: item[1], reverse=True))
        self.others = dict(sorted(self.others.items(), key=lambda item: item[1], reverse=True))
    
    def sumOwnOthers(self):
        return updateDictFromDict(self.own, self.others)
    

