import pickle
from collections import namedtuple
AuthorCommitTuple = namedtuple('AuthorCommitTuple', ('author', 'commit'))




if __name__=="__main__":

    defectMatrix=[]
    with open('../projectData/defectAuthorRelation.p','rb') as r:
        defectMap = pickle.load(r)
        print(len(defectMap.items()))

        for parentCommit, fileDict in defectMap.items():
                for fileName, listOfLines in fileDict.items():
                    for line, author, buggyCommit in listOfLines:
                        print(parentCommit, fileName, line, " ".join(author), buggyCommit)
                        defectMatrix.append([parentCommit, fileName, line, " ".join(author), buggyCommit])



    with open('../projectData/defectAuthorMatrix.p','wb+') as w:
        pickle.dump(defectMatrix, w)


