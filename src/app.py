"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person
from routes import api

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

app.register_blueprint(api, url_prefix="/api")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
from flask import Flask, Blueprint, jsonify, request
from models import db, User, Hunter, Demon, CombatStyle

api = Blueprint("api", __name__)

@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()

    return jsonify([user.serialize() for user in users]), 200

@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg":"User not found"}), 404
    return jsonify(user.serialize())
@api.route("/users",methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("email") or not data.get("password"):
        return jsonify({"msg": "Email and Password are required"}), 400
    new_user = User(
        email = data["email"],
        password = data["password"]
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.serialize()), 201

@api.route("/<int:user_id>/favorite_hunters", methods=["GET"])
def get_favorite_hunter(user_id):
    users = db.session.get(User,user_id)
    if not users:
        return jsonify({ "msg" : "User not found"}), 404
    favorites = [user.serialize() for user in users.favorite_hunter]
    return jsonify(favorites), 200

@api.route("/<int:user_id>/favorite_demons", methods=["GET"])
def get_favorite_demon(user_id):
    users = db.session.get(User,user_id)
    if not users:
        return jsonify({ "msg" : "User not found"}), 404
    favorites = [user.serialize() for user in users.favorite_demon]
    return jsonify(favorites), 200

@api.route("/<int:user_id>/favorite_combatStyles", methods=["GET"])
def get_favorite_combatStyle(user_id):
    users = db.session.get(User,user_id)
    if not users:
        return jsonify({ "msg" : "User not found"}), 404
    favorites = [user.serialize() for user in users.favorite_combatStyle]
    return jsonify(favorites), 200

