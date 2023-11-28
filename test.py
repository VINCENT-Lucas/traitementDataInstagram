import datetime

def nextMonth(month):
        #month : str sous forme '%m/%Y'
        imois, iyear = int(month[:2]), int(month[3:])
        if imois == 12:
            return '01/' + str(iyear + 1)
        newMonth = str(imois + 1) if imois + 1 > 9 else '0' + str(imois + 1)
        return newMonth + '/' + str(iyear)
 
def generateMonthsFrom(referenceMonth):
        list = [referenceMonth]
        actualMonth = datetime.datetime.now().strftime("%m/%Y")
        while referenceMonth != actualMonth:
            referenceMonth = nextMonth(referenceMonth)
            list.append(referenceMonth)
        return list

print('12/2020-01/2021'[-7:])
