from flask import Flask
from flask_restful import Resource, Api, abort
from flask_pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
username = os.environ["MONGO_USERNAME"]
password = os.environ["MONGO_PASSWORD"]

print(username, password)
cluster = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.acrjr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["melee_frame_data"]
collection = db["characters"]

app = Flask(__name__)
api = Api(app)

class Character(Resource):
    def get(self, character_name):
        try:
            return collection.find_one({"name":character_name}), 200
        except:
            abort(404, message="Character does not exist")
class MoveType(Resource):
    def get(self, character_name, move_type):
        try:
            character = collection.find_one({"name":character_name})
            return character[move_type], 200
        except:
            abort(404, message="Move Type or Character does not exist")
class Move(Resource):
    def get(self, character_name, move_type, move_name):
        try:
            character = collection.find_one({"name":character_name})
            moves = character[move_type]
            return moves[move_name], 200
        except:
            abort(404,  message="Move, Move Type, or Character does not exist")

        

api.add_resource(Character, "/<string:character_name>")
api.add_resource(MoveType, "/<string:character_name>/<string:move_type>")
api.add_resource(Move, "/<string:character_name>/<string:move_type>/<string:move_name>")

if __name__ == "__main__":
    app.run()
