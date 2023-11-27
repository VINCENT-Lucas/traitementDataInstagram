from .util import *

class TimeZones:
    def __init__(self, data, filesManager) -> None:
        self.data = data
        self.filesManager = filesManager
        self.discussions = data.discussionsList
        self.firstMessageDate = timestampToDate(data.mostAncientDiscussion[1])[3:]

    def generateColors(self, amount):
        ''' Génère amount couleurs sous forme rgba(255, 99, 132, 1)'''
        colorsList = []
        for i in range(amount):
            # Variation des composantes RVB en fonction de l'itération
            r = int(255 * (i / amount))
            g = int(255 * ((i + amount // 3) / amount) % 256)
            b = int(255 * ((i + 2 * amount // 3) / amount) % 256)

            colorsList.append(f"rgba({r}, {g}, {b}, 1)")

        self.colorsList = colorsList

    def monthToTimeCode(month):
        return datetime.strptime(month, '%m/%Y')

    def generateMonthsFrom(referenceMonth):
        list = [referenceMonth]
        actualMonth = datetime.datetime.now().strftime("%m/%Y")
        while referenceMonth != actualMonth:
            if referenceMonth[:2] != '12':
                number = int(referenceMonth[:2])+1
                numberToStr = str(number) if number > 9 else '0' + str(number)
                referenceMonth = numberToStr + referenceMonth[2:]
            else:
                referenceMonth = '01/' + str(int(referenceMonth[3:])+1)
            list.append(referenceMonth)
        return list

    def monthIsSuperior(month1, month2):
        year1, year2 = int(month1[3:]), int(month2[3:])
        month1, month2 = int(month1[:2]), int(month2[:2])
        return year1 > year2 or year1 == year2 and month1 > month2

    def generateDataSet(self):
        dataSets = []
        monthsList = TimeZones.generateMonthsFrom(datetime.datetime.fromtimestamp(self.data.mostAncientDiscussion[1]/1000).strftime("%m/%Y"))
        self.generateColors(len(self.discussions))
        #print("MonthList", monthsList)

        for discussion in self.discussions:
            #print(f"{discussion.title}: {len(discussion.messagesList)}, {discussion.discussionSizePerDay}")
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
            
            discussionDict['data'] = monthsData
            discussionDict['borderColor'] = self.colorsList.pop(0)
            discussionDict['borderWidth'] = 2
            dataSets.append(discussionDict)
        self.dataSets = dataSets
        self.monthsList = monthsList

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

<!-- Ajoutez un conteneur pour le graphique -->
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