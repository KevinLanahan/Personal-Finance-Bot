from time import sleep
from openai import OpenAI
from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)


client = OpenAI(api_key='ask_for_when_testing')

assistant = client.beta.assistants.create(
    name="Personal Finance Bot",
    instructions="You are a personal finance bot, you are going to give advice based on users financial goals",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini"
)

thread = client.beta.threads.create()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['message']
    
    # Send Q's
    try:
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )
        print("Message sent successfully.")
    except Exception as e:
        return jsonify({'response': f"Error while sending message: {str(e)}"}), 500

    # Create run
    try:
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )
        print("Run created successfully.")
    except Exception as e:
        return jsonify({'response': f"Error while creating run: {str(e)}"}), 500

    # Wait for run to complete
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        sleep(1)

    # Retrieve messages and format response
    try:
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print("Messages retrieved successfully.")
        response_message = ""
        for message in reversed(messages.data):
            if message.content:
                response_message += f"{message.content[0].text.value}\n"
        
        return jsonify({'response': response_message.strip()})
    except Exception as e:
        return jsonify({'response': f"Error while retrieving messages: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
