from .util import *

class TimeZones:
    def __init__(self, data, filesManager) -> None:
        self.data = data
        self.filesManager = filesManager
        self.discussions = data.discussionsList
        self.firstMessageDate = timestampToDate(data.mostAncientDiscussion[1])[3:]

    def generateColors(self, amount):
        ''' Génère "amount" couleurs sous forme rgba(255, 99, 132, 1)'''
        colorsList = []
        step = int(255/((amount//7)+1))
        intensity = 0
        while len(colorsList) < amount:
            intensity += step

            colorsList.append(f"rgba({intensity}, {0}, {0}, 1)")
            colorsList.append(f"rgba({0}, {intensity}, {0}, 1)")
            colorsList.append(f"rgba({0}, {0}, {intensity}, 1)")
            colorsList.append(f"rgba({intensity}, {intensity}, {0}, 1)")
            colorsList.append(f"rgba({0}, {intensity}, {intensity}, 1)")
            colorsList.append(f"rgba({intensity}, {0}, {intensity}, 1)")
            colorsList.append(f"rgba({intensity}, {intensity}, {intensity}, 1)")

        self.colorsList = colorsList[:amount]

    def monthToTimeCode(month):
        return datetime.strptime(month, '%m/%Y')

    def generateMonthsFrom(referenceMonth):
        list = [referenceMonth]
        actualMonth = datetime.datetime.now().strftime("%m/%Y")
        while referenceMonth != actualMonth:
            referenceMonth = TimeZones.nextMonth(referenceMonth)
            list.append(referenceMonth)
        return list

    def monthIsSuperior(month1, month2):
        year1, year2 = int(month1[3:]), int(month2[-4:])
        month1, month2 = int(month1[:2]), int(month2[-7:-5])
        return year1 > year2 or year1 == year2 and month1 > month2

    def nextMonth(month):
        #month : str sous forme '%m/%Y'
        imois, iyear = int(month[:2]), int(month[3:])
        if imois == 12:
            return '01/' + str(iyear + 1)
        newMonth = str(imois + 1) if imois + 1 > 9 else '0' + str(imois + 1)
        return newMonth + '/' + str(iyear)

    def mergeData(monthsL, monthsV):
        #monthsL : Liste des mois sous format '%m/%y' depuis la création du compte
        #monthsV : Liste d'entiers qui représentent le nombre de messages envoyés chaque mois
        if len(monthsL)%2 == 1:
            monthsL.append(TimeZones.nextMonth(monthsL[-1][-7:]))
            monthsV.append(0)
        
        shorterMonthsL, shorterMonthsV = [], []
        for i in range(0, len(monthsV), 2):
            shorterMonthsL.append(monthsL[i][:7] + '-' + monthsL[i+1][-7:])
            shorterMonthsV.append(monthsV[i] + monthsV[i+1])
        return shorterMonthsL, shorterMonthsV


    def generateDataSet(self):
        dataSets = []
        monthsListRef = TimeZones.generateMonthsFrom(datetime.datetime.fromtimestamp(self.data.mostAncientDiscussion[1]/1000).strftime("%m/%Y"))
        self.generateColors(len(self.discussions))

        for discussion in self.discussions:
            #print(f"{discussion.title}: {len(discussion.messagesList)}, {discussion.discussionSizePerDay}")
            monthsList = monthsListRef
            discussionDict = {'label': discussion.title}
            monthsData = []
            idays, imonths, sumMonth = 0, 0, 0
            keysList, valuesList = list(discussion.discussionSizePerDay.keys()), list(discussion.discussionSizePerDay.values())
            day, msgAmount = keysList[0], valuesList[0]


            # On itère sur les mois, on fixe leur valeur à 0 tant qu'on n'a pas atteint le mois du 1er jour de discussion
            while TimeZones.monthIsSuperior(day[3:], monthsList[imonths]):
                monthsData.append(0)
                imonths += 1
            
            #print(f"Sortie de boucle: jour {day}")
            while imonths < len(monthsList):
                if day[3:] == monthsList[imonths]:
                    sumMonth += msgAmount
                    idays += 1
                    if idays >= len(keysList):
                        monthsData.append(sumMonth)
                        imonths += 1
                        while imonths < len(monthsList):
                            monthsData.append(0)
                            imonths += 1
                    else:
                        day, msgAmount = keysList[idays], valuesList[idays]
                else:
                    # Cas où on change de mois
                    monthsData.append(sumMonth)
                    sumMonth = 0
                    imonths += 1
            
            while len(monthsList) > 40:
                monthsList, monthsData = TimeZones.mergeData(monthsList, monthsData)

            discussionDict['data'] = monthsData
            discussionDict['borderColor'] = self.colorsList.pop(0)
            discussionDict['borderWidth'] = 2
            dataSets.append(discussionDict)
        self.dataSets = dataSets
        self.monthsList = monthsList
        print(dataSets, monthsList)

    def writeTimeZones(self):
        self.generateDataSet()
        with open(os.path.join(self.filesManager.menusPath, 'convEvolution.html'), 'w', encoding="utf-8") as writingFile:
            writingFile.write(self.generateOutput())

    def generateOutput(self):
        return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Évolution des conversations</title>
    
    <!-- Inclure la bibliothèque Chart.js depuis CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        h1 {{
            text-align: center;
            color: #333333;
        }}
        /* Ajoutez du style au conteneur du graphique */
        #myChartContainer {{
            width: 95%;
            margin: 0;
            padding: 20px;
            background-color: #f8f8f8;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
    </style>
</head>
<body>
<h1>Evolution du nombre de messages au cours du temps</h1>

<div id="myChartContainer">
    <!-- Ajoutez un canvas où le graphique sera rendu -->
    <canvas id="myChart" width="400" height="200"></canvas>
</div>

<script>
    // Données du graphique
    var data = {{
        labels: {self.monthsList},
        datasets: {self.dataSets}
    }};

    data.labels.forEach((month, index) => {{
        data.datasets.forEach(dataset => {{
            if (dataset.data[index] === 0) {{
                dataset.data[index] = null;
            }}
        }});
    }});

    // Options du graphique
    var options = {{
        scales: {{
            y: {{
                beginAtZero: true
            }}
        }},
        plugins: {{
            legend: {{
                display: false // Masquer les légendes
            }}
        }},
        animation: false
    }};

    // Récupérez le contexte du canvas
    var ctx = document.getElementById('myChart').getContext('2d');

    // Créez le graphique en ligne
    var myChart = new Chart(ctx, {{
        type: 'line',
        data: data,
        options: options
    }});
</script>

</body>
</html>
'''