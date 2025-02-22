import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from data_preprocessing import get_chunks

docs, chunks = get_chunks()

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "" # Put your huggingface key

embedding_model = HuggingFaceEmbeddings(model_name ="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma(collection_name="vector_database", 
            embedding_function=embedding_model, 
            persist_directory="./chroma_db_")

def retrieval(user_query):
    retrieved_docs = db.similarity_search_with_score(user_query, k=3)
    context_text = "\n\n".join([doc.page_content for doc, _ in retrieved_docs])
    return context_text


if __name__ == "__main__":
    if not db.get()["ids"]:
        db.add_documents(chunks)
    
    stored_embeddings = db.get()["ids"]
    print(f"Successfully stored {len(stored_embeddings)} embeddings in ChromaDB!")
