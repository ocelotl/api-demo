# boom_bot.py

from os import environ
from github import Github

{
    'sha': '681ac7d78883f0570ec96385092d30402a030f70',
    'filename': 'README.rst',
    'status': 'modified',
    'additions': 5,
    'deletions': 0,
    'changes': 5,
    'blob_url': (
        'https://github.com/ocelotl/api-demo/blob/'
        '9b03defde2fe11040b17618a9626102f7d00fbdf/README.rst'
    ),
    'raw_url': (
        'https://github.com/ocelotl/api-demo/raw/'
        '9b03defde2fe11040b17618a9626102f7d00fbdf/README.rst'
    ),
    'contents_url': (
        'https://api.github.com/repos/ocelotl/api-demo/contents/'
        'README.rst?ref=9b03defde2fe11040b17618a9626102f7d00fbdf'
    ),
    'patch': (
        '@@ -1,2 +1,7 @@'
        '\n API Demo'
        '\n ========'
        '\n+'
        '\n+boom asdfasdf'
        '\n+sdfsdf'
        '\n+boom asdfasd'
        '\n+boom'
    )
}


def check_pull_request(repo, pr_number):
    pr = repo.get_pull(pr_number)
    files = pr.get_files()

    for file in files:
        if file.filename.endswith('.rst'):
            for line in [
                line[1:] for line in file.patch.split("\n") if
                line.startswith("+") and
                len(line) > 1
            ]:

                if line.strip().startswith('boom'):
                    pr.create_issue_comment("boom found")


if __name__ == "__main__":
    # Replace 'your_token' with your GitHub token
    g = Github(environ.get("GITHUB_TOKEN"))
    repo = g.get_repo('ocelotl/api-demo')

    check_pull_request(repo, int(environ.get("GITHUB_REF").split("/")[2]))
    # check_pull_request(repo, 2)
