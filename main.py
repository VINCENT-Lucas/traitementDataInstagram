import datetime, time

import os
import json
from collections import Counter
global userName, dirPaths

from code.html import *
from code.utilitaries import *
from code.treatment import *



'''//TODO
- All done :)
05/07/2023, VINCENT Lucas
'''

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

# Initialisation des variables
wordCounterDic, messageAmountDic, conversationAgeDic, usersInfoDic, sentMsgTimeTableDic, receivedMsgTimeTableDic  = {}, {}, {}, {}, {}, {}
inbox_directories = find_inbox_directories()
username = get_self_username(inbox_directories)

jsonList = getAllConversationFiles(inbox_directories)

treatment(jsonList, username, wordCounterDic, sentMsgTimeTableDic, receivedMsgTimeTableDic)

for inbox_directory in inbox_directories:
    for root, dirs, files in os.walk(inbox_directory):
            dirName = os.path.basename(root)
            jsonList = []
            for file_name in files:
                if file_name.endswith(".json"):
                    file_path = os.path.join(root, file_name)
                    jsonList.append(file_path)
            if jsonList:
                ConversationfilesProcess(jsonList, messageAmountDic, wordCounterDic, conversationAgeDic, dirName, usersInfoDic, username, dirPaths)

sortedMessAmount = dict(sorted(messageAmountDic.items(), key=lambda x: x[1], reverse=True))
title = "Top conversations."
generate_html(sortedMessAmount, "messageCount.html", title, dirPaths)

title = "Mots les plus utilisés"
sortedWord_counter = orderDic(wordCounterDic)
generate_html(sortedWord_counter, "wordCounter.html", title, dirPaths)

title = "Age des conversations"
sortedConversationAge = orderDic(conversationAgeDic, False)
for key in sortedConversationAge:
    sortedConversationAge[key] = convert_timestamp(sortedConversationAge[key])
generate_html(sortedConversationAge, "convAge.html", title, dirPaths)

generate_conv_menu(usersInfoDic, dirPaths)

generateTimeTable(sentMsgTimeTableDic, receivedMsgTimeTableDic, os.path.join(dirPaths['Menus'], "accountData.html"))

generate_index(dirPaths, username)
