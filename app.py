from flask import Flask, render_template, request, jsonify
import time
import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# Function to continuously listen for voice input and return user input
def listen_for_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for user input...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source)
            user_input = recognizer.recognize_google(audio)

            print(f"User said: {user_input}")
            return user_input

        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
            return ""

# Function to search for and narrate the answer to a question
def search_and_narrate_answer(question):
    search_url = f"https://www.google.com/search?q={question}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    answer_elements = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")
    
    if answer_elements:
        answer = answer_elements[0].get_text()
        text_to_speech("Here's the answer to your question:")
        text_to_speech(answer)
    else:
        text_to_speech("I couldn't find an answer to your question.")

# Function to ask if the user has any questions
def ask_if_question():
    text_to_speech("Do you have any questions?")
    time.sleep(1)

# Function to narrate a chapter with question prompts
def narrate_chapter_with_questions(chapter_text):
    paragraphs = chapter_text.split('\n\n')  # Assuming paragraphs are separated by two newlines
    for paragraph in paragraphs:
        text_to_speech(paragraph)
        time.sleep(1)  # Adjust this delay as needed

        ask_if_question()  # Ask if there are any questions

        user_input = ""
        start_time = time.time()

        while time.time() - start_time < 5:
            user_input = listen_for_input()
            if user_input:
                if user_input.lower():
                    search_and_narrate_answer(user_input)
                break

# Create Web Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/narrate', methods=['POST'])
def narrate():
    chapter_text = request.form['text']
    narrate_chapter_with_questions(chapter_text)
    return "Text narration started."

@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '')
    
    # Process the question as needed
    # You can use the 'question' variable here to perform actions or provide a response
    
    return "Question answered."

if __name__ == '__main__':
    app.run(debug=True)
