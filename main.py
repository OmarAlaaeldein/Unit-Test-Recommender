import model
import os
import torch
import json

model = model.Model()
unittests = []
unittest_code_text = {}
unittest_text_embeddings = {}

# Load unit tests from directory
for file in os.listdir("unittests"):
    with open(os.path.join("unittests", file), "r") as f:
        unittest = f.read()
        unittests.append(unittest)
        code_text = model.summarize_unittests(unittest)
        text_embedding = torch.tensor(model.encode_paragraph(code_text))
        unittest_code_text[unittest] = code_text
        unittest_text_embeddings[unittest] = text_embedding


flag = int(input("Enter 1 for text similarity or 2 for code similarity: "))

if flag == 1:
    text = input("Enter the text: ")
    text_embedding = torch.tensor(model.encode_paragraph(text))
    paragraph_embeddings = torch.stack(list(unittest_text_embeddings.values()), dim=0)
    top_k_indices = model.semantic_search(text_embedding.unsqueeze(0), paragraph_embeddings, 1)
    top_k_indices = [index['corpus_id'] for index in top_k_indices]
    results = []
    for index in top_k_indices:
        for code, code_embedding in unittest_text_embeddings.items():
            similarity_score = torch.cosine_similarity(code_embedding, paragraph_embeddings[index], dim=0)
            results.append({
                'prompt_text': text,
                'candidate_code': code,
                'similarity_score': similarity_score.item()
            })
    with open('results.txt', 'w') as f:
        json.dump(results, f, indent=4)
elif flag == 2:
    code_input = input("Enter the code: ")
    code_embedding = torch.tensor(model.encode_paragraph(model.summarize_unittests(code_input)))
    paragraph_embeddings = torch.stack(list(unittest_text_embeddings.values()), dim=0)
    top_k_indices = model.semantic_search(code_embedding.unsqueeze(0), paragraph_embeddings, 1)
    top_k_indices = [index['corpus_id'] for index in top_k_indices]
    results = []
    for index in top_k_indices:
        for code, code_embedding in unittest_text_embeddings.items():
            similarity_score = torch.cosine_similarity(code_embedding, paragraph_embeddings[index], dim=0)
            results.append({
                'prompt_code': code_input,
                'candidate_code': code,
                'similarity_score': similarity_score.item()
            })
    with open('results.txt', 'w') as f:
        json.dump(results, f, indent=4)
        