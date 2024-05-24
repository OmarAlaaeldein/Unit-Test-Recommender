import os
import torch
import json
import time
import sys
import model
import faiss
import pickle
import hashlib

VECTOR_DIMENSION = 384  # sentence-transformers/multi-qa-MiniLM-L6-dot-v1 model has 384-dimensional embeddings

def initialize_model():
    start_time = time.perf_counter()
    model_instance = model.Model()
    end_time = time.perf_counter()
    return model_instance, end_time - start_time

def calculate_file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def load_existing_embeddings():
    if os.path.exists('unittest_embeddings.pkl'):
        with open('unittest_embeddings.pkl', 'rb') as f:
            data = pickle.load(f)
            if len(data) == 3:  # Check if the pickle file contains only three values
                unittest_code_text, unittest_text_embeddings, index = data
                file_hashes = {}  # Initialize file_hashes as an empty dictionary
            elif len(data) == 4:  # If the pickle file contains four values
                unittest_code_text, unittest_text_embeddings, index, file_hashes = data
            else:
                raise ValueError("Invalid pickle file format")
    else:
        unittest_code_text = {}
        unittest_text_embeddings = {}
        index = faiss.IndexFlatL2(VECTOR_DIMENSION)
        file_hashes = {}
    return unittest_code_text, unittest_text_embeddings, index, file_hashes

def save_embeddings(unittest_code_text, unittest_text_embeddings, index, file_hashes):
    with open('unittest_embeddings.pkl', 'wb') as f:
        pickle.dump((unittest_code_text, unittest_text_embeddings, index, file_hashes), f)

def load_unit_tests(model_instance):
    start_time = time.perf_counter()
    unittest_code_text, unittest_text_embeddings, index, file_hashes = load_existing_embeddings()
    
    current_files = set(os.listdir("unittests"))
    existing_files = set(file_hashes.keys())
    new_files = current_files - existing_files

    updated = False

    # Check for modified files
    for file in existing_files:
        file_path = os.path.join("unittests", file)
        if os.path.exists(file_path):
            current_hash = calculate_file_hash(file_path)
            if current_hash != file_hashes[file]:
                # File has changed, reprocess it
                with open(file_path, "r") as f:
                    unittest = f.read()
                    code_text = model_instance.summarize_unittests(unittest)
                    text_embedding = model_instance.encode_paragraph(code_text)
                    
                    if len(text_embedding) != VECTOR_DIMENSION:
                        raise ValueError(f"Expected embedding dimension {VECTOR_DIMENSION}, but got {len(text_embedding)}")
                    
                    unittest_code_text[file] = code_text
                    unittest_text_embeddings[file] = text_embedding
                    index.add(torch.tensor(text_embedding).unsqueeze(0).numpy())
                    file_hashes[file] = current_hash
                    updated = True

    # Process new files
    for file in new_files:
        file_path = os.path.join("unittests", file)
        current_hash = calculate_file_hash(file_path)
        with open(file_path, "r") as f:
            unittest = f.read()
            code_text = model_instance.summarize_unittests(unittest)
            text_embedding = model_instance.encode_paragraph(code_text)
            
            if len(text_embedding) != VECTOR_DIMENSION:
                raise ValueError(f"Expected embedding dimension {VECTOR_DIMENSION}, but got {len(text_embedding)}")
            
            unittest_code_text[file] = code_text
            unittest_text_embeddings[file] = text_embedding
            index.add(torch.tensor(text_embedding).unsqueeze(0).numpy())
            file_hashes[file] = current_hash
            updated = True

    if updated:
        save_embeddings(unittest_code_text, unittest_text_embeddings, index, file_hashes)
    
    end_time = time.perf_counter()
    return unittest_code_text, unittest_text_embeddings, index, end_time - start_time

def get_user_input():
    start_time = time.perf_counter()
    flag = int(input("Enter 1 for text similarity or 2 for code similarity: "))
    end_time = time.perf_counter()
    return flag, end_time - start_time

def perform_similarity(model_instance, index, unittest_text_embeddings, input_text, is_code):
    start_time = time.perf_counter()
    if is_code:
        input_embedding = model_instance.encode_paragraph(model_instance.summarize_unittests(input_text))
    else:
        input_embedding = model_instance.encode_paragraph(input_text)
        
    if len(input_embedding) != VECTOR_DIMENSION:
        raise ValueError(f"Expected input embedding dimension {VECTOR_DIMENSION}, but got {len(input_embedding)}")
    
    D, I = index.search(torch.tensor(input_embedding).unsqueeze(0).numpy(), 1)
    results = []
    
    for idx in I[0]:
        file = list(unittest_text_embeddings.keys())[idx]
        code_embedding = unittest_text_embeddings[file]
        similarity_score = torch.cosine_similarity(torch.tensor(input_embedding), torch.tensor(code_embedding), dim=0).item()
        results.append({
            'input': input_text,
            'candidate_code': file,
            'similarity_score': similarity_score
        })

    with open('results.txt', 'w') as f:
        json.dump(results, f, indent=4)
        
    end_time = time.perf_counter()
    return end_time - start_time

def main(flag=None, input_text=None, input_code=None):
    print(f"Flag: {flag}, Input Text: {input_text}, Input Code: {input_code}")  # Debugging output
    program_start_time = time.perf_counter()
    model_instance, model_init_time = initialize_model()
    unittest_code_text, unittest_text_embeddings, index, load_unit_tests_time = load_unit_tests(model_instance)

    if flag is None:
        flag, get_user_input_time = get_user_input()
    else:
        get_user_input_time = 0

    if flag == 1:
        if input_text is None:
            input_text = input("Enter the text: ")
        similarity_time = perform_similarity(model_instance, index, unittest_text_embeddings, input_text, is_code=False)
    elif flag == 2:
        if input_code is None:
            input_code = input("Enter the code: ")
        similarity_time = perform_similarity(model_instance, index, unittest_text_embeddings, input_code, is_code=True)

    program_end_time = time.perf_counter()
    total_execution_time = program_end_time - program_start_time
    print(f"Model init time: {model_init_time:.2f} seconds")
    print(f"Load unit tests time: {load_unit_tests_time:.2f} seconds")
    print(f"Get user input time: {get_user_input_time:.2f} seconds")
    print(f"Similarity computation time: {similarity_time:.2f} seconds")
    print(f"Total execution time: {total_execution_time:.2f} seconds")
    return model_init_time, load_unit_tests_time, get_user_input_time, similarity_time, total_execution_time

if __name__ == "__main__":
    if len(sys.argv) > 1:
        flag = int(sys.argv[1])
        if flag == 1:
            input_text = sys.argv[2] if len(sys.argv) > 2 else None
            input_code = None
        elif flag == 2:
            input_code = sys.argv[2] if len(sys.argv) > 2 else None
            input_text = None
        model_init_time, load_unit_tests_time, get_user_input_time, similarity_time, total_time = main(flag, input_text, input_code)
    else:
        main()
