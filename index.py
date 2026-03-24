from flask import render_template, request
from flask.views import MethodView
import requests
import os
import concurrent.futures

class Index(MethodView):
    # get movie list
    def get(self):
        
        url = "https://api.themoviedb.org/3/movie/popular?language=en-US&"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {os.getenv("TMDB_BEARER")}" 
        }

        responses = []
        
        # for i in range(1, 4):
        #     responses.append(requests.get(url+f"page={i}", headers=headers))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(requests.get, url + f"page={i}", headers=headers)
                for i in range(1, 4)
            ]
            responses = [f.result() for f in futures]

        movies = {}
        i = 0

        for response in responses:
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                for index, movie in enumerate(results, 1):  # Extract data for the movies                 
                    movie_data = {
                        'id': movie.get('id'),
                        'title': movie.get('title'),
                        'poster_path': movie.get('poster_path'),
                        'release_date': movie.get('release_date')
                    }
                    movies[i] = movie_data
                    i += 1
            else:
                print("Error occurred:", response.status_code)

        return render_template('index.html', movies = movies)
