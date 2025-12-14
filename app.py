from flask import Flask, request, jsonify
from flask_cors import CORS
from mchat_predictor import MChatPredictor
from mchat_chatbot import MChatChatbot

app = Flask(__name__)

CORS(app) #Allow React to communicate with Flask 


sessions = {}

@app.route('/api/start', methods=['POST'])
def start_conversation():
    session_id = request.json.get('session_id', 'default')
    predictor = MChatPredictor()
    chatbot = MChatChatbot(model_predictor=predictor)
    sessions[session_id] = chatbot
    
    initial_message = chatbot.start_conversation()
    return jsonify({
        'message': initial_message,
        'stage': chatbot.stage,
        'progress': f"0/10"
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    session_id = request.json.get('session_id', 'default')
    user_message = request.json.get('message', '')

    if session_id not in sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    chatbot = sessions[session_id]
    response = chatbot.chat(user_message)

    #calculate the progress
    if chatbot.stage == "questions":
        progress = f"{chatbot.current_question_idx}/10"
    elif chatbot.stage == "demographics":
        progress = "demographics"
    elif chatbot.stage == "Complete":
        progress = "Complete"
    else:
        progress = "0/10"

    return jsonify({
        'message': response,
        'stage': chatbot.stage,
        'progress': progress,
        'IsComplete': chatbot.stage == "complete"
    })

@app.route('/api/reset', methods=['POST'])
def reset():
    session_id = request.json.get('session_id', 'default')
    if session_id in sessions:
        sessions[session_id].reset()
        initial_message = sessions[session_id].start_conversation()
        return jsonify({
            'message': initial_message,
            'stage': sessions[session_id].stage,
            'progress': "0/10"
        })
    
    return jsonify({'error': 'Session not found'}), 404



if __name__ == '__main__':
    app.run(debug=True, port=5000)

