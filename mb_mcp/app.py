from flask import Flask, request, jsonify
import asyncio
from slack_connecter import run_app as run_slack_app
from gdrive_connecter import run_app as run_gdrive_app
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='../query_dashboard', template_folder='../query_dashboard')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/ask', methods=['POST'])
async def ask():
    data = request.get_json()
    user_question = data.get('question')
    selected_application = data.get('application')

    if not user_question or not selected_application:
        return jsonify({'error': 'Missing question or application'}), 400

    try:
        if selected_application == 'slack':
            result = await run_slack_app(user_question)
        elif selected_application == 'gdrive':
            result = await run_gdrive_app(user_question)
        else:
            return jsonify({'error': 'Invalid application'}), 400
        answer = result['messages'][-1].content
        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
