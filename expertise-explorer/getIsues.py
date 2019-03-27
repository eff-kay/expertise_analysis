
import json


mapIds = {}

def getIssues():


    with open("../Data/gitLog.txt", 'r') as f:
        lines = f.readlines()

        for line in lines:
            currHash, prevHash, msg = line.strip().split("&=&")
            splitMsg = msg.strip().split(" ")
            issueNum = splitMsg[0][:-1]

            if issueNum[:2] not in ('HA', "MA", "YA", "HD"):
                continue

            if currHash=='' or prevHash=='':
                continue

            if issueNum in mapIds.keys():
                mapIds[issueNum].append((currHash, prevHash))
            else:
                mapIds[issueNum]=[(currHash, prevHash)]


    with open('../Data/issueList.json', 'w+') as w:
        json.dump(mapIds, w)




if __name__=="__main__":
    getIssues()