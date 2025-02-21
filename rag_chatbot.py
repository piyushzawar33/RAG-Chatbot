from flask import Flask, request, render_template, jsonify
from embed_store import retrieval
import mysql.connector
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
import os
import re

app = Flask(__name__)


with open("Key/Gemini key.txt") as f:
    GOOGLE_API_KEY = f.read().strip()

genai.configure(api_key=GOOGLE_API_KEY)


db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Use your password here
    "database": "rag_chatbot"
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


def store_chat(role, content):
    cursor.execute("INSERT INTO chat_history (role, content) VALUES (%s, %s)", (role, content))
    conn.commit()

def get_chat_history():
    cursor.execute("SELECT role, content, timestamp FROM chat_history ORDER BY timestamp DESC LIMIT 20")
    history = cursor.fetchall()

    chat_history = [{"role": row[0], "content": row[1], "timestamp": row[2]} for row in history]
    return chat_history

def clean_response(text):
    text = re.sub(r'\n+', '\n', text.strip())
    text = re.sub(r'The prompt repeats itself.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\*\s+', '* ', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text) 
    return text


def generate_response(user_query, context_text):
    try:
        INPUT_TEMPLATE = """
        {question} Answer this question based on the below context.
        context is: {context}.
        Note that answer will not be too long. Also remember that if the question is outside the context
        then kindly say that this question is out of the context provided.
        Do not say "according to the context" or "mentioned in the context" or similar.
        """
        prompt_template = ChatPromptTemplate.from_template(INPUT_TEMPLATE)
        formatted_prompt = prompt_template.format(context=context_text, question=user_query)

        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(formatted_prompt)

        cleaned_text = clean_response(response.text)
        return cleaned_text
    except Exception as e:
        return f"Error generating response: {e}"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("query", "")    
    
    if not user_query:
        return jsonify({"response": "Please enter a valid question."}), 400

    context_text = retrieval(user_query)
    response_text = generate_response(user_query, context_text)

    store_chat("user", user_query)
    store_chat("system", response_text)

    return jsonify({"response": response_text})

@app.route("/history", methods = ['GET'])
def history():
    chat_history = get_chat_history()
    return jsonify({"history": chat_history})


if __name__ == "__main__":
    app.run(debug=True)
