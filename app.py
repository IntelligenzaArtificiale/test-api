from flask import Flask, request, jsonify
import urllib.parse
import json
import requests
import re

app = Flask(__name__)

@app.route('/')
def info():

    html = '''
    <h1>Traduttore API</h1>
    <p>Questa è una semplice API di traduzione che utilizza Google Translate per tradurre testo da una lingua all'altra.</p>
    <p>Per utilizzare l'API, inviare una richiesta GET alla seguente URL:</p>
    <pre>/translate?text=testo&arget_language=lingua_destinazione</pre>
    <p>Sostituire "testo"e "lingua_destinazione" con i valori desiderati.</p>
    '''

@app.route("/healthz")
def health_check():
    return "OK", 200


@app.route("/translate", methods=["POST"])
def translate():
    text = request.json["text"]
    target_language = request.json["tl"]

    #se il testo è più lungo di 2000 caratteri, ritorna un errore
    if len(text) > 2000:
        return jsonify({"error": "Text too long"}), 400


    if not all([text, target_language]):
        return jsonify({"error": "Missing required parameters"}), 400
    
    sentences = re.split(r'[.!?]+', text)
    translated_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 1:  # verifica che la frase non sia vuota
            try:
                encoded_sentence = urllib.parse.quote(sentence)
                url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_language}&dt=t&q={encoded_sentence}"
                response = requests.get(url)
                data = response.json()
                translated_sentences.append(data[0][0][0])
            except requests.exceptions.RequestException as e:
                return jsonify({"error": f"Request error: {e}"}), 500
            except ValueError as e:
                return jsonify({"error": f"JSON parsing error: {e}"}), 500

    translated_text = " ".join(translated_sentences)
    return json.dumps({"translated_text": translated_text}, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.route("/translateTest", methods=["GET"])
def translateTest():
    text = request.args.get("text")
    target_language = request.args.get("tl")

    if len(text) > 2000:
        return jsonify({"error": "Text too long"}), 400

    if not all([text, target_language]):
        return jsonify({"error": "Missing required parameters"}), 400
    
    sentences = re.split(r'[.!?]+', text)
    translated_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 1:  # verifica che la frase non sia vuota
            try:
                encoded_sentence = urllib.parse.quote(sentence)
                url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_language}&dt=t&q={encoded_sentence}"
                response = requests.get(url)
                data = response.json()
                translated_sentences.append(data[0][0][0])
            except requests.exceptions.RequestException as e:
                return jsonify({"error": f"Request error: {e}"}), 500
            except ValueError as e:
                return jsonify({"error": f"JSON parsing error: {e}"}), 500

    translated_text = " ".join(translated_sentences)
    return json.dumps({"translated_text": translated_text}, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

