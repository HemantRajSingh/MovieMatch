from flask import Flask, request, jsonify 
from flask_cors import CORS
from flask import Response


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
CORS(app, resources={r"/*": {"origins": "*"}})

root_dir = Path(__file__).resolve().parent.parent

# load models
vectorizer = joblib.load(root_dir / 'models/tfidf_vectorizer.pkl')
knn_model = joblib.load(root_dir / 'models/knn_model.pkl')
movie_embeddings = np.load(root_dir / 'models/movie_embeddings.npy', allow_pickle=True)

# Load the preprocessed dataset
df = pd.read_csv(root_dir / 'data/merged/imdb_movies_min_votes_500.csv')
df = df.drop(['genre', 'keywords', 'actors', 'director', 'synopsis', 'summary'], axis=1)


model_name = "embeddings"
glove_file = root_dir / 'models/glove.6B.100d.txt'

embedding_size = 100
word_embeddings = {}
with open(glove_file, 'r', encoding='utf-8') as f:
    for line in f:
        values = line.split()
        word = values[0]
        embedding = np.array(values[1:], dtype='float32')
        word_embeddings[word] = embedding
        
def text_to_embeddings(text):
    words = text.split()
    embeddings = np.zeros(embedding_size)
    count = 0
    for word in words:
        if word in word_embeddings:
            embeddings += word_embeddings[word]
            count += 1
    if count != 0:
        embeddings /= count
    return embeddings

def process_query(query):
    query = query.lower()
    tokens = nltk.word_tokenize(query)
    tokens = [token for token in tokens if token not in stopwords.words('english')]
    lemmatizer = nltk.WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return tokens

@app.route('/api/select_model/', methods=['POST'])
def set_model():
    global model_name
    model = request.json.get('value', 'embeddings')
    return {'status': 'success'}


@app.route('/recommendations/', methods=['POST', 'OPTIONS'])
def get_recommendations():
    user_input = request.json.get('query', '')
    user_input_embeddings = text_to_embeddings(user_input)
    if len(user_input_embeddings) == 0:
        return jsonify([])  

    cosine_similarities = cosine_similarity([user_input_embeddings], movie_embeddings).flatten()
    similar_movies_indices = cosine_similarities.argsort()[:-10:-1]
    return Response(df.iloc[similar_movies_indices].to_json(orient='records'), mimetype='application/json')

@app.route('/browse/', methods=['GET'])
def browse_movies():
    return Response(df[:60].to_json(orient="records"), mimetype='application/json')

@app.route('/top_rated_movies/', methods=['GET'])
def top_rated_movies():
    top_rated = df.sort_values(by='rating', ascending=False).head(10)
    return Response(top_rated[:60].to_json(orient='records'), mimetype='application/json')

@app.route('/latest_movies/', methods=['GET'])
def latest_movies():
    latest = df.sort_values(by='year', ascending=False).head(10)
    return Response(latest[:60].to_json(orient='records'), minetype='application/json')

@app.route('/popular_movies/', methods=['GET'])
def popular_movies():
    popular = df.sort_values(by='rating_count', ascending=False).head(10)
    return Response(popular[:60].to_json(orient='records'), minetype='application/json')

@app.route('/trending_movies/', methods=['GET'])
def trending_movies():
    # You can implement trending logic based on your criteria
    # For example, movies that gained the most rating counts in the last week
    trending = df.sort_values(by=['year', 'rating_count'], ascending=[False, False]).head(10)
    # convert trending to dictionary and return
    
    return Response(trending[:60].to_json(orient='records'), minetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
