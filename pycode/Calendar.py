import os, datetime
from .Html import *

class Calendar:
  def __init__(self) -> None:
    self.biggestStreak = 0
    
  def writeCalendar(self, daysList, discussion, fileManager):
      with open(os.path.join(fileManager.calendarPath, discussion.dirName + '.html'), 'w', encoding="utf-8") as dataFile:
        if daysList == []:
          dataFile.write("No messages")
          return

        monthDict = {"01": "Jan", "02": "Fév", "03": "Mar", "04": "Avr", "05": "Mai", "06": "Juin", "07": "Juil", "08": "Août", "09": "Sept", "10": "Oct", "11": "Nov", "12": "Déc"}
        dataFile.write(Html.getCalendarHeader())
        # Début du tableau
        title = f'<header>\n<h1>Calendrier: {discussion.title}</h1>\n</header>\n'
        dataFile.write('<body>' + title + '\n\t<div class="container">\n\t\t<table class="table">\n\t\t<tbody>')

        # Génération des numéros de jours
        text = '<tr>\n<td class="year-cell"><span class="number"> </span></td>\n<td class="number-cell"><span class="number"> </span></td>\n'
        for i in range(1, 32):
          text += f'<td class="number-cell"><span class="number">{i}</span></td>' + '\n'
        text += '</tr>'
        dataFile.write(text)

        currentStreak = 1

        # Génération des cases
        currentDay = '01/01/' + daysList[0][6:]
        dataFile.write('<tr>\n<td class="year-cell"><span class="number"> </span></td>\n<td class="number-cell"><span class="number">Jan</span></td>\n')
        while daysList != [] or self.nextDay(currentDay)[:5] != '02/01':
          # Si la date est présente dans la liste, on ajoute une case verte, et on passe au jour suivant dans la liste
          # Sinon on ajoute une case rouge
          
          if daysList == [] or currentDay != daysList[0]:
            text = '<td class="red"><span style="color: transparent;">o</span></td>\n'
            currentStreak = 0
          else:
            text = f'<td class="green"><a href="{os.path.join(fileManager.conversationsPath, discussion.dirName + ".html") + "#" + currentDay}" style="color: transparent;">o</a></td>\n'
            daysList = daysList[1:]
            currentStreak += 1
            if currentStreak > self.biggestStreak:
              self.biggestStreak = currentStreak
          dataFile.write(text)
            
          # On regarde si on change de mois
          if self.nextDay(currentDay)[3:5] != currentDay[3:5]:
            # On rajoute des cases grises pour les jours qui n'existent pas (30 février, 31 avril...)
            greyAmount, text = 31 - int(currentDay[:2]), ''
            for i in range(greyAmount):
              text += '<td class="grey"></td>\n'
            dataFile.write(text + '</tr>\n<tr>\n')

            # On regarde si on change d'année
            if self.nextDay(currentDay)[:5] == '01/12':
              dataFile.write('<tr class="transition-line">')

            # On regarde si le mois correspond à 05 pour écrire l'année
            if currentDay[3:5] == '05':
              text = f'<td class="year-cell"><span class="number">{currentDay[6:]}</span></td>'
            else:
              text = '<td class="year-cell"><span class="number"> </span></td>'
            if daysList != [] or self.nextDay(currentDay)[:5] != '01/01':
              text += f'<td class="number-cell"><span class="number">{monthDict[self.nextDay(currentDay)[3:5]]}</span></td>'
            dataFile.write(text)

          currentDay = self.nextDay(currentDay)
        #Fin du tableau
        dataFile.write('</tbody>\n</table>\n</div>\n</body>')
  
  def nextDay(self, date_str):
    dateObj = datetime.datetime.strptime(date_str, '%d/%m/%Y')
    newDate = dateObj + datetime.timedelta(days=1)
    newDateStr = newDate.strftime('%d/%m/%Y')
    return newDateStr
    
