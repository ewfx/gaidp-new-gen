import traceback
import PyPDF2
import faiss
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
from generateValidationFunctions import process_rules_file
import os

# Define the results directory
RESULTS_DIR = "results"

# Ensure the directory exists
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)  # Create directory if it doesn't exist
    
# -------------------------------------- PDF Q&A (RAG) --------------------------------------

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HF_TOKEN = "paste_your_hugging_face_access_key"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF"""
    try:
        text = ""
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
        return text.strip()
    except Exception as e:
        return f"❌ Error reading PDF: {traceback.format_exc()}"

def split_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def build_faiss_index(chunks):
    dimension = 384
    index = faiss.IndexFlatL2(dimension)
    embeddings = [embed_model.encode(chunk) for chunk in chunks]
    embeddings = np.array(embeddings).astype('float32')
    index.add(embeddings)
    return index, embeddings, chunks

def retrieve_relevant_chunks(query, index, chunks, embeddings, top_k=3):
    query_embedding = embed_model.encode(query).astype('float32')
    _, idxs = index.search(np.array([query_embedding]), top_k)
    return "\n".join([chunks[i] for i in idxs[0]])

def query_llm(context, query):
    """Query LLM and return response"""
    try:
        # prompt = f"Question: {query}\n\nAnswer:"
        prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 800, "temperature": 0.7}})
        return response.json()[0]["generated_text"]
    except Exception as e:
        return f"❌ Error querying LLM: {traceback.format_exc()}"
    
def extract_rules(response, filename="rules.txt"):
    """Extracts rules from LLM response and saves them to a file."""
       
    # Define full file path
    file_path = os.path.join(RESULTS_DIR, filename)

    write_flag = False
    rules = []

    for line in response.split("\n"):
        line = line.strip()

        if "Answer:" in line:
            write_flag = True
            continue  # Skip the "Answer:" line itself

        if write_flag and line and line[0].isdigit():  # Ensure it's a numbered rule
            rules.append(line)

    if rules:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("\n".join(rules))
            print(f"✅ Rules saved to: {file_path}")
        except Exception as e:
            print(f"❌ Error saving rules file: {str(e)}")
    else:
        print("❌ No rules found to save.")


def process_pdf_and_ask(pdf_file, question):
    """Process PDF and return answer"""
    try:
        text = extract_text_from_pdf(pdf_file)
        if text.startswith("❌"):
            return text  # Return error message if PDF reading fails
        chunks = split_text(text)
        index, embeddings, chunk_list = build_faiss_index(chunks)
        relevant_chunks = retrieve_relevant_chunks(question, index, chunk_list, embeddings)
        response = query_llm(relevant_chunks, question)
        extract_rules(response)
        process_rules_file(os.path.join(RESULTS_DIR, "rules.txt"))
        return response
    except Exception as e:
        return f"❌ Error processing PDF: {traceback.format_exc()}"
