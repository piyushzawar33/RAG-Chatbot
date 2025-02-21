# RAG-Chatbot
Cogninext Task 2


This is a Retrieval-Augmented Generation (RAG) chatbot that uses:

ChromaDB for document storage and retrieval
Google Gemini AI for response generation
Flask for the API and web interface
MySQL for storing chat history



1. Clone the Repository by
git clone https://github.com/piyushzawar33/rag-chatbot.git
cd rag-chatbot


2. Create a Virtual Environment & Install Dependencies
python -m venv venv
venv\Scripts\activate

3. Install Required Packages by
pip install -r requirements.txt

4. Set Up the Database (MySQL)
mysql -u root -p
Use your MySQL password if any

CREATE DATABASE rag_chatbot;
USE rag_chatbot;

CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role VARCHAR(10) NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

5. Create a Hugging Face API token
set HUGGINGFACEHUB_API_TOKEN="your_huggingface_api_key"

Get your Google AI Key from Google AI Studio
Save the key in Key/Gemini key.txt


6. Create a data/ folder and put your PDF documents into it.

for running the Chatbot run:
python rag_chatbot.py

7. Test the API Endpoints by
For chat:
curl -X POST "http://127.0.0.1:5000/chat" -H "Content-Type: application/json" -d "{\"query\": \"What is AI?\"}"

For history
curl -X GET "http://127.0.0.1:5000/history"
