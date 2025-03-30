import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_movie_data():
    """Loads a sample movie dataset."""
    data = {
        'Movie': [
            'Inception', 'Interstellar', 'The Matrix', 'The Dark Knight', 'Titanic', 'Avatar',
            'The Shawshank Redemption', 'Gladiator', 'The Godfather', 'Pulp Fiction'
        ],
        'Genre': [
            'Sci-Fi, Action', 'Sci-Fi, Drama', 'Sci-Fi, Action', 'Action, Drama', 'Romance, Drama', 'Sci-Fi, Action',
            'Drama, Crime', 'Action, Drama', 'Crime, Drama', 'Crime, Drama'
        ]
    }
    return pd.DataFrame(data)
