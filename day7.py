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

def compute_similarity(movies_df):
    """Computes cosine similarity matrix based on genres."""
    tfidf = TfidfVectorizer(stop_words='english')
    genre_matrix = tfidf.fit_transform(movies_df['Genre'])
    similarity_matrix = cosine_similarity(genre_matrix)
    return similarity_matrix

def get_movie_recommendations(movie_name, movies_df, similarity_matrix):
    """Returns a list of recommended movies based on a given movie."""
    if movie_name not in movies_df['Movie'].values:
        return "Movie not found in the database."
    
    index = movies_df[movies_df['Movie'] == movie_name].index[0]
    scores = list(enumerate(similarity_matrix[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    recommended_movies = [movies_df.iloc[i[0]]['Movie'] for i in scores[1:6]]
    
    return recommended_movies

def main():
    movies_df = load_movie_data()
    similarity_matrix = compute_similarity(movies_df)
    
    print("Available Movies:")
    print(movies_df[['Movie', 'Genre']].to_string(index=False))
    
    movie_name = input("Enter a movie name for recommendations: ")
    recommendations = get_movie_recommendations(movie_name, movies_df, similarity_matrix)
    
    if isinstance(recommendations, str):
        print(recommendations)
    else:
        print("Recommended Movies:")
        for movie in recommendations:
            print(movie)

if __name__ == "__main__":
    main()
