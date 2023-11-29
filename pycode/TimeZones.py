from .util import *

''' A class that represents the number of messages sent across all discussions over different periods '''
class TimeZones:
    def __init__(self, data, filesManager) -> None:
        self.biggestDiscussionByMonths = {}
        self.data = data
        self.filesManager = filesManager
        self.discussions = data.discussionsList
        self.firstMessageDate = timestampToDate(data.mostAncientDiscussion[1])[3:]

    def generateColors(self, amount):
        ''' Generates "amount" colors in the format: rgba(255, 99, 132, 1)'''
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
        ''' Converts a timecode to a month under %m/%Y format '''
        return datetime.strptime(month, '%m/%Y')

    def generateMonthsFrom(referenceMonth):
        ''' Generates the list of months between now and the reference month '''
        list = [referenceMonth]
        actualMonth = datetime.datetime.now().strftime("%m/%Y")
        while referenceMonth != actualMonth:
            referenceMonth = TimeZones.nextMonth(referenceMonth)
            list.append(referenceMonth)
        return list

    def monthIsSuperior(month1, month2):
        ''' Return True if the first number in parameter is more recent that the second one. (for example 08/2020 > 08/2019) '''
        year1, year2 = int(month1[3:]), int(month2[-4:])
        month1, month2 = int(month1[:2]), int(month2[-7:-5])
        return year1 > year2 or year1 == year2 and month1 > month2

    def nextMonth(month):
        ''' Takes a month in the '%m/%Y format and returns the next month '''
        imois, iyear = int(month[:2]), int(month[3:])
        if imois == 12:
            return '01/' + str(iyear + 1)
        newMonth = str(imois + 1) if imois + 1 > 9 else '0' + str(imois + 1)
        return newMonth + '/' + str(iyear)

    def mergeData(monthsL, monthsV):
        ''' Takes a list of periods and a list of values associated to these periods, and return a list of new periods and the list of
        values associated to these periods. Example: 
        merge(['08/2020', '09/2020', '10/2020', '11/2020'], [1,2,3,4]) returns ['08/2020-09/2020', '10/2020-11/2020'], [3, 7]'''
        if len(monthsL)%2 == 1:
            monthsL.append(TimeZones.nextMonth(monthsL[-1][-7:]))
            monthsV.append(0)
        
        shorterMonthsL, shorterMonthsV = [], []
        for i in range(0, len(monthsV), 2):
            shorterMonthsL.append(monthsL[i][:7] + '-' + monthsL[i+1][-7:])
            shorterMonthsV.append(monthsV[i] + monthsV[i+1])
        return shorterMonthsL, shorterMonthsV

    def endsWithAnEmptyPeriod(self):
        for dict in self.dataSets:
            if dict['data'][-1] != 0:
                return False
        return True

    def removeEmptyPeriods(self):
        while self.endsWithAnEmptyPeriod():
            self.monthsList = self.monthsList[:-1]
            for dic in self.dataSets:
                dic['data'] = dic['data'][:-1]

    def updateBiggestDiscussion(self, month, discussionName, amountOfMessagesThisMonth):
        if month not in self.biggestDiscussionByMonths:
            self.biggestDiscussionByMonths[month] = (discussionName, amountOfMessagesThisMonth)
            return
        if amountOfMessagesThisMonth > self.biggestDiscussionByMonths[month][1]:
            self.biggestDiscussionByMonths[month] = (discussionName, amountOfMessagesThisMonth)

    def generateDataSet(self):
        ''' Generates all the data required to write the file'''
        dataSets = []
        self.allMonthsList = TimeZones.generateMonthsFrom(datetime.datetime.fromtimestamp(self.data.mostAncientDiscussion[1]/1000).strftime("%m/%Y"))
        self.generateColors(len(self.discussions))

        for discussion in self.discussions:
            #print(f"{discussion.title}: {len(discussion.messagesList)}, {discussion.discussionSizePerDay}")
            monthsList = self.allMonthsList
            discussionDict = {'label': discussion.title}
            monthsData = []
            idays, imonths, sumMonth = 0, 0, 0
            keysList, valuesList = list(discussion.discussionSizePerDay.keys()), list(discussion.discussionSizePerDay.values())
            day, msgAmount = keysList[0], valuesList[0]


            # On itère sur les mois, on fixe leur valeur à 0 tant qu'on n'a pas atteint le mois du 1er jour de discussion
            while TimeZones.monthIsSuperior(day[3:], monthsList[imonths]):
                monthsData.append(0)
                imonths += 1
            
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
                    # We're changing month
                    self.updateBiggestDiscussion(monthsList[imonths], discussion.title, sumMonth)
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
        dataSets = self.removeEmptyPeriods()
        
        #print(dataSets, monthsList)

    def writeBestDiscThroughTime(self):
    # Crée une chaîne HTML de début
        html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Discussions les plus actives chaque mois</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #ffcce7;  
                margin: 20px;
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                align-items: flex-start;  
            }
            h1 {
                color: #333333;
                text-align: center;
                width: 100%;  
            }
            .bubble {
                background-color: #daf2dc;
                color: #154360;
                border-radius: 20px;  
                width: auto;  
                max-width: 200px;
                padding: 8px;
                height: 80px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                margin: 10px;
                overflow: hidden; 
            }
            .bubble:nth-child(2n) {
                background-color: #81b7d2;  
                margin-top: 50px;
            }
        </style>
    </head>
    <body>
        <h1>Discussions les plus actives chaque mois</h1>
    '''

        # Ajoute chaque bulle à la page
        for key, values in self.biggestDiscussionByMonths.items():
            if values[1] != 0:
                html_content += f'''
                    <div class="bubble">
                        <div>{key}</div>
                        <div>{values[0]}</div>
                        <div>{values[1]}</div>
                    </div>
                '''

        # Ajoute la fin de la structure HTML
        html_content += '''
        </body>
        </html>
        '''

        # Écrit le contenu dans un fichier HTML
        with open(os.path.join(self.filesManager.menusPath, "BestDiscussions.html"), 'w', encoding='utf-8') as htmlFile:
            htmlFile.write(html_content)

    def writeTimeZones(self):
        ''' Writes the file that contains the graph of the Conversations' sizes Evolution throught time'''
        self.generateDataSet()
        with open(os.path.join(self.filesManager.menusPath, 'convEvolution.html'), 'w', encoding="utf-8") as writingFile:
            writingFile.write(self.generateOutput())

    def generateOutput(self):
        ''' Returns the HTML code for the graph of the Conversations' sizes Evolution throught time'''
        return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Évolution des conversations</title>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        h1 {{
            text-align: center;
            color: #333333;
        }}
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
    <canvas id="myChart" width="400" height="200"></canvas>
</div>

<script>
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

    var ctx = document.getElementById('myChart').getContext('2d');

    var myChart = new Chart(ctx, {{
        type: 'line',
        data: data,
        options: options
    }});
</script>

</body>
</html>
'''