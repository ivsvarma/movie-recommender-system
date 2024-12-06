import json 
from urllib import response
import requests


url = 'http://127.0.0.1:8000/movieSuggestion'

input_data_for_model = {
    'movie_name' : 'iron man',
    'no_of_movies' : 20
}

input_json = json.dumps(input_data_for_model)
response = requests.post(url , data= input_json)
print(response.text)