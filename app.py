import os
from google import genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import absl.logging

app = Flask(__name__)
CORS(app)

os.environ["GRPC_VERBOSITY"] = "NONE"
absl.logging.set_verbosity(absl.logging.ERROR)

client = genai.Client(api_key="AIzaSyDjho6SJ0gw0GadBv5FoXzbqwH8aY6DFE4")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        user_message = data.get('message')
        chat_type = data.get('chat_type')

        # if chat_type == 'ai':
        #     response = client.models.generate_content(
        #         model="gemini-2.0-flash", contents=user_message
        #     )
        #     return jsonify({'response': response.text})
        if chat_type == 'ai':
            system_prompt = """
            You are Nidhisakh, a multilingual, intelligent, and helpful loan advisory chatbot. Your role is to assist users in understanding, comparing, and applying for loans tailored to their specific needs. 

Your tasks include:
- Asking relevant questions to identify the user's loan purpose (e.g., education, home, personal, business).
- Explaining types of loans available with their features (interest rate, tenure, eligibility, documentation, and processing fees).
- Calculating estimated loan eligibility based on user's income, expenses, employment status, and credit score.
- Providing EMI calculation using principal, interest rate, and tenure.
- Comparing loan offers from various banks or NBFCs (use realistic, general examples unless connected to a live API).
- Advising users on improving eligibility and minimizing interest burden.
- Explaining key financial terms in simple words.
- Assisting with the digital loan application process.
- Answering FAQs in a professional and easy-to-understand tone.
- Supporting English, Hindi, and Tamil (or other requested languages).
- Maintaining user privacy and never storing personal data.

Always be polite, professional, and clear. Ask one question at a time, guide the user step-by-step, and present information using bullet points or tables for clarity.

            """
            prompt = f"{system_prompt}\n\nUser: {user_message}\nAI:"
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt

        )
        cleaned = clean_response(response.text)
        return jsonify({'response': cleaned})


        return jsonify({'response': f"You said: {user_message}"})
    
    except Exception as e:
        return jsonify({'response': f"An error occurred: {str(e)}"}), 500
import re

def clean_response(text):
    
    # max_length = 300 
    # if len(cleaned) > max_length:
    #     cleaned = cleaned[:max_length].rsplit('.', 1)[0] + '.'
    # Remove Markdown-style bold and italics
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    
    # Remove AI: prefix
    text = re.sub(r'^AI:\s*', '', text, flags=re.IGNORECASE)

    # Optional: Replace bullet points and unnecessary colons
    text = re.sub(r'^[\*\-]\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r':\s*\n', '.\n', text)

    # Remove excessive newlines
    text = re.sub(r'\n{2,}', '\n', text)

    return text.strip()


if __name__ == '__main__':
    app.run(debug=True)