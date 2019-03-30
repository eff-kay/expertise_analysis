
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




if __name__=="__main__":
    getIssues()

