# boom_bot.py

from os import environ
from github import Github


def check_pull_request(repo, pr_number):
    pr = repo.get_pull(pr_number)
    files = pr.get_files()

    for file in files:
        if file.filename.endswith('.rst'):
            content = file.raw_data.decode('utf-8')
            lines = content.split('\n')

            for i, line in enumerate(lines, start=1):
                if line.strip().startswith('BOOM'):
                    comment = f"BOOM found in line {i}"
                    pr.create_issue_comment(comment)


if __name__ == "__main__":
    # Replace 'your_token' with your GitHub token
    g = Github('your_token')
    repo = g.get_repo('ocelotl/api-demo')
    pr_number = 1  # Replace with the actual pull request number

    check_pull_request(repo, environ.get("GITHUB_REF").split("/")[2])
