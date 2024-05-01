import model
import os
import torch
import json
import time

program_start_time = time.perf_counter()

# Stage 1: Initialize model
init_model_start_time = time.perf_counter()
model = model.Model()
init_model_end_time = time.perf_counter()
print(f"Initializing model took {init_model_end_time - init_model_start_time:.2f} seconds")

unittests = []
unittest_code_text = {}
unittest_text_embeddings = {}

# Stage 2: Load unit tests from directory
load_unittests_start_time = time.perf_counter()
for file in os.listdir("unittests"):
    with open(os.path.join("unittests", file), "r") as f:
        unittest = f.read()
        unittests.append(unittest)
        code_text = model.summarize_unittests(unittest)
        text_embedding = torch.tensor(model.encode_paragraph(code_text))
        unittest_code_text[unittest] = code_text
        unittest_text_embeddings[unittest] = text_embedding
load_unittests_end_time = time.perf_counter()
print(f"Loading unit tests took {load_unittests_end_time - load_unittests_start_time:.2f} seconds")

get_input_start_time = time.perf_counter()
flag = int(input("Enter 1 for text similarity or 2 for code similarity: "))
get_input_end_time = time.perf_counter()
print(f"Getting user input took {get_input_end_time - get_input_start_time:.2f} seconds")

if flag == 1:
    # Stage 3: Text similarity
    text = input("Enter the text: ")
    text_similarity_start_time = time.perf_counter()
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
    text_similarity_end_time = time.perf_counter()
    print(f"Text similarity took {text_similarity_end_time - text_similarity_start_time:.2f} seconds")
elif flag == 2:
    # Stage 3: Code similarity
    code_input = input("Enter the code: ")
    code_similarity_start_time = time.perf_counter()
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
    code_similarity_end_time = time.perf_counter()
    print(f"Code similarity took {code_similarity_end_time - code_similarity_start_time:.2f} seconds")

program_end_time = time.perf_counter()
print(f"Total execution time: {program_end_time - program_start_time:.2f} seconds")