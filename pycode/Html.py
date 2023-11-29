from .util import *

''' Generates all the invariant HTML code required for the files'''
class Html:
    def __init__(self) -> None:
        pass
    
    def getConversationHeader(conversationName):
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

    def getCalendarHeader():
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

    def getIndex(fileManager):
        return f'''<!DOCTYPE html>
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
    <a href="{fileManager.menusPath}\messageCount.html" class="button">Voir les plus longues conversations</a>
    <a href="{fileManager.menusPath}\convAge.html" class="button">Conversations les plus anciennes</a>
    <a href="{fileManager.menusPath}\wordCounter.html" class="button">Liste des mots les plus utilisés</a>
    <a href="{fileManager.menusPath}\convMenu.html" class="button">Voir les conversations</a>
    <a href="{fileManager.menusPath}\\accountData.html" class="button">Données du compte</a>
    <a href="{fileManager.menusPath}\emojisCounter.html" class="button">Liste des emojis les plus utilisés</a>
    <a href="{fileManager.menusPath}\convEvolution.html" class="button">Evolution des conversations</a>
  </div>

  <div class="image-container">
    <img src="images/instagramIcon.png" alt="Image">
    <tag>@{fileManager.data.accountOwner}</tag>
  </div>
</body>
</html>
'''

    def getConvMenuHeader():
        return '''<!DOCTYPE html>
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
    
    def getAccountDataHeader():
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

    def calculateGradientColor(height, maxValue):
        relativeHeight = height / maxValue

        red = int(68 + 127 * relativeHeight)
        green = 10
        blue = 60

        return f'rgb({red}, {green}, {blue})'

    def generateGraph(dataDic):
        htmlCode = '<div class="container"> <table class="table"> \n\t <tbody>'
        emptyCase = '<td class="number-cell"><span class="number"> </span></td>'

        percentageDic = dicToPercentageDic(dataDic)
        maxValue = max(percentageDic.values()) if percentageDic != {} else 0

        # Le graphe a une hauteur max de taille maxValue
        for i in range(maxValue + 1, 0, -1):
            # On crée une nouvelle ligne de tableau
            htmlCode += '<tr>\n'

            # On traite le graph ligne par ligne
            for key in dataDic:
                if i <= percentageDic[key]:
                    gradientColor = Html.calculateGradientColor(i, maxValue)
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

    def getRankingHeader(title):
        return'''
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

