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
    url1 = 'https://test-api-6lv1.onrender.com/translateTest?text=ciao&sl=it&tl=en'
    url2 = 'https://test-api-6lv1.onrender.com/translateTest?text=buongiorno&sl=it&tl=de'
    url3 = 'https://test-api-6lv1.onrender.com/translateTest?text=hola&sl=sl&tl=fr'
    url4 = 'https://test-api-6lv1.onrender.com/translateTest?text=salut&sl=fr&tl=pt'
    url5 = 'https://test-api-6lv1.onrender.com/translateTest?text=bonjour&sl=fr&tl=ru'

    # Ritorna tutti gli esempi in stile HTML
    html += '<br><h1>Esempi Traduttore API</h1> '
    html += '<ul>'
    html += '<li>Traduci "ciao" dall\'italiano all\'inglese: <a href="' + url1 + '">' + url1 + '</a> </li>'
    html += '<li>Traduci "buongiorno" dall\'italiano al tedesco: <a href="' + url2 + '">' + url2 + '</a> </li>'
    html += '<li>Traduci "hola" dallo spagnolo al francese: <a href="' + url3 + '">' + url3 + '</a> </li>'
    html += '<li>Traduci "salut" dal francese al portoghese: <a href="' + url4 + '">' + url4 + '</a> </li>'
    html += '<li>Traduci "bonjour" dal francese al russo: <a href="' + url5 + '">' + url5 + '</a> </li>'
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
