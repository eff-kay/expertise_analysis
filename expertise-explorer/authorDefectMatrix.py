import pickle
from collections import namedtuple
from repoExecutor import *
from filterIssues import *


AuthorCommitTuple = namedtuple('AuthorCommitTuple', ('author', 'commit'))

def createDefectMatrix(project):
    defectMatrix=[]
    with open('../projectData/defectAuthorRelationFor'+project+'.p','rb') as r:
        defectMap = pickle.load(r)
        print(len(defectMap.items()))

        for parentCommit, fileDict in defectMap.items():
                for fileName, listOfLines in fileDict.items():
                    for line, author, buggyCommit in listOfLines:
                        defectMatrix.append([parentCommit, fileName, line, " ".join(author), buggyCommit])

    with open('../projectData/defectAuthorMatrixFor'+project+'.p','wb+') as w:
        pickle.dump(defectMatrix, w)

def createDefectMatrixFromMap(defectMap, project):
    defectMatrix=[]

    for parentCommit, fileDict in defectMap.items():
            for fileName, listOfLines in fileDict.items():
                for line, author, buggyCommit in listOfLines:
                    print(parentCommit, fileName, line, " ".join(author), buggyCommit)
                    defectMatrix.append([parentCommit, fileName, line, " ".join(author), buggyCommit])

    with open('../projectData/defectAuthorMatrixFor'+project+'.p','wb+') as w:
        pickle.dump(defectMatrix, w)

import os
if __name__=="__main__":
    fileName= 'YARN1000'
    projectName='YARN'
    issues = getResolvedIssuesFromFile(fileName)
    print(len(issues))
    filteredIssues = filterGitLog(issues, '../projectData/issueList.json', projectName)
    print(len(filteredIssues))
    writeToFile(fileName, filteredIssues)

    bugMap = createBugMap(fileName)
    print(len(bugMap.items()))
    createDefectMatrixFromMap(bugMap, fileName)
    print('done')



