from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

def load_pdf(pdf_path):
    loader = DirectoryLoader(pdf_path, glob='*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents 


def clean_text(documents):
    text = re.sub(r'\n+', '\n', text.strip())
    text = re.sub(r'\*\s+', '* ', text)
    return text

def split_text(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap = 50)
    chunk = text_splitter.split_documents(text)
    return chunk


def get_chunks(pdf_path = 'data/'):
    docs = load_pdf(pdf_path)
    chunks = split_text(docs)
    return docs, chunks
    

if __name__ == "__main__":
    docs, chunks = get_chunks()
    print(f"Processed {len(chunks)} text chunks from {len(docs)} documents.")