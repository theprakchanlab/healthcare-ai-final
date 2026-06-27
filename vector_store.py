# vector_store.py
# FAISS memory — stores patient records so AI can search them

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from patients import PATIENTS

# Only use this specific Mac/Windows fix if running locally
if not os.environ.get("STREAMLIT_RUNTIME_CHECK"):
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

load_dotenv()

def build_vector_store():
    """
    Converts patient records into vector embeddings
    and stores them in FAISS for fast AI search
    """
    print("Building patient memory (FAISS)...")

    # Convert each patient record into a Document object
    documents = []
    for pid, data in PATIENTS.items():
        # Combine all patient info into one text block
        text = f"""
        Patient ID: {pid}
        Name: {data['name']}
        Age: {data['age']}
        Disease: {data['disease']}
        Assigned Doctor: {data['doctor']}
        Medical History: {data['history']}
        """
        documents.append(
            Document(
                page_content=text,
                metadata={"patient_id": pid, "name": data["name"]}
            )
        )

    print("Creating OpenAI embeddings...")
    
    # DYNAMIC API KEY LOOKUP: Checks .env locally first, then Streamlit Secrets on cloud
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("Critical Error: OPENAI_API_KEY could not be found!")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=api_key
    )
    print("Embeddings object created...")

    # Build FAISS index from documents
    vector_store = FAISS.from_documents(documents, embeddings)
    
    print("FAISS index created...")
    print(f"Memory built! {len(documents)} patient records stored.")
    return vector_store


def search_patient_memory(vector_store, query):
    """
    Search for a patient using natural language
    Example: search_patient_memory(store, "kidney disease patient")
    """
    results = vector_store.similarity_search(query, k=1)
    if results:
        return results[0].page_content
    return "No matching patient found."


# Test it directly
if __name__ == "__main__":
    store = build_vector_store()

    print("\n--- Testing search ---")
    result = search_patient_memory(store, "kidney disease patient")
    print("Search result:", result)

    print("\n--- Day 2 complete! FAISS memory is working ---")
