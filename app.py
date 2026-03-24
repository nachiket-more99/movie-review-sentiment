from dotenv import load_dotenv
load_dotenv()

import flask
from flask.views import MethodView
from index import Index
from movie import Movie
import os
import json

app = flask.Flask(__name__)   


app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

# Movie route with movie_id to fetch movie details
app.add_url_rule('/movie/<int:movie_id>',  
                 view_func=Movie.as_view('movie'),
                 methods=['GET', 'POST'])

@app.route("/health")
def health():
    return flask.jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
