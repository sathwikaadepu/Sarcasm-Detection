import os
import io
import re
import pickle
import nltk
import speech_recognition as sr
from nltk.sentiment import SentimentIntensityAnalyzer
from flask import Flask, render_template, request, jsonify

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_url_path='/static', static_folder='static')

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

@app.route('/', methods=['GET'])
def home():
    # Your logic for rendering the main landing page
    return render_template('home.html')

def analyze_sentiment(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        sentiment_scores = sia.polarity_scores(text)
        return text, sentiment_scores
    except sr.UnknownValueError:
        return None, None
    
def map_sentiment_score_to_label(sentiment_score):
    if sentiment_score >= 0.1:  # Hypothetical threshold for sarcasm detection
        return "Sarcasm"
    else:
        return "Not a Sarcasm"
    
#text-analysis
app.secret_key = b'_thuiklstrhj/'

# Load the pickled model and TF-IDF vectorizer
with open('tfidf.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def predict(text):
    """This function predicts if a sentence is sarcastic or not."""
    data = text
    data = re.sub('[^a-zA-Z]', ' ', data)
    s = []
    s.append(data)
    data = vectorizer.transform(s).toarray()
    prediction = model.predict(data)
    return int(prediction[0])

@app.route("/text")
def text():
    return render_template('text.html')

@app.route("/prediction", methods=['POST'])
def prediction():
    if request.method == 'POST':
        text = request.form['text']
        prediction_result = predict(text)
        return render_template('text.html', response=prediction_result)

# Define route for the homepage
@app.route('/index', methods=['GET', 'POST'])
def index():
    sentiment_score = None
    transcribed_text = None
    sentiment_label = None
    if request.method == 'POST':
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'})

        audio_file = request.files['audio']

        if audio_file:
            audio_filename = audio_file.filename
            if audio_filename.endswith('.mp3'):
                temp_audio_file = 'temp_audio.wav'
                audio_file.save(temp_audio_file)
            elif audio_filename.endswith('.wav'):
                temp_audio_file = 'temp_audio.wav'
                audio_file.save(temp_audio_file)
            else:
                return jsonify({'error': 'Unsupported audio format'})

            transcribed_text, sentiment_scores = analyze_sentiment(temp_audio_file)

            if sentiment_scores:
                sentiment_score = sentiment_scores['compound']
                sentiment_label = map_sentiment_score_to_label(sentiment_score)

            # Delete the temporary audio file
            os.remove(temp_audio_file)
    

    return render_template('index.html', sentiment_score=sentiment_score, transcribed_text=transcribed_text, sentiment_label=sentiment_label)


if __name__ == '__main__':
    app.run(debug=True)
