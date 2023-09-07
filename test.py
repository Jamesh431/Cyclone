from github import Github
import os
import csv

profile_name = "Jamesh431"
acc_token = "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"

g = Github(acc_token)
user = g.get_user(profile_name)


def nab_repos(repo_name):
    os.makedirs(f'{profile_name}/', exist_ok=True)

    with open(f'{repo_name.full_name}.csv', "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Repository", "Commit ID", "Commit Comment"])

        for branch in repo.get_branches():
            for commits in repo.get_commits(sha=branch.commit.sha):
                csv_writer.writerow([repo.full_name, commits.sha, commits.commit.message
                                     ])


for repo in user.get_repos():
    nab_repos(repo)
