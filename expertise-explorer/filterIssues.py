
import pandas as pd
import json




def getResolvedIssuesFromFile(project):
    jsonFile = open('../projectData/resolvedIssuesFor'+project+".json", 'r')
    jsonRawData = jsonFile.read()
    jsonData = json.loads(jsonRawData)
    issues = pd.DataFrame(jsonData['issues'])
    return issues


def filterGitLog(resolvedIssues, filePath, projectName):
    gitLog = open(filePath, 'r')
    gitData = json.load(gitLog)
    filteredDict = {k: v for k, v in gitData.items() if k[:4] == projectName}
    gitIssues = pd.Series(list(filteredDict.keys()))

    a = []
    for x in resolvedIssues['key']:
        for y in gitIssues:
            if x == y:
                a.append(x)

    finalGitDict = {k: v for k, v in filteredDict.items() if k in a}
    return finalGitDict


def writeToFile(project, finalGitDict):
    with open("../projectData/filteredGitLogFor"+project+".json", 'w+') as f:
        json.dump(finalGitDict, f)

if __name__=="__main__":
    fileName= 'HDFS2000'
    projectName='HDFS'
    issues = getResolvedIssuesFromFile(fileName)
    print(len(issues))
    filteredIssues = filterGitLog(issues, '../projectData/issueList.json', projectName)
    print(len(filteredIssues))
    writeToFile(fileName, filteredIssues)
    # print(len(filteredIssues.items()))

    # with open("../projectData/filteredGitLogForHAD.json", 'r') as r:
    #     issueDict= json.load(r)
    #     print(len(issueDict.items()))



