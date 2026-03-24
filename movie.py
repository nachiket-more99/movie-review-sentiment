from flask import render_template
from flask.views import MethodView
import requests
import threading
import os
from sentiment_analysis import SentimentAnalysis

sentiment_cache = {}

class Movie(MethodView):
    # retrive movie details with reviews
    def get(self, movie_id=None):
        if movie_id is None:
            return render_template('index.html')
        else:
            url_reviews = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"
            url_details = f"https://api.themoviedb.org/3/movie/{movie_id}"

            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {os.getenv("TMDB_BEARER")}" 
            }

            reviews_thread = threading.Thread(target=self.get_reviews, args=(url_reviews, headers))
            details_thread = threading.Thread(target=self.get_details, args=(url_details, headers))

            reviews_thread.start()
            details_thread.start()

            reviews_thread.join()
            details_thread.join()

            # analysis = SentimentAnalysis.analyse_reviews(self.reviews)
            # self.movie_details['analysis'] = analysis

            if movie_id in sentiment_cache:
                analysis = sentiment_cache[movie_id]
                print("got analysis form cache")
            else:
                print("calling llm for analysis")
                analysis = SentimentAnalysis.analyse_reviews(self.reviews)
                sentiment_cache[movie_id] = analysis

            self.movie_details['analysis'] = analysis

            return render_template('movie.html', movie_details=self.movie_details)

    def get_reviews(self, url, headers):
        response = requests.get(url, headers=headers)
        self.reviews = []

        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            for review in results[:100]:
                self.reviews.append(review.get('content'))
        else:
            print("Error occurred in reviews:", response.status_code)

    def get_details(self, url, headers):
        response = requests.get(url, headers=headers)
        self.movie_details = {}

        if response.status_code == 200:
            data = response.json()
            genre_data = [genre.get('name') for genre in data.get('genres', [])]
            self.movie_details = {
                'title': data.get('original_title'),
                'tagline': data.get('tagline'),
                'overview': data.get('overview'),
                'poster': data.get('poster_path'),
                'release_date': data.get('release_date'),
                'genre': ', '.join(genre_data),
                'backdrop_path': data.get('backdrop_path')
            }
        else:
            print("Error occurred in details:", response.status_code)
