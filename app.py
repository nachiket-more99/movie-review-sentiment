import flask
from flask.views import MethodView
from index import Index
from movie import Movie
import os
from google.cloud import secretmanager
import json


# Set the environment variable with the retrieved secret
os.environ["tmdb_bearer"] = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMTllMjY4NzFhY2I0YTg2Y2FhYWE5YWJkYmMxMGY5YyIsIm5iZiI6MTc3NDIwNjU3OC4xODQsInN1YiI6IjY5YzAzZTcyZTRhZDczNjMxOTAxY2Q0ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.uk1ltYR9uaJeIveukHgODN0LLTaEa1g1gmtD7thUHpU"

app = flask.Flask(__name__)   

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

# Movie route with movie_id to fetch movie details
app.add_url_rule('/movie/<int:movie_id>',  
                 view_func=Movie.as_view('movie'),
                 methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
