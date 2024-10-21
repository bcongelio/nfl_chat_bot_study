from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset
import os
import torch

### checking if CUDA is avaliable and set the GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load the model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name).to(device)

# Set the padding token
tokenizer.pad_token = tokenizer.eos_token

# Load the dataset
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
dataset_path = os.path.join(parent_dir, 'nfl_analytics_test', 'nfl_dataset.json')

if os.path.exists(dataset_path):
    dataset = load_dataset('json', data_files=dataset_path)
    ### data is likely(???) wrapped in a DatasetDict, so I need to access the 'train' split
    if isinstance(dataset, dict) and 'train' in dataset:
        dataset = dataset['train']
else:
    raise FileNotFoundError(f"Dataset not found at {dataset_path}. Please check the file path.")

print(f"Dataset loaded with {len(dataset)} entries.")
print(f"First entry: {dataset[0]}")

### prepare the dataset for language modeling
def prepare_train_features(examples):
    # Combine question and answer
    texts = [q + " " + a for q, a in zip(examples["question"], examples["answer"])]
    
    ### tokenize the texts
    tokenized = tokenizer(texts, truncation=True, padding="max_length", max_length=512)
    
    ### prepare the labels (same as input_ids for language modeling)
    tokenized["labels"] = tokenized["input_ids"].copy()
    
    return tokenized

tokenized_dataset = dataset.map(prepare_train_features, batched=True, remove_columns=dataset.column_names)

### data collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

### Set up training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    save_steps=10_000,
    save_total_limit=2,
    prediction_loss_only=True,
    fp16 = True,
)

### create trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator,
)

# Start training
trainer.train()

output_dir = "./nfl_analytics_model"
model.save_pretained(output_dir)
tokenizer.save_pretrained(output_dir)
print(f"Model saved to {output_dir}")
