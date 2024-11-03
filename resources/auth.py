from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from database import db
from schemas.user_schema import UserSchema

blp = Blueprint("auth", __name__, url_prefix="/auth", description="Authentication API")

user_schema = UserSchema()

@blp.route("/register", methods=["POST"])
@blp.arguments(UserSchema)
def register(user_data):
    if User.query.filter_by(username=user_data["username"]).first():
        abort(409, message="Username already exists.")
    user = User(username=user_data["username"])
    user.set_password(user_data["password"])
    db.session.add(user)
    db.session.commit()
    return {"message": "User registered successfully"}, 201

@blp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and user.check_password(data["password"]):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        abort(401, message="Invalid credentials")

@blp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
