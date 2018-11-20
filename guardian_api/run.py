from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from .views import RetrieveArticles
app = Flask(__name__, static_url_path='/static')
CORS(app)
api = Api(app)

#api.add_resource(RetrieveArticles, '/articles/<string:article_id>')
api.add_resource(RetrieveArticles, '/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
