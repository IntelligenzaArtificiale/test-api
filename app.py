from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/')
def info():
    return '''
    <h1>Traduttore API</h1>
    <p>Questa è una semplice API di traduzione che utilizza Google Translate per tradurre testo da una lingua all'altra.</p>
    <p>Per utilizzare l'API, inviare una richiesta GET alla seguente URL:</p>
    <pre>/translate?text=testo&source_language=lingua_sorgente&target_language=lingua_destinazione</pre>
    <p>Sostituire "testo", "lingua_sorgente" e "lingua_destinazione" con i valori desiderati.</p>
    '''

@app.route('/example')
def example():
    # Esempi di richieste di traduzione
    url1 = 'https://test-api-6lv1.onrender.com/translate?text=ciao&source_language=italiano&target_language=inglese'
    url2 = 'https://test-api-6lv1.onrender.com/translate?text=buongiorno&source_language=italiano&target_language=tedesco'
    url3 = 'https://test-api-6lv1.onrender.com/translate?text=hola&source_language=spagnolo&target_language=francese'
    url4 = 'https://test-api-6lv1.onrender.com/translate?text=salut&source_language=francese&target_language=portoghese'
    url5 = 'https://test-api-6lv1.onrender.com/translate?text=bonjour&source_language=francese&target_language=russo'

    # Ritorna tutti gli esempi in stile HTML
    html = '<h1>Esempi Traduttore API</h1> '
    html += '<ul>'
    html += '<li>' + url1 + '</li>'
    html += '<li>' + url2 + '</li>'
    html += '<li>' + url3 + '</li>'
    html += '<li>' + url4 + '</li>'
    html += '<li>' + url5 + '</li>'
    html += '</ul>'

    return html


@app.route("/healthz")
def health_check():
    return "OK", 200

@app.route("/translate", methods=["POST"])
def translate():
    text = request.json["text"]
    source_language = request.json["source_language"]
    target_language = request.json["target_language"]
    
    sentences = re.split(r'[.!?]+', text)
    translated_sentences = []
    for sentence in sentences:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_language}&tl={target_language}&dt=t&q={sentence}"
        response = requests.get(url)
        data = response.json()
        translated_sentences.append(data[0][0][0])
    
    translated_text = " ".join(translated_sentences)
    
    return jsonify({"translated_text": translated_text})

@app.route("/translate")
def translate():
    text = request.args.get("text")
    source_language = request.args.get("source_language")
    target_language = request.args.get("target_language")
    
    sentences = re.split(r'[.!?]+', text)
    translated_sentences = []
    for sentence in sentences:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_language}&tl={target_language}&dt=t&q={sentence}"
        response = requests.get(url)
        data = response.json()
        translated_sentences.append(data[0][0][0])
    
    translated_text = " ".join(translated_sentences)
    
    return jsonify({"translated_text": translated_text})
