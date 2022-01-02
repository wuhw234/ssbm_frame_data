from flask import Flask
from flask_restful import Resource, Api, abort
from flask_pymongo import MongoClient
import os
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import send_from_directory

load_dotenv()
username = os.environ["MONGO_USERNAME"]
password = os.environ["MONGO_PASSWORD"]

cluster = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.acrjr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["melee_frame_data"]
collection = db["characters"]

app = Flask(__name__)
api = Api(app)

@app.route("/static/<path:path>")
def swagger(path):
    return send_from_directory("static", path)


SWAGGER_URL = "/swagger"
PATH_TO_SWAGGER = "/static/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    PATH_TO_SWAGGER,
    config={
        "app_name": "Melee Frame Data API"
    }
)


app.register_blueprint(swaggerui_blueprint)

class Character(Resource):
    def get(self, character_name):
        try:
            character = collection.find_one({"name":character_name})
            if not character:
                raise KeyError()
            return character, 200
        except:
            abort(404, message="Character does not exist")
class MoveType(Resource):
    def get(self, character_name, move_type):
        try:
            character = collection.find_one({"name":character_name})
            movetype_data = character[move_type]
            if not movetype_data:
                raise KeyError()
            return movetype_data, 200
        except:
            abort(404, message="Move Type or Character does not exist")
class Move(Resource):
    def get(self, character_name, move_type, move_name):
        try:
            character = collection.find_one({"name":character_name})
            moves = character[move_type]
            move_data = moves[move_name]
            if not move_data:
                raise KeyError()
            return move_data, 200
        except:
            abort(404,  message="Move, Move Type, or Character does not exist")


api.add_resource(Character, "/api/<string:character_name>")
api.add_resource(MoveType, "/api/<string:character_name>/<string:move_type>")
api.add_resource(Move, "/api/<string:character_name>/<string:move_type>/<string:move_name>")

if __name__ == "__main__":
    app.run()
