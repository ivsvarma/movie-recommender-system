

# uvicorn ml_model_as_api:app                                                         


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
import difflib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

class ModelInput(BaseModel):
    movie_name: str
    no_of_movies: int

MOVIE_MODEL_PATH = r"C:\Users\ivsva\Desktop\Machine Learning Course With Python\machine learning\projects using different model\movie_trained_model.sav"
MOVIE_DATA_PATH = r"C:\Users\ivsva\Desktop\Machine Learning Course With Python\machine learning\csvfiles\movies.csv"

# Load the trained model and verify its type
try:
    movie_trained_model = pickle.load(open(MOVIE_MODEL_PATH, "rb"))
    print("Model type:", type(movie_trained_model))
except FileNotFoundError:
    raise RuntimeError("Model file not found. Please check the path.")

# Assign the similarity matrix
similarity = movie_trained_model

# Load movie data and verify structure
try:
    movie_data = pd.read_csv(MOVIE_DATA_PATH)
    print("Movie data head:\n", movie_data.head())
    if 'title' not in movie_data.columns:
        raise KeyError("Missing 'title' column in the movie dataset.")
except FileNotFoundError:
    raise RuntimeError("Movie dataset not found. Please check the path.")

@app.post("/movieSuggestion")
def movie_suggestion(input_parameters: ModelInput):
    movie_name = input_parameters.movie_name
    no_of_movies = input_parameters.no_of_movies

    list_of_movies = movie_data['title'].tolist()

    # Find close matches to the input movie
    find_close_match = difflib.get_close_matches(movie_name, list_of_movies)
    if not find_close_match:
        raise HTTPException(status_code=404, detail="Movie not found in dataset.")

    close_match = find_close_match[0]
    index_of_matched_in_list = movie_data[movie_data.title == close_match].index[0]

    # Get similarity scores for the matched movie
    similarity_score = list(enumerate(similarity[index_of_matched_in_list]))

    # Sort movies by similarity
    sorted_similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    

    
    top_movies = []
    for (index, score) in enumerate(sorted_similarity_score[1: no_of_movies + 1]):
        title = movie_data.iloc[index]['title']
        top_movies.append({title})

    return {
        "input_movie": movie_name,
        "top_similar_movies": top_movies
    }
