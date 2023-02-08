from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/')
def info():

    html = '''
    <h1>Traduttore API</h1>
    <p>Questa è una semplice API di traduzione che utilizza Google Translate per tradurre testo da una lingua all'altra.</p>
    <p>Per utilizzare l'API, inviare una richiesta GET alla seguente URL:</p>
    <pre>/translate?text=testo&source_language=lingua_sorgente&target_language=lingua_destinazione</pre>
    <p>Sostituire "testo", "lingua_sorgente" e "lingua_destinazione" con i valori desiderati.</p>
    '''

    # Esempi di richieste di traduzione
    url1 = 'https://test-api-6lv1.onrender.com/translate?text=ciao&sl=italiano&tl=inglese'
    url2 = 'https://test-api-6lv1.onrender.com/translate?text=buongiorno&sl=italiano&tl=tedesco'
    url3 = 'https://test-api-6lv1.onrender.com/translate?text=hola&sl=spagnolo&tl=francese'
    url4 = 'https://test-api-6lv1.onrender.com/translate?text=salut&sl=francese&tl=portoghese'
    url5 = 'https://test-api-6lv1.onrender.com/translate?text=bonjour&sl=francese&tl=russo'

    # Ritorna tutti gli esempi in stile HTML
    html += '<br><h1>Esempi Traduttore API</h1> '
    html += '<ul>'
    html += '<li>Traduci "ciao" dall\'italiano all\'inglese: ' + url1 + '</li>'
    html += '<li>Traduci "buongiorno" dall\'italiano al tedesco: ' + url2 + '</li>'
    html += '<li>Traduci "hola" dallo spagnolo al francese: ' + url3 + '</li>'
    html += '<li>Traduci "salut" dal francese al portoghese: ' + url4 + '</li>'
    html += '<li>Traduci "bonjour" dal francese al russo: ' + url5 + '</li>'
    html += '</ul>'

    return html


@app.route("/healthz")
def health_check():
    return "OK", 200


@app.route("/translate", methods=["POST"])
def translate():
    text = request.json["text"]
    source_language = request.json["sl"]
    target_language = request.json["tl"]
    
    sentences = re.split(r'[.!?]+', text)
    translated_sentences = []
    for sentence in sentences:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_language}&tl={target_language}&dt=t&q={sentence}"
        response = requests.get(url)
        data = response.json()
        translated_sentences.append(data[0][0][0])
    
    translated_text = " ".join(translated_sentences)
    
    return jsonify({"translated_text": translated_text})


@app.route("/translateTest", methods=["GET"])
def translateTest():
    text = request.args.get("text")
    source_language = request.args.get("sl")
    target_language = request.args.get("tl")
    
    sentences = re.split(r'[.!?]+', text)
    translated_sentences = []
    for sentence in sentences:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_language}&tl={target_language}&dt=t&q={sentence}"
        response = requests.get(url)
        data = response.json()
        translated_sentences.append(data[0][0][0])
    
    translated_text = " ".join(translated_sentences)
    
    return jsonify({"translated_text": translated_text})
