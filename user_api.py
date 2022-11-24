from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_bcrypt import check_password_hash
from models import User, Change
from schemas import *
import db_utils
import sqlalchemy
import marshmallow


user_bp = Blueprint('user', __name__)


@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        user_data = UserToCreate().load(request.json)
        user = db_utils.create_entry(User, **user_data)

        response = make_response(jsonify(UserData().dump(user)))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid data input", status=400))
        response.status_code = 400
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
    return response


@user_bp.route('/login', methods=['GET'])
def login_user():
    try:
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if not username or not password:
            return make_response('Could not verify', 401, {'WWW.Authentication': 'Basic realm: "Login required"'})

        user = db_utils.get_entry_by_username(User, username)

        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return jsonify({'token': access_token})

        return make_response('Could not verify\n', 401, {'WWW.Authentication': 'Basic realm: "Login required"'})
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid data input", status=400))
        response.status_code = 400
        return response

    # TO DO
@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_users():
    note = db_utils.get_all_entry(User)

    response = make_response(jsonify(UserData(many=True).dump(note)))
    response.status_code = 200
    return response


@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    current_identity_id = get_jwt_identity()
    user = db_utils.get_entry_by_id(User, user_id)
    if current_identity_id != user.id:
        return jsonify('Access is denied')
    try:
        # current_identity_id = get_jwt_identity()
        # user = db_utils.get_entry_by_id(User, user_id)
        # if current_identity_id != user.id:
        #     return jsonify('Access is denied')
        user = db_utils.get_entry_by_id(User, user_id)
        user_stats = db_utils.get_all_entry_by_uid(Change, user_id)
        count = db_utils.get_entry_by_uid_count(Change, user_id)
        response = make_response(jsonify(user=UserToShow().dump(user),
                                         count=count,
                                         editing=ChangeNoId(many=True).dump(user_stats)))
        response.status_code = 200
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@user_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    # current_identity_id = get_jwt_identity()
    # user = db_utils.get_entry_by_id(User, user_id)
    # if current_identity_id != user.id:
    #     return jsonify('Access is denied')
    # user_data = UserToCreate().load(request.json)
    # for key in user_data:
    #     if key == 'username':
    #         if db_utils.get_entry_by_username_scalar(User, user_data[key]) is not None:
    #             response = make_response(jsonify(message="Username duplicate", status=400))
    #             response.status_code = 400
    #             return response
    #     if key == 'email':
    #         if db_utils.get_entry_by_email_scalar(User, user_data[key]) is not None:
    #             response = make_response(jsonify(message="Email duplicate", status=400))
    #             response.status_code = 400
    #             return response
    try:
        current_identity_id = get_jwt_identity()
        user = db_utils.get_entry_by_id(User, user_id)
        if current_identity_id != user.id:
            return jsonify('Access is denied')
        user_data = UserToCreate().load(request.json)
        for key in user_data:
            if key == 'username':
                if db_utils.get_entry_by_username_scalar(User, user_data[key]) is not None:
                    response = make_response(jsonify(message="Username duplicate", status=400))
                    response.status_code = 400
                    return response
            if key == 'email':
                if db_utils.get_entry_by_email_scalar(User, user_data[key]) is not None:
                    response = make_response(jsonify(message="Email duplicate", status=400))
                    response.status_code = 400
                    return response
        user = db_utils.get_entry_by_id(User, user_id)
        db_utils.update_entry(User, user_id, **user_data)
        response = make_response(jsonify(message="User data updated", status=200))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid data input", status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
    return response


@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    # current_identity_id = get_jwt_identity()
    # user = db_utils.get_entry_by_id(User, user_id)
    # if current_identity_id != user.id:
    #     return jsonify('Access is denied')
    try:
        current_identity_id = get_jwt_identity()
        user = db_utils.get_entry_by_id(User, user_id)
        if current_identity_id != user.id:
            return jsonify('Access is denied')

        db_utils.delete_entry(User, user_id)
        response = make_response(jsonify(message="User deleted", status=200))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="User has notes", status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response
