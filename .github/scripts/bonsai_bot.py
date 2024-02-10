from os import environ
from github import Github
from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification
)
from torch import argmax, no_grad
from pathlib import Path
from os.path import abspath


model = DistilBertForSequenceClassification.from_pretrained(
    str(Path(abspath(__file__)).parent)
)
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")


if __name__ == "__main__":

    pr = (
        Github(environ.get("GITHUB_TOKEN")).
        get_repo('ocelotl/api-demo').
        get_pull(int(environ.get("GITHUB_REF").split("/")[2]))
    )

    for file in pr.get_files():
        if file.filename.endswith('.md'):


            lines = file.patch.split("\n")

            for index, line in enumerate(lines):
                if (
                    line.startswith("+") and
                    len(line) > 1
                ):
                    input_sentence = line[1:]
                    tokenized_input = tokenizer(
                        input_sentence, return_tensors='pt'
                    )

                    with no_grad():
                        output = model(**tokenized_input)

                    predicted_class = argmax(output.logits, dim=1).item()

                    if predicted_class == 0:
                        continue

                    if predicted_class == 1:
                        modal_verb = "MAY"

                    if predicted_class == 2:
                        modal_verb = "MUST"

                    message = (
                        f"This sentence can be rewritten using {modal_verb}"
                    )

                    # https://pygithub.readthedocs.io/en/v2.2.0/github_objects/PullRequest.html?highlight=create_review#github.PullRequest.PullRequest.create_review_comment
                    pr.create_review_comment(
                        message,
                        pr.get_commits()[pr.commits - 1],
                        file.filename,
                        line=index - 2,
                        side="RIGHT"
                    )
