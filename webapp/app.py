# webapp/app.py
from flask import Flask, render_template, request
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import nltk
from nltk.corpus import stopwords


app = Flask(__name__)

# Load the TF-IDF vectorizer and cosine similarity matrix
vectorizer = joblib.load('../models/tfidf_vectorizer.pkl')
cosine_similarities = joblib.load('../models/cosine_similarities.pkl')

# Load the preprocessed dataset
df = pd.read_csv('../data/processed/preprocessed_dataset.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    suggestions = []

    if request.method == 'POST':
        user_input = request.form['user_input']
        suggestions = get_movie_suggestions(user_input)

    return render_template('index.html', suggestions=suggestions)

def get_movie_suggestions(user_input):

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['ProcessedPlot'])
    user_input_tfidf = vectorizer.transform([user_input])
    user_cosine_similarities = cosine_similarity(user_input_tfidf, tfidf_matrix).flatten()
    similar_movies_indices = user_cosine_similarities.argsort()[:-10:-1]
    suggestions = df.iloc[similar_movies_indices][['Movie Title', 'Cover Image', 'Genre', 'Year']].to_dict('records')

    return suggestions

if __name__ == '__main__':
    app.run()
