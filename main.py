import os
global userName, dirPaths

from code.html import *
from code.utilitaries import *
from code.treatment import *

''' Trouve les chemins des dossiers inbox.
Attention: ce fichier doit se trouver à la racine du dossier instaData.'''
def find_inbox_directories():
    inbox_directories = []
    path = getCurrentDirPath(__file__)
    for root, dirs, files in os.walk(path):
        if "inbox" in dirs:
            inbox_directory = os.path.join(root, "inbox")
            inbox_directories.append(inbox_directory)
    return inbox_directories


# On crée les différents dossiers et on stocke leurs chemins dans le dictionnaire dirPaths
dirPaths = create_dirs(getCurrentDirPath(__file__))

# Initialisation des variables : 
# wordCounterDic: associe à chaque mot employé le nombre d'emplois
# conversationSizeDic: associe à chaque conversations le nombre de messages envoyés sous forme de tuple (utilisateur, reste de la conv.)
# conversationAgeDic: associe à chaque conversation son âge (datetime)
# usersInfoDic: associe à chaque nom de fichier le nom d'utilisateur associé
# sentMsgTimeTableDic, receivedMsgTimeTableDic: associe à chaque heure de la journée les nombres de messages envoyés et reçus
# conversationMaxStreakDic: associe à chaque conversation sa plus grande série de jours de discussion
# amountOfParticipantsDic: associe à chaque conversation son nombre de participants
wordCounterDic, conversationSizeDic, conversationAgeDic, usersInfoDic, sentMsgTimeTableDic, receivedMsgTimeTableDic  = {}, {}, {}, {}, {}, {}
conversationMaxStreakDic, complicityScoreDic, amountOfParticipantsDic, amountOfMessPerDayDic = {}, {}, {}, {}
inbox_directories = find_inbox_directories()
username = get_self_username(inbox_directories)

jsonList = getAllConversationFiles(inbox_directories)

treatment(jsonList, username, wordCounterDic, sentMsgTimeTableDic, receivedMsgTimeTableDic, amountOfParticipantsDic)

for inbox_directory in inbox_directories:
    for root, dirs, files in os.walk(inbox_directory):
            dirName = os.path.basename(root)
            jsonList = []
            for file_name in files:
                if file_name.endswith(".json"):
                    file_path = os.path.join(root, file_name)
                    jsonList.append(file_path)
            if jsonList:
                ConversationTreatment(jsonList, conversationSizeDic, wordCounterDic, conversationAgeDic, dirName, usersInfoDic, username, dirPaths, conversationMaxStreakDic, amountOfMessPerDayDic)

computeComplicityScores(complicityScoreDic, amountOfParticipantsDic, conversationAgeDic, conversationSizeDic, conversationMaxStreakDic)

generate_html(orderDic(mergeDic(conversationSizeDic)), "messageCount.html", "Top conversations.", dirPaths)

generate_html(orderDic(wordCounterDic), "wordCounter.html", "Mots les plus utilisés", dirPaths)

sortedConversationAge = orderDic(conversationAgeDic, False)
for key in sortedConversationAge:
    sortedConversationAge[key] = convertTimestamp(sortedConversationAge[key])
generate_html(sortedConversationAge, "convAge.html", "Age des conversations", dirPaths)

generateConvMenu(usersInfoDic, dirPaths)

generateAccountData(username, complicityScoreDic, conversationAgeDic, conversationSizeDic, conversationMaxStreakDic, sentMsgTimeTableDic, receivedMsgTimeTableDic, amountOfMessPerDayDic, sentMsgTimeTableDic, os.path.join(dirPaths['Menus'], "accountData.html"))

generate_index(dirPaths, username)
