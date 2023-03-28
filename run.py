from flask import Flask, request, render_template
from io import BytesIO
from PyPDF2 import PdfReader
from generate_embedding import Chatbot
import requests
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key ="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"
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/process_pdf", methods=['POST'])
def process_pdf():
    print("Processing pdf")
    file = request.data
    pdf = PdfReader(BytesIO(file))
    chatbot = Chatbot()
    paper_text = chatbot.parse_paper(pdf)
    global df
    df = chatbot.paper_df(paper_text)
    df = chatbot.calculate_embeddings(df)
    print("Done processing pdf")
    return {'answer': ''}

@app.route("/download_pdf", methods=['POST'])
def download_pdf():
    chatbot = Chatbot()
    url = request.json['url']
    r = requests.get(str(url))
    print(r.headers)
    pdf = PdfReader(BytesIO(r.content))
    paper_text = chatbot.parse_paper(pdf)
    global df
    df = chatbot.paper_df(paper_text)
    df = chatbot.calculate_embeddings(df)
    print("Done processing pdf")
    return {'key': ''}

@app.route("/reply", methods=['POST'])
def reply():
    chatbot = Chatbot()
    query = request.json['query']
    query = str(query)
    prompt = chatbot.create_prompt(df, query)
    response = chatbot.response(df, prompt)
    print(response)
    return response, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
