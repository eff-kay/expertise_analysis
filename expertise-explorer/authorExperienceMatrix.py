
import json
import pickle
mapIds = {}

def countAuthor(author):
    allKeys = list(map(lambda x: x[0], mapIds.keys()))
    keyWithAuthor = [k for k in allKeys if k==author]
    return len(keyWithAuthor)

def getIssues():

    with open("../projectData/authorCommit.txt", 'r') as f:
        lines = f.readlines()

        for line in reversed(lines):
            author, commit= line.strip().split("&=&")
            mapIds[(author, commit)]= countAuthor(author)+1

    with open('../projectData/authorExperienceMatrix.p', 'wb') as w:
        pickle.dump(mapIds, w)

def getLines():
    with open("Repo/hadoop/test.txt", 'r') as f:
        lines = f.readlines()

        experienceMatrix=[]

        for line in lines:
            if line[0].isalpha():
                splitLine = line.split("&=&")
                author, commit = splitLine[0],splitLine[1]

            if not line[0].isalpha() and line[0] not in '\n':
                print(line)
                splitLine = line.split(" ")
                filesTouched, linesAdded = splitLine[1], splitLine[4]
                if splitLine[5][0]!='i':
                    linesAdded=0


                experienceMatrix.append([author, commit, linesAdded])

    with open('../projectData/authorExperienceLinesMatrix.p', 'wb') as w:
        pickle.dump(experienceMatrix, w)

if __name__=="__main__":
    # getLines()

    # with open('../projectData/authorExperienceMatrix.p', 'rb') as r:
    #     diffMatrix = pickle.load(r)
    #
    # with open('../projectData/authorExperienceLinesMatrix.p', 'rb') as r:
    #     lineMatrix = pickle.load(r)
    #
    # lDiffMatrix = list(diffMatrix)
    # for i in range(len(lDiffMatrix)):
    #     if lDiffMatrix[i]!=lineMatrix[i]:
    #         print(lDiffMatrix[i], lineMatrix[i])


    with open("Repo/hadoop/test.txt", 'r') as f:
        lines = f.readlines()


