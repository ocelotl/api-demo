# boom_bot.py

from os import environ
from github import Github
from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification
)
import torch
from pathlib import Path

sentence_classifier_path = str(Path(__file__))

# Load model and tokenizer from disk
model = DistilBertForSequenceClassification.from_pretrained(
    sentence_classifier_path
)
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

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

            lines = file.patch.split("\n")

            for index, line in enumerate(lines):
                if (
                    line.startswith("+") and
                    len(line) > 1 and
                    line[1:].startswith("boom")
                ):
                    # Tokenize the input sentence
                    input_sentence = line[1:]
                    tokenized_input = tokenizer(
                        input_sentence, return_tensors='pt'
                    )

                    # Perform inference
                    with torch.no_grad():
                        output = model(**tokenized_input)

                    # Get the predicted class
                    predicted_class = torch.argmax(output.logits, dim=1).item()
                    # https://pygithub.readthedocs.io/en/v2.2.0/github_objects/PullRequest.html?highlight=create_review#github.PullRequest.PullRequest.create_review_comment

                    if predicted_class == 0:
                        continue

                    if predicted_class == 1:
                        modal_verb = "MAY"

                    if predicted_class == 2:
                        modal_verb = "MUST"

                    message = (
                        f"This sentence can be rewritten using {modal_verb}"
                    )

                    pr.create_review_comment(
                        message,
                        pr.get_commits()[pr.commits - 1],
                        file.filename,
                        line=index,
                        side="RIGHT"
                    )


if __name__ == "__main__":
    g = Github(environ.get("GITHUB_TOKEN"))
    repo = g.get_repo('ocelotl/api-demo')

    check_pull_request(repo, int(environ.get("GITHUB_REF").split("/")[2]))
    # check_pull_request(repo, 2)
