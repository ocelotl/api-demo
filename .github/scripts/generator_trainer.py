from transformers import T5Tokenizer, T5ForConditionalGeneration
from torch.utils.data import DataLoader, TensorDataset
from torch import optim, device, cuda, no_grad
from sklearn.model_selection import train_test_split
from google.colab import drive
from pathlib import Path
from json import load

drive.mount('/content/drive')

verb = "may"

sentence_generator_path = (
    Path(f"content/drive/My Drive/{verb}_sentence_generator")
)

with (
    open(sentence_generator_path.joinpath(f"{verb.upper()}_1000.json")) as
    sentence_pairs_file
):
    sentence_pairs = load(sentence_pairs_file)

informal_sentences = [sentence_pair[0] for sentence_pair in sentence_pairs]
formal_sentences = [sentence_pair[1] for sentence_pair in sentence_pairs]

# Tokenize the sentences
tokenizer = T5Tokenizer.from_pretrained("t5-base")
tokenized_inputs = tokenizer(
    informal_sentences, return_tensors="pt", padding=True, truncation=True
)
tokenized_targets = tokenizer(
    formal_sentences, return_tensors="pt", padding=True, truncation=True
)

# Split the dataset
input_ids_train, input_ids_val, target_ids_train, target_ids_val = (
    train_test_split(
        tokenized_inputs["input_ids"],
        tokenized_targets["input_ids"],
        test_size=0.1,
        random_state=42
    )
)

# Create DataLoader for training and validation
train_dataset = TensorDataset(input_ids_train, target_ids_train)
val_dataset = TensorDataset(input_ids_val, target_ids_val)
train_dataloader = DataLoader(train_dataset, batch_size=4, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=4, shuffle=False)

# Model initialization
model = T5ForConditionalGeneration.from_pretrained("t5-base")

# Training loop
optimizer = optim.AdamW(model.parameters(), lr=5e-5)
device = device("cuda" if cuda.is_available() else "cpu")
model.to(device)

num_epochs = 3
for epoch in range(num_epochs):
    model.train()
    for batch in train_dataloader:
        input_ids, target_ids = batch
        input_ids, target_ids = input_ids.to(device), target_ids.to(device)

        optimizer.zero_grad()
        outputs = model(input_ids=input_ids, labels=target_ids)
        loss = outputs.loss
        loss.backward()
        optimizer.step()

    # Validation
    model.eval()
    with no_grad():
        total_loss = 0
        for batch in val_dataloader:
            input_ids, target_ids = batch
            input_ids, target_ids = input_ids.to(device), target_ids.to(device)

            outputs = model(input_ids=input_ids, labels=target_ids)
            total_loss += outputs.loss.item()

        avg_loss = total_loss / len(val_dataloader)
        print(f"Epoch {epoch + 1}/{num_epochs}, Validation Loss: {avg_loss}")

model.save_pretrained(str(sentence_generator_path))

# Example usage to generate formal normative sentence
informal_input = "Close the window."
tokenized_input = tokenizer(
    informal_input,
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

formal_output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
print("Formal normative sentence:", formal_output)
