from transformers import (
    T5ForConditionalGeneration,
    T5Config,
    T5Tokenizer
)
from torch import cuda, device
from google.colab import drive
from pathlib import Path

drive.mount("/content/drive")

verb = "may"

sentence_generator_path = (
    Path(f"/content/drive/My Drive/{verb}_sentence_generator")
)
tokenizer = T5Tokenizer.from_pretrained("t5-base")


# Load the configuration
config = T5Config.from_pretrained(sentence_generator_path)

# Load the model
model = T5ForConditionalGeneration.from_pretrained(
    sentence_generator_path, config=config
)

informal_sentences = [
    "The user is free to add more methods to the API",
    "The SDK can be implemented by the user or the admin",
    "It is optional for the user to deploy the application"
]

device = device("cuda" if cuda.is_available() else "cpu")

for informal_sentence in informal_sentences:
    tokenized_input = tokenizer(
        informal_sentence,
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    input_ids = tokenized_input["input_ids"].to(device)
    output_ids = model.generate(
        input_ids,
        max_length=50,
        num_beams=4,
        length_penalty=2.0,
        early_stopping=True
    )
    formal_sentence = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    print(informal_sentence)
    print(formal_sentence)
