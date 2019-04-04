import subprocess
import os
import json

import pickle

import whatthepatch

from collections import namedtuple

AuthorCommitTuple = namedtuple('AuthorCommitTuple', ('author', 'commit'))

HADOOP_GIT_COMMAND = "git clone https://gitbox.apache.org/repos/asf/hadoop.git"

class RepoExecutor:
    CLONE_REPO = {
        'hadoop': HADOOP_GIT_COMMAND,
    }

    SAVE_CURRENT_WORKING_DIRECTORY = 'CURR_DIR=$PWD'
    GO_BACK_TO_WORKING_DIRECTORY = 'cd $CURR_DIR'

    def __init__(self, repo_name):
        self.repo_name = repo_name

        if not os.path.isdir(f'./Repo/{self.repo_name}'):
            subprocess.run(";".join([
                self.SAVE_CURRENT_WORKING_DIRECTORY,
                f'mkdir Repo/',
                f'cd Repo/',
                self.CLONE_REPO[self.repo_name],
                self.GO_BACK_TO_WORKING_DIRECTORY,
            ]), shell=True)

        # print(f'{self.repo_name} exists in ./Repo/{self.repo_name}...')

    def execute(self, command):
        return subprocess.check_output(";".join([
            self.SAVE_CURRENT_WORKING_DIRECTORY,
            f'cd Repo/{self.repo_name}',
            command,
            self.GO_BACK_TO_WORKING_DIRECTORY,
        ]), shell=True).decode('utf-8')

    def execute_commands(self, commands):
        command = ";".join([
            self.SAVE_CURRENT_WORKING_DIRECTORY,
            f'cd Repo/{self.repo_name}',
            *commands,
            self.GO_BACK_TO_WORKING_DIRECTORY,
        ])

        return subprocess.run(command,
            shell=True, capture_output=True, check=True)



class GitCommands:
    GIT_CHECKOUT = 'git checkout'
    GIT_GET_HEAD_COMMIT = "git rev-parse HEAD"
    GIT_CHECKOUT_MASTER = "git checkout master"
    SAVE_CURRENT_WORKING_DIRECTORY = 'CURR_DIR=$PWD'
    GO_BACK_TO_WORKING_DIRECTORY = 'cd $CURR_DIR'

    GIT_LOG = "git log --format='%H'"

    repo_name="hadoop"


    def getHead(self):
        return subprocess.check_output(";".join([
            self.SAVE_CURRENT_WORKING_DIRECTORY,
            f'cd Repo/{self.repo_name}',
            f'git rev-parse HEAD',
            self.GO_BACK_TO_WORKING_DIRECTORY,
        ]), shell=True).decode('utf-8')


    def checkout(self, commit):
        checkoutCommand = "git checkout "+commit

        return subprocess.check_output(";".join([
            self.SAVE_CURRENT_WORKING_DIRECTORY,
            f'cd Repo/{self.repo_name}',
            checkoutCommand,
            self.GO_BACK_TO_WORKING_DIRECTORY,
        ]), shell=True).decode('utf-8')


    def gitBlameOnCommit(self, commit, file, startLine, endLine):
        checkoutStatus = self.checkout(commit)
        if checkoutStatus!=None:
            result = self.gitBlame(file, startLine, endLine)
            checkoutStatus = self.checkout('master')
            if checkoutStatus:
                return result
        return None


    def gitBlame(self, file, startLine, endLine):

        blameCommand = "git blame -p {} -L {},{}".format(file, startLine, endLine)

        return subprocess.check_output(";".join([
            self.SAVE_CURRENT_WORKING_DIRECTORY,
            f'cd Repo/{self.repo_name}',
            blameCommand,
            self.GO_BACK_TO_WORKING_DIRECTORY,
        ]), shell=True).decode('utf-8')

    def getDiff(self, commitHash, parentCommitHash):
        return RepoExecutor(self.repo_name).execute(
                    f'git diff {commitHash} {parentCommitHash}'
            )


    def parseGitBlame(self, text):
        print(text)
        returnHash = {}
        splitText = text.split("\n")
        firstLine = splitText[0]
        commitId = firstLine.split(" ")[0]

        secondLine = splitText[1]
        authorName = secondLine.split(" ")[1:]

        return [authorName, commitId]


def createBugMap(projectName):

    file = open('../projectData/filteredGitLogFor'+projectName+'.json', 'r')
    filteredGitLog = json.load(file)
    bugMap = {}

    GitCommands().checkout('master')

    count = 0
    for k,v in list(filteredGitLog.items())[:]:
        currentCommit, parentCommit = v[0]
        patch = GitCommands().getDiff(parentCommit, currentCommit)

        GitCommands().checkout(parentCommit)

        # print(getGitLog())
        # # print(checkoutMaster())
        # print(getHeadHash())
        for diff in whatthepatch.parse_patch(patch):
            fileName = diff.header.old_path.split('/')[-1]

            if fileName.split(".")[-1]=='java':
                if diff.changes==None:
                    continue
                for prevLine, currLine, text in diff.changes:
                    if currLine == None:
                        gitBlameText = GitCommands().gitBlame(diff.header.old_path, prevLine, prevLine)
                        if gitBlameText != None:
                            parsedData = GitCommands().parseGitBlame(gitBlameText)

                            if parentCommit not in bugMap:
                                bugMap[parentCommit] = {}


                            if diff.header.old_path not in bugMap[parentCommit]:
                                bugMap[parentCommit][diff.header.old_path] = [(prevLine, parsedData[0], parsedData[1])]
                            else:
                                bugMap[parentCommit][diff.header.old_path].append((prevLine, parsedData[0], parsedData[1]))


        GitCommands().checkout('master')

        count += 1
        print("current count is at {}".format(count))

    return bugMap


def writeBugMapToFile(bugMap, projectName):
    with open('../ProjectData/defectAuthorRelationFor'+projectName+'.p','wb') as w:
        pickle.dump(bugMap, w)

if __name__=="__main__":
    fileName = 'HDFS2000'
    bugMap = createBugMap(projectName)

    print(bugMap)
    # writeBugMapToFile(bugMap,projectName)

