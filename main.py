import model
import os
import torch
import json
import time
import sys

# Function to initialize the model and measure the time it takes
def initialize_model():
    start_time = time.perf_counter()
    model_instance = model.Model()
    end_time = time.perf_counter()
    print(f"Initializing model took {end_time - start_time:.2f} seconds")
    return model_instance

# Function to load unit tests, summarize them, and encode the summaries
def load_unit_tests(model_instance):
    start_time = time.perf_counter()
    unittests = []
    unittest_code_text = {}
    unittest_text_embeddings = {}
    for file in os.listdir("unittests"):
        with open(os.path.join("unittests", file), "r") as f:
            unittest = f.read()
            unittests.append(unittest)
            code_text = model_instance.summarize_unittests(unittest)
            text_embedding = torch.tensor(model_instance.encode_paragraph(code_text))
            unittest_code_text[unittest] = code_text
            unittest_text_embeddings[unittest] = text_embedding
    end_time = time.perf_counter()
    print(f"Loading unit tests took {end_time - start_time:.2f} seconds")
    return unittests, unittest_code_text, unittest_text_embeddings

# Function to get user input and measure the time it takes
def get_user_input():
    start_time = time.perf_counter()
    flag = int(input("Enter 1 for text similarity or 2 for code similarity: "))
    end_time = time.perf_counter()
    print(f"Getting user input took {end_time - start_time:.2f} seconds")
    return flag

# Function to perform text similarity and measure the time it takes
def perform_text_similarity(model_instance, unittest_text_embeddings):
    text = input("Enter the text: ")
    start_time = time.perf_counter()
    text_embedding = torch.tensor(model_instance.encode_paragraph(text))
    paragraph_embeddings = torch.stack(list(unittest_text_embeddings.values()), dim=0)
    top_k_indices = model_instance.semantic_search(text_embedding.unsqueeze(0), paragraph_embeddings, 1)
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
    end_time = time.perf_counter()
    print(f"Text similarity took {end_time - start_time:.2f} seconds")

# Function to perform code similarity and measure the time it takes
def perform_code_similarity(model_instance, unittest_text_embeddings):
    code_input = input("Enter the code: ")
    start_time = time.perf_counter()
    code_embedding = torch.tensor(model_instance.encode_paragraph(model_instance.summarize_unittests(code_input)))
    paragraph_embeddings = torch.stack(list(unittest_text_embeddings.values()), dim=0)
    top_k_indices = model_instance.semantic_search(code_embedding.unsqueeze(0), paragraph_embeddings, 1)
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
    end_time = time.perf_counter()
    print(f"Code similarity took {end_time - start_time:.2f} seconds")

# Main function to orchestrate the program
def main(flag=None, input_text=None, input_code=None):
    program_start_time = time.perf_counter()
    model_instance = initialize_model()
    unittests, unittest_code_text, unittest_text_embeddings = load_unit_tests(model_instance)

    if flag is None:
        flag = get_user_input()

    if flag == 1:
        if input_text is None:
            input_text = input("Enter the text: ")
        perform_text_similarity(model_instance, unittest_text_embeddings, input_text)
    elif flag == 2:
        if input_code is None:
            input_code = input("Enter the code: ")
        perform_code_similarity(model_instance, unittest_text_embeddings, input_code)

    program_end_time = time.perf_counter()
    print(f"Total execution time: {program_end_time - program_start_time:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        flag = int(sys.argv[1])
        if flag == 1:
            input_text = sys.argv[2] if len(sys.argv) > 2 else None
            input_code = None
        elif flag == 2:
            input_code = sys.argv[2] if len(sys.argv) > 2 else None
            input_text = None
        main(flag, input_text, input_code)
    else:
        main()