from flask import Flask, jsonify
from flask_cors import CORS


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from pathlib import Path
import joblib


app = Flask(__name__)
CORS(app)

root_dir = Path(__file__).resolve().parent.parent
# Load the TF-IDF vectorizer and cosine similarity matrix
vectorizer = joblib.load(root_dir / 'models/tfidf_vectorizer.pkl')
cosine_similarities = joblib.load(root_dir / 'models/cosine_similarities.pkl')

# Load the preprocessed dataset
df = pd.read_csv(root_dir / 'data/processed/preprocessed_dataset.csv')


@app.route('/recommendations/<query>', methods=['GET'])
def get_movie_recommendations(query):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['ProcessedPlot'])
    user_input_tfidf = vectorizer.transform([query])
    user_cosine_similarities = cosine_similarity(user_input_tfidf, tfidf_matrix).flatten()
    similar_movies_indices = user_cosine_similarities.argsort()[:-10:-1]
    suggestions = df.iloc[similar_movies_indices][['Movie Title', 'Cover Image', 'Genre', 'Year']].to_dict('records')

    return jsonify(suggestions)


@app.route('/browse', methods=['GET'])
def browse_movies():
    return jsonify(df[['Movie Title', 'Cover Image', 'Genre', 'Year']].to_dict('records'))


if __name__ == '__main__':
    app.run(debug=True)
