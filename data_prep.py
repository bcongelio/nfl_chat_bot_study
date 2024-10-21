import nltk
from datasets import Dataset
from bs4 import BeautifulSoup
import os

### download needed nltk data
nltk.download('punkt_tab')

def prepare_data(book_docs_path, nflverse_docs_path):
    ### loading book content from html files
    book_content = ""
    for filename in os.listdir(book_docs_path):
        if filename.endswith('.html'):
            with open(os.path.join(book_docs_path, filename), 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                ### extracting text from html
                book_content += soup.get_text() + "\n\n"

    ### loading nflverse documentation
    nflverse_file = os.path.join(nflverse_docs_path, 'pbp_dictionary.html')
    with open(nflverse_file, 'r', encoding='utf-8') as f:
        nflverse_soup = BeautifulSoup(f.read(), 'html.parser')
        docs_content = nflverse_soup.get_text()

    ### combing the content
    full_content = book_content + "\n\n" + docs_content

    ### splitting into sentences
    sentences = nltk.sent_tokenize(full_content)

    ### create question-answer pairs (placeholder)
    qa_pairs = [{"question": f"What does this mean: {sent}", "answer": sent} for sent in sentences]

    ### creating the hugging face dataset
    dataset = Dataset.from_dict({
        "question": [pair["question"] for pair in qa_pairs],
        "answer": [pair["answer"] for pair in qa_pairs]
    })

    return dataset

### usage
current_dir = os.path.dirname(os.path.abspath(__file__))
book_docs_path = os.path.join(current_dir, 'book_docs')
nflverse_docs_path = os.path.join(current_dir, 'nflverse_docs')

dataset = prepare_data(book_docs_path, nflverse_docs_path)
print(f"Dataset created with {len(dataset)} entries.")

### save dataset to json
json_path = os.path.join(current_dir, 'nfl_dataset.json')
dataset.to_json(json_path)
print(f"Dataset saved to {json_path}")
