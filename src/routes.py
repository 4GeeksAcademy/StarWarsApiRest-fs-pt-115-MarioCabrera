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

@api.route("/<int:user_id>/favorite_hunter/<int:hunter_id>",methods=["POST"])
def add_favorite_hunter(user_id,hunter_id):
    user = db.session.get(User,user_id)
    hunter = db.session.get(Hunter,hunter_id)

    if not user or not hunter:
        return jsonify({"msg":"User or Hunter not found"}), 404
    
    if hunter in user.favorite_hunter:
        return jsonify({"msg":"Hunter already in user's favourite"}), 400
    
    user.favorite_hunter.append(hunter)

    db.session.commit()

    return jsonify(user.serialize()), 200

@api.route("/<int:user_id>/favorite_hunter/<int:hunter_id>",methods=["DELETE"])
def remove_favorite_hunter(user_id,hunter_id):
    user = db.session.get(User,user_id)
    hunter = db.session.get(Hunter,hunter_id)

    if not user or not hunter:
        return jsonify({"msg":"User or Hunter not found"}), 404
    
    if hunter in user.favorite_hunter:
        user.favorite_hunter.remove(hunter)
        db.session.commit()

    return jsonify(user.serialize()), 200

@api.route("/<int:user_id>/favorite_demon/<int:demon_id>",methods=["POST"])
def add_favorite_demon(user_id,demon_id):
    user = db.session.get(User,user_id)
    demon = db.session.get(Demon,demon_id)

    if not user or not demon:
        return jsonify({"msg":"User or Demon not found"}), 404
    
    if demon in user.favorite_demon:
        return jsonify({"msg":"demon already in user's favourite"}), 400
    
    user.favorite_demon.append(demon)

    db.session.commit()

    return jsonify(user.serialize()), 200

@api.route("/<int:user_id>/favorite_demon/<int:demon_id>",methods=["DELETE"])
def remove_favorite_demon(user_id,demon_id):
    user = db.session.get(User,user_id)
    demon = db.session.get(Demon,demon_id)

    if not user or not demon:
        return jsonify({"msg":"User or Demon not found"}), 404
    
    if demon in user.favorite_demon:
        user.favorite_demon.remove(demon)
        db.session.commit()
    
    return jsonify(user.serialize()), 200

@api.route("/<int:user_id>/favorite_combat_style/<int:combat_style_id>",methods=["POST"])
def add_favorite_combat_style(user_id,combat_style_id):
    user = db.session.get(User,user_id)
    combat_style = db.session.get(CombatStyle,combat_style_id)

    if not user or not combat_style:
        return jsonify({"msg":"User or Combat Style not found"}), 404
    
    if combat_style in user.favorite_combatStyle:
        return jsonify({"msg":"combat style already in user's favourite"}), 400
        
    user.favorite_combatStyle.append(combat_style)
    
    db.session.commit()

    return jsonify(user.serialize()), 200

@api.route("/<int:user_id>/favorite_combat_style/<int:combat_style_id>",methods=["DELETE"])
def delete_favorite_combat_style(user_id,combat_style_id):
    user = db.session.get(User,user_id)
    combat_style = db.session.get(CombatStyle,combat_style_id)

    if not user or not combat_style:
        return jsonify({"msg":"User or Combat Style not found"}), 404
    
    if combat_style in user.favorite_combatStyle:
        user.favorite_combatStyle.remove(combat_style)
        db.session.commit()

    return jsonify(user.serialize()), 200

