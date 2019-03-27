import subprocess
import os

import whatthepatch

HADOOP_GIT_COMMAND = "git clone https://gitbox.apache.org/repos/asf/hadoop.git"
class RepoExecutor:
    CLONE_REPO = {
        'hadoop': HADOOP_GIT_COMMAND,
    }

    SAVE_CURRENT_WORKING_DIRECTORY = 'CURR_DIR=$PWD'
    GO_BACK_TO_WORKING_DIRECTORY = 'cd $CURR_DIR'

    def __init__(self, repo_name):
        self.repo_name = repo_name

        if not os.path.isfile(f'./Repo'):
            subprocess.run('mkdir Repo', shell=True)
            print("creating Repo dir")

        if not os.path.isdir(f'./Repo/{self.repo_name}'):
            subprocess.run(";".join([
                self.SAVE_CURRENT_WORKING_DIRECTORY,
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


def get_patch(commit_hash, parent_commit_hash):
    repo_name = 'hadoop'
    return RepoExecutor(repo_name).execute(
        f'git diff {commit_hash} {parent_commit_hash}'
    )

if __name__=="__main__":
    
    patch = get_patch('e92107b18f82b3501deaa6170d322a0fb512ec71', 'e2d46ac5a4b50a19ba1075c6b32147e81088d6ec')
    for diff in whatthepatch.parse_patch(patch):
        fileName = diff.header.old_path.split('/')[-1]
        print(fileName)