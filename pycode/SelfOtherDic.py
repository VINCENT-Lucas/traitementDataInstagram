from .util import *

class SelfOtherDic:
    def __init__(self, ownInit=None, othersInit=None) -> None:
        if not ownInit:
            self.own = {}
        else:
            self.own = ownInit
        if not othersInit:
            self.others = {}
        else:
            self.others = othersInit
        

    def add(self, selfOrOther, arg, value=1):
        if selfOrOther == 'self':
            if arg in self.own:
                self.own[arg] += value
            else:
                self.own[arg] = value
        else:
            if arg in self.others:
                self.others[arg] += value
            else:
                self.others[arg] = value
    
    def addAll(self, selfOrOther, listOrDic):
        if type(listOrDic) == list:
            for elem in listOrDic:
                self.add(selfOrOther, elem, value=1)
        elif type(listOrDic) == dict:
            for key in listOrDic:
                self.add(selfOrOther, key, listOrDic[key])
        else:
            raise("ArgError")


    def sort(self):
        self.own = dict(sorted(self.own.items(), key=lambda item: item[1], reverse=True))
        self.others = dict(sorted(self.others.items(), key=lambda item: item[1], reverse=True))
    
    def sumOwnOthers(self):
        return sumOfTwoDicts(self.own, self.others)
    

