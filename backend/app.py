from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
import threading
import ollama
import ssl

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Funzione per inviare messaggio dal chatbot (ollama)
def get_chatbot_response(user_input):
    messages = [
        {"role": "user", "content": f"Rispondi alla seguente domanda usando solo informazioni relative agli Anni di Piombo:\n\nDomanda: {user_input}\nRisposta:"}
    ]
    response = ollama.chat(
        model='llama3',
        messages=messages,
        stream=False  # Imposta su False per ottenere la risposta completa
    )
    # Restituisce il primo messaggio della risposta (modificabile a seconda del formato)
    return response[0]['message']['content']

# Gestione connessione client
@socketio.on('connect')
def handle_connect():
    print('Client connesso')

# Gestione messaggio in arrivo dal frontend (Angular)
@socketio.on('message')
def handle_message(msg):
    print(f"Messaggio ricevuto dal client: {msg}")
    
    # Ottieni la risposta dal chatbot
    response = get_chatbot_response(msg)
    
    # Invia la risposta al client
    emit('message', response)

# Configura il server HTTPS
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='path/to/cert.pem', keyfile='path/to/key.pem')

if __name__ == '__main__':
    # Avvia il server Flask con supporto HTTPS
    socketio.run(app, host='0.0.0.0', port=5000, ssl_context=context)
