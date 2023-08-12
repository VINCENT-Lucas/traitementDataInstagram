import os

from code.utilitaries import *

global emptyCase, greyCase

emptyCase = '<td class="number-cell"><span class="number"> </span></td>'
greyCase = '<td class="grey"></td>'

# --------------------- Répartition horaire ---------------------

''' Header du timeTable '''
def AccountDataGetHeader():
  return '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    header {
      font-weight: bold;
      text-align: center; /* Centrer le titre */
      color: #2d2c2c; /* Couleur du texte de l'en-tête */
      text-shadow: 1px 1px 2px #000; /* Ajouter une ombre au texte */
    }
    .highlight {
      text-align: center;
      padding: 5px;
      font-size: 20px;
      font-weight: bold;
    }
    .table {
      border-collapse: collapse;
      margin-left: auto;
      margin-right: auto;
    }
    .table td {
      width: 20px;
      height: 20px;
      border-right: 4px solid black; /* Bordure à droite */
      border-left: 4px solid black;  /* Bordure à gauche */
    }
    .table .number-cell {
      border: none;
    }
    .container {
      display: flex;
      align-items: center;
    }
    body {
      background-color: #d8ecf1; /* Couleur de fond de la page */
    }
  </style>
</head>\n'''

''' Calcule la couleur d'une case en fonction de sa hauteur '''
def calculateGradientColor(height, maxValue):
    relativeHeight = height / maxValue

    red = int(68 + 127 * relativeHeight)
    green = 10
    blue = 60

    return f'rgb({red}, {green}, {blue})'

''' Génère un graphe en fonction d'un dictionnaire donné '''
def generateGraph(dataDic):
  htmlCode = '<div class="container"> <table class="table"> \n\t <tbody>'

  percentageDic = dicToPercentageDic(dataDic)
  maxValue = dicGetMaxValue(percentageDic)

  # Le graphe a une hauteur max de taille maxValue
  for i in range(maxValue + 1, 0, -1):
    # On crée une nouvelle ligne de tableau
    htmlCode += '<tr>\n'

    # On traite le graph ligne par ligne
    for key in dataDic:
      if i <= percentageDic[key]:
        gradientColor = calculateGradientColor(i, maxValue)
        htmlCode += f'<td style="width: 20px; height: 20px; border-right: 4px solid black; border-left: 4px solid black; background-color: {gradientColor};"></td>'
      elif i == percentageDic[key] + 1:
        htmlCode += f'<td class="number-cell"><span class="number">{dataDic[key]}</span></td>'
      else:
        htmlCode += emptyCase
    # Fin de ligne
    htmlCode += '</tr>\n'
  
  htmlCode += '<tr>\n'
  for key in dataDic:
    htmlCode += f'<td class="number-cell"><span class="number">{key}</span></td>\n'
  htmlCode += '</tr>\n'

  #Fin du tableau
  htmlCode += '</tbody>\n</table>\n</div>'
  return htmlCode

''' Horaires d'envoi/Réception des messages'''
def generateAccountData(username, complicityScoreDic, conversationAgeDic, conversationSizeDic, conversationMaxStreakDic, sentDic, receivedDic, amountOfMessPerDayDic, sentMsgTimeTableDic, path):
    # Début de la construction du code HTML
    htmlCode = AccountDataGetHeader()

    htmlCode += '<body>\n'
    htmlCode += f'\t<header>\n<h1> {username} </h1>\n</header>\n'

    htmlCode += f'<div class="highlight"> Meilleure conversation: <span style="text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">{dicGetMaxKey(complicityScoreDic)}</span> ({dicGetMaxValue(complicityScoreDic)}☆)</div>\n'
    htmlCode += f'<div class="highlight"> Plus ancienne conversation: <span style="text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">{dicGetMinKey(conversationAgeDic)}</span> ({dateTimeToDays(dicGetMinValue(conversationAgeDic))}j)</div>\n'
    htmlCode += f'<div class="highlight"> Plus longue conversation: <span style="text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">{dicGetMaxKey(mergeDic(conversationSizeDic))}</span> ({dicGetMaxValue(mergeDic(conversationSizeDic))} messages)</div>\n'
    htmlCode += f'<div class="highlight"> Conversation la plus stable: <span style="text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">{dicGetMaxKey(conversationMaxStreakDic)}</span> ({dicGetMaxValue(conversationMaxStreakDic)}j de conversation à la suite)</div>\n'

    htmlCode += f'<div class="highlight"> Nombre de messages envoyés: {sumDicI(conversationSizeDic, 0)}</div>'
    htmlCode += f'<div class="highlight"> Nombre de messages reçus: {sumDicI(conversationSizeDic, 1)}</div>'
    htmlCode += f'<div class="highlight"> Nombre de conversations: {len(conversationAgeDic)}</div>'
    htmlCode += f'<div class="highlight"> Jour le plus actif: {dicGetMaxKey(amountOfMessPerDayDic)}, {dicGetMaxValue(amountOfMessPerDayDic)} messages envoyés</div>'
    htmlCode += f'<div class="highlight"> Période la plus active de la journée: {dicGetMaxKey(sentMsgTimeTableDic)} ({dicGetMaxValue(dicToPercentageDic(sentMsgTimeTableDic))}% des messages)</div>'

    # Ajout du titre
    htmlCode += '\t<header>\n<h1> Nombre de messages envoyés par heure. </h1>\n</header>\n'
    
    # Ajout d'un graphe
    htmlCode += generateGraph(orderDicKeys(sentDic))

    htmlCode += '\t<header>\n<h1> Nombre de messages reçus par heure. </h1>\n</header>\n'
    htmlCode += generateGraph(orderDicKeys(receivedDic))
    
    # Fin du body 
    htmlCode += '\n</body>'

    with open(path, 'w', encoding="utf-8") as writingFile:
      writingFile.write(htmlCode)
  

# --------------------- Calendrier -------------------

''' [HTML] Renvoie les headers du calendrier'''
def calendarGetHeader():
  return '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    header {
      font-weight: bold;
      text-align: center; /* Centrer le titre */
      color: #2d2c2c; /* Couleur du texte de l'en-tête */
      text-shadow: 1px 1px 2px #000; /* Ajouter une ombre au texte */
    }
    .table {
      border-collapse: collapse;
      margin-left: auto;
      margin-right: auto;
    }
    .table td {
      width: 10px;
      height: 10px;
      border: 4px solid black;
    }
    .table .red {
      background-color: rgba(175, 40, 40, 0.666);
    }
    .table .green {
      background-color: rgba(76, 175, 40, 0.666);
    }
    .table .grey {
      background-color: grey;
    }
    .table .bottomLine {
      border: none;
      border-bottom: 4px solid black; 
    }
    .table .number {
      text-align: center;
      font-weight: bold;
    }
    .table .number-cell {
      border: none;
    }
    .container {
      display: flex;
      align-items: center;
    }
    .text {
      margin-right: 10px;
      font-weight: bold;
    }
    .table .year-cell {
      border: none;
      writing-mode: vertical-lr;
      text-orientation: mixed;
      white-space: nowrap;
      transform: rotate(180deg);
    }
    .transition-line td {
      border-bottom: 8px solid black;
    }
    body {
      background-color: #d8ecf1; /* Couleur de fond de la page */
    }
  </style>
</head>\n'''

''' [HTML] Ecriture du calendrier d'activité'''
def writeCalendar(daysList, link, convData, nextDay, dirPaths, name):
  if daysList == []:
    with open(link, 'w', encoding="utf-8") as DataFile:
      DataFile.write("No messages")
    return

  monthDict = {"01": "Jan", "02": "Fév", "03": "Mar", "04": "Avr", "05": "Mai", "06": "Juin", "07": "Juil", "08": "Août", "09": "Sept", "10": "Oct", "11": "Nov", "12": "Déc"}
  text = calendarGetHeader()
  # Début du tableau
  title = f'<header>\n<h1>Calendrier: {convData["conversationName"]}</h1>\n</header>\n'
  text += '<body>' + title + '\n\t<div class="container">\n\t\t<table class="table">\n\t\t<tbody>'

  # Génération des numéros de jours
  text += '<tr>\n<td class="year-cell"><span class="number"> </span></td>\n<td class="number-cell"><span class="number"> </span></td>\n'
  for i in range(1, 32):
    text += f'<td class="number-cell"><span class="number">{i}</span></td>' + '\n'
  text += '</tr>'

  currentStreak = 1

  # Génération des cases
  currentDay = '01/01/' + daysList[0][6:]
  text += '<tr>\n<td class="year-cell"><span class="number"> </span></td>\n<td class="number-cell"><span class="number">Jan</span></td>\n'
  while daysList != [] or nextDay(currentDay)[:5] != '02/01':
    # Si la date est présente dans la liste, on ajoute une case verte, et on passe au jour suivant dans la liste
    # Sinon on ajoute une case rouge
    if daysList == [] or currentDay != daysList[0]:
      text += '<td class="red"><span style="color: transparent;">o</span></td>\n'
      currentStreak = 0
    else:
      text += f'<td class="green"><a href="{os.path.join(dirPaths["Conversations"], name + ".html") + "#" + currentDay}" style="color: transparent;">o</a></td>\n'
      daysList = daysList[1:]
      currentStreak += 1
      if currentStreak > convData["biggestStreak"]:
         convData["biggestStreak"] = currentStreak
      
    # On regarde si on change de mois
    if nextDay(currentDay)[3:5] != currentDay[3:5]:
      # On rajoute des cases grises pour les jours qui n'existent pas (30 février, 31 avril...)
      greyAmount = 31 - int(currentDay[:2])
      for i in range(greyAmount):
         text += '<td class="grey"></td>\n'
      text += '</tr>\n<tr>\n'

      # On regarde si on change d'année
      if nextDay(currentDay)[:5] == '01/12':
        text += '<tr class="transition-line">'

      # On regarde si le mois correspond à 05 pour écrire l'année
      if currentDay[3:5] == '05':
        text += f'<td class="year-cell"><span class="number">{currentDay[6:]}</span></td>'
      else:
        text += '<td class="year-cell"><span class="number"> </span></td>'
      if daysList != [] or nextDay(currentDay)[:5] != '01/01':
        text += f'<td class="number-cell"><span class="number">{monthDict[nextDay(currentDay)[3:5]]}</span></td>'

    currentDay = nextDay(currentDay)
  #Fin du tableau
  text += '</tbody>\n</table>\n</div>\n</body>'
  with open(link, 'w', encoding="utf-8") as dataFile:
    dataFile.write(text)

# --------------------- Conversations --------------

''' [HTML] Le début des fichiers HTML du dossier Conversations'''
def getHTMLConvHeader(conversationName):
    return f'''<!DOCTYPE html>
<html>
<head>
  <title>{conversationName}</title>
  <meta charset="utf-8">
  <style>
    .container {{
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      background-color: #fafafa;
      font-family: Arial, sans-serif;
    }}
    .message {{
      border-radius: 10px;
      padding: 10px;
      margin-bottom: 10px;
    }}
    .user {{
      font-weight: bold;
      color: #3897f0;
    }}
    .timestamp {{
      font-size: 12px;
      color: #999999;
    }}
    .text {{
      margin-top: 5px;
    }}
    .user1 {{
      text-align: right;
      background-color: #f3f0f0;
    }}
    .user2 {{
      text-align: left;
      background-color: #ffffff;
    }}
  </style>
</head>
    '''

''' [HTML] Génère le compteur de mots'''
def generate_html(dictionary, name, title, dirPaths):
    count = 1
    link = dirPaths['Menus'] + "\\" + name
    html_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>'''+title+'''</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            padding: 20px;
            margin: 0;
        }

        h1 {
            color: #333333;
            text-align: center;
        }

        .row {
            display: flex;
            justify-content: center;
        }

        .box {
            background-color: #ffffff;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        .box:not(:last-child) {
            margin-right: 10px;
        }

        .box:nth-child(1) {
            font-size: 22px;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border-bottom-left-radius: 15px;
            border-bottom-right-radius: 15px;
        }

        .box:nth-child(2) {
            font-size: 20px;
        }

        .box:nth-child(3) {
            font-size: 18px;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border-bottom-left-radius: 15px;
            border-bottom-right-radius: 15px;
        }
    </style>
</head>
<body>
    <h1>'''+title+'''</h1>
'''

    for key in dictionary:
        html_content += f'    <div class="row">\n'
        html_content += f'        <div class="box">{count}</div>\n'
        html_content += f'        <div class="box">{key}</div>\n'
        html_content += f'        <div class="box">{dictionary[key]}</div>\n'
        html_content += f'    </div>\n'
        count += 1
    
    html_content += '''
</body>
</html>
'''
    with open(link, 'w', encoding="utf-8") as file:
        file.write(html_content)

''' [HTML] Génère le index'''
def generate_index(dirPaths, username):
    html_content = f'''<!DOCTYPE html>
<html>
<head>
  <title>Mes données Instagram</title>
  <meta charset="utf-8">
  <style>
    header {{
      font-family: Georgia, serif;
      font-weight: bold;
      font-size: 40px;
      margin-top: 50px;
      text-align: center;
      color: #2d2c2c;
      text-shadow: 0px 0px 0px #000;
    }}
    tag {{
      font-family: Georgia, serif;
      font-weight: bold;
      font-size: 40px;
      text-align: center;
      color: #2d2c2c;
    }}
    body {{
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
    }}
    .button-container {{
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      margin: 50px 100px 0px 100px;
    }}
    .button-container a {{
      text-decoration: none;
      margin: 10px 0;
    }}
    .button {{
      display: inline-block;
      padding: 10px 20px;
      background-color: #3b3e3e63;
      color: #ffffff;
      border-radius: 4px;
      font-size: 16px;
      transition: background-color 0.3s ease;
    }}
    .button:hover {{
      background-color: #E2A9F3;
    }}
    .background-image {{
      background-image: url('images/background.jpg');
      background-size: cover;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: -1;
    }}
    .image-container {{
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 40vh;
      margin-top: 50px;
    }}
    .image-container img {{
      max-width: 5%;
      max-height: 5%;
    }}
  </style>
</head>
<body>
  <div class="background-image"></div>

  <header>Mes données Instagram</header>

  <div class="button-container">
    <a href="{dirPaths['Menus']}\messageCount.html" class="button">Voir les plus longues conversations</a>
    <a href="{dirPaths['Menus']}\convAge.html" class="button">Conversations les plus anciennes</a>
    <a href="{dirPaths['Menus']}\wordCounter.html" class="button">Liste des mots les plus utilisés</a>
    <a href="{dirPaths['Menus']}\convMenu.html" class="button">Voir les conversations</a>
    <a href="{dirPaths['Menus']}\\accountData.html" class="button">Données du compte</a>
  </div>

  <div class="image-container">
    <img src="images/instagramIcon.png" alt="Image">
    <tag>@{username}</tag>
  </div>
</body>
</html>
'''
    with open(f"{dirPaths['Root']}\index.html", 'w', encoding="utf-8") as indexFile:
        indexFile.write(html_content)

# ------------------ Fichier ConvMenu -----------------------

''' [HTML] Génère le menu des conversations convMenu.html'''
def generateConvMenu(usersInfo, dirPaths):
  html_content = '''<!DOCTYPE html>
  <html>
  <head>
    <title>Conversations Instagram</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        background-color: #f2f2f2;
        margin: 0;
        padding: 20px;
      }
      h1 {
        text-align: center;
        color: #333333;
      }
      ul {
        list-style-type: none;
        padding: 0;
      }
      li {
        margin-bottom: 10px;
      }
      a {
        display: block;
        background-color: #ffffff;
        border: 1px solid #dddddd;
        border-radius: 4px;
        padding: 10px;
        color: #333333;
        text-decoration: none;
        transition: background-color 0.3s ease;
      }
      a:hover {
        background-color: #dddddd;
      }
      .button {
        background-color: #c6e3bc;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 5px 10px;
        font-size: 12px;
        cursor: pointer;
      }
    </style>
  </head>
  <body>
    <h1>Conversations Instagram</h1>
    <ul>'''
  for name in usersInfo:
    button = f'<a href={os.path.join(dirPaths["Données"], name+".html")} class="button">Détails</a>'
    html_content += f'<li><a href="{os.path.join(dirPaths["Conversations"], name+".html")}">{usersInfo[name]}</a>\n{button}</li>'

  html_content += "</ul>\n</body>\n</html>"

  with open(f"{dirPaths['Menus']}\convMenu.html", 'w', encoding="utf-8") as file:
      file.write(html_content)

# ------------------ Fichier Données ----------------

def dataGetHeader():
  return '''<!DOCTYPE html>
<html>
<head>
  <title>Données de conversation</title>
  <meta charset="utf-8">
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f2f2f2;
    }
    header {
      font-weight: bold;
      text-align: center;
      color: #333;
      padding: 20px;
      background-color: #fff;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      text-shadow: 1px 1px 2px #000;
    }
    .container {
      display: flex;
      justify-content: space-around;
      max-width: 800px;
      margin: 20px auto;
    }
    .column {
      flex: 1;
      padding: 20px;
      background-color: #fff;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      border-radius: 8px;
    }
    h2 {
      color: #555;
    }
    ul {
      list-style: none;
      padding: 0;
    }
    li {
      margin-bottom: 10px;
      color: #666;
    }
    .table {
      border-collapse: collapse;
      margin-left: auto;
      margin-right: auto;
    }
    .button-container {
      text-align: center;
      margin-top: 20px;
      margin-bottom: 40px;
    }
    .button {
      padding: 10px 20px;
      background-color: #86c088;
      color: white;
      text-decoration: none;
      font-size: 16px;
      border-radius: 4px;
      transition: background-color 0.3s ease;
    }
    .button:hover {
      background-color: #639e6e;
    }
  </style>
</head>
'''

''' [HTML] Affichage d'un fichiers HTML du dossier Données'''
def htmlOutputData(listUser1, listUser2, listGlobal, fileName, convName, dirPaths, hoursDic, username):
  txt = dataGetHeader()
  txt += f'<body>\n<header>\n\t<h1>Données de conversation: {convName}</h1>\n</header>\n'
  
  # Partie user1
  txt += f'<div class="container">\n<div class="column">\n<h2>{username}</h2>\n<ul>\n'
  for line in listUser1:
    txt += f'<li>{line}</li>\n'
  txt += '</ul>\n</div>\n'

  # Partie user2
  txt += f'<div class="column">\n<h2>{convName}</h2>\n<ul>\n'
  for line in listUser2:
    txt += f'<li>{line}</li>\n'
  txt += '</ul>\n</div>\n'

  txt += '</div>\n'

  # Partie globale
  txt += '<div class="container">\n<div class="column">\n<ul>\n'
  for line in listGlobal:
    txt += f'<li>{line}</li>\n'
  txt += '</ul>\n</div>\n</div>\n'

  txt += '<div class="button-container">\n'
  txt += f'\t<a href="{os.path.join(dirPaths["Calendar"], fileName+".html")}" class="button">Voir le calendrier</a>\n'
  txt += f'\t<a href="{os.path.join(dirPaths["Words"], fileName+".html")}" class="button">Mots les plus utilisés</a>\n</div>\n'

  txt += '\n<header>\n<h1>Répartition des messages</h1>\n</header>\n'
  txt += generateGraph(orderDicKeys(hoursDic))

  txt += "</body>\n</html>"    
  return txt

''' [HTML] Ecriture des données dans le fichier correspondant'''
def writeDataConversation(fileName, convData,  calendarList, dirPaths, username, hoursDic):
    conversationName = convData["conversationName"]
    with open(os.path.join(dirPaths['Données'], fileName+'.html'), 'w', encoding="utf-8") as writingFile:

      listUser1 = [f"Nombre de messages envoyés: {convData['amountOfSentMsg']}."]
      listUser2 = [f"Nombre de messages envoyés: {convData['amountOfReceivedMsg']}."]

      meanAnsTime = convData['timeBeforeAnswering']/convData['amountOfSentAns'] if convData['amountOfSentAns']!=0 else 0
      listUser1.append(f"Temps moyen de réponse: {msToTime(meanAnsTime)}.")
      
      meanAnsTime = convData['timeBeforeGettingAnswered']/convData['amountOfReceivedAns'] if convData['amountOfReceivedAns'] !=0 else 0
      listUser2.append(f"Temps moyen de réponse: {msToTime(meanAnsTime)}.")
      
      daysList = extractDays(calendarList)

      meanAnsLength = convData["sizeOfSentMessages"]/convData['amountOfSentMsg'] if convData['amountOfSentMsg'] !=0 else 0
      listUser1.append(f"Taille moyenne des messages: {int(meanAnsLength)} caractères.")
      meanAnsLength = convData["sizeOfReceivedMessages"]/convData['amountOfReceivedMsg'] if convData['amountOfReceivedMsg'] !=0 else 0
      listUser2.append(f"Taille moyenne des messages: {int(meanAnsLength)} caractères.")

      listGlobal = []
      mostActiveDay, messageAmount = mostCommonElement(daysList)
      if mostActiveDay:
        listGlobal.append(f"Jour de la plus longue discussion: {mostActiveDay}: {messageAmount} messages.")
      else:
        listGlobal.append(f"Jour de la plus longue discussion: Aucun.")
      
      listGlobal.append(f"Plus grande période de conversation: {convData['biggestStreak']} jours.\n")
      writingFile.write(htmlOutputData(listUser1, listUser2, listGlobal, fileName, conversationName, dirPaths, hoursDic, username))

# ------------------ Autres -----------------------



# ---------------------- Words ------------------- 

''' [HTML] Affichage d'un fichiers HTML du dossier Words'''
def htmlOutputWords(list, convName):
  txt = dataGetHeader()
  txt += f'<body>\n<header>\n<h1>{convName}: mots les plus utilisés</h1>\n</header>\n'
  txt += "<ul>"
  for elem in list:
    txt += "<li>" + elem + "</li>"
  txt += "</ul>\n"

  txt += "</body>\n</html>"    
  return txt

''' Trie les ratios des valeurs de 2 dictionnaires par clefs données par ordre décroissant. '''
def generateRatio(globalCounterDic, convCounterDic):
  finalDic = {}
  for key in convCounterDic:
    if key not in globalCounterDic or globalCounterDic[key] == convCounterDic[key]:
      finalDic[key] = 0
    else:
      finalDic[key] = (convCounterDic[key]/globalCounterDic[key])
  
  return orderDic(finalDic)

''' Ecriture dans les fichiers du dossier Words des mots les plus utilisés dans une conversation. '''
def writeMostUsedWords(conversationWordCounter, wordCounterDic, path, conversationName, fileName, dirPaths, hoursDic):
  differencesDic = generateRatio(wordCounterDic, conversationWordCounter)
  list, count = [], 0
  
  for key, value in differencesDic.items():
    if int(100*value) != 0:
      list.append(str(key) + ": " + str(int(100*value)) + '%')
      count += 1
    if count > 50:
      break
  
  with open(path, 'w', encoding="utf-8") as writingFile:
    # Il faut utiliser une autre fonction que htmlOutputData()
    writingFile.write(htmlOutputWords(list, conversationName))
