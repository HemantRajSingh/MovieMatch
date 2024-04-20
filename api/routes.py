from flask import Flask, request, jsonify
from flask_cors import CORS


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


app = Flask(__name__)
CORS(app)

root_dir = Path(__file__).resolve().parent.parent

# load models
vectorizer = joblib.load(root_dir / 'models/tfidf_vectorizer.pkl')
glove_embeddings = np.load(root_dir / 'models/glove_embeddings.npy', allow_pickle=True)
knn_model = joblib.load(root_dir / 'models/knn_model.pkl')
movie_embeddings = np.load(root_dir / 'models/movie_embeddings.npy', allow_pickle=True)

# Load the preprocessed dataset
df = pd.read_csv(root_dir / 'data/processed/preprocessed_dataset.csv')

model_name = "embeddings"

@app.route('/api/select_model', methods=['POST'])
def set_model():
    global model_name
    model = request.json.get('value', 'embeddings')
    return {'status': 'success'}


@app.route('/recommendations/<query>', methods=['GET'])
def get_movie_recommendations(query):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['ProcessedPlot'])
    user_input_tfidf = vectorizer.transform([query])
    user_cosine_similarities = cosine_similarity(user_input_tfidf, tfidf_matrix).flatten()
    similar_movies_indices = user_cosine_similarities.argsort()[:-10:-1]
    suggestions = df.iloc[similar_movies_indices].to_dict('records')
    return jsonify(suggestions)

@app.route('/recommendations/', methods=['POST'])
def get_recommendations():
    # get movie recommendations using cosine similarity between glove embeddings and user input embeddings
    user_input = request.json.get('query', '')

    # Get the embedding for each word and handle missing values
    user_input_embeddings = text_to_embeddings(user_input)
    if len(user_input_embeddings) == 0:
        return jsonify([])  # Return empty recommendations if no valid embeddings found

    cosine_similarities = cosine_similarity([user_input_embeddings], movie_embeddings).flatten()
    similar_movies_indices = cosine_similarities.argsort()[:-10:-1]
    suggestions = df.iloc[similar_movies_indices].to_dict('records')
    return jsonify(suggestions)

def text_to_embeddings(text):
    tokens = process_query(text)
    word_embeddings = [glove_embeddings[word] for word in tokens if word in glove_embeddings]
    if len(word_embeddings) == 0:
        return None
    embeddings = np.mean(word_embeddings, axis=0)
    return embeddings

def process_query(query):
    # Tokenize the query
    query = query.lower()
    tokens = nltk.word_tokenize(query)

    # Remove stopwords
    tokens = [token for token in tokens if token not in stopwords.words('english')]

    # Lemmatize the tokens
    lemmatizer = nltk.WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return tokens

def text_to_embeddings(text):
    words = text.split()
    embeddings = np.zeros(100)
    count = 0
    for word in words:
        if word in glove_embeddings:
            embeddings += glove_embeddings[word]
            count += 1
    if count != 0:
        embeddings /= count
    return embeddings

@app.route('/browse', methods=['GET'])
def browse_movies():
    return jsonify(df.to_dict('records'))


if __name__ == '__main__':
    app.run(debug=True)
