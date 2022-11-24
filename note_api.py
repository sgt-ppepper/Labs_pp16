from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from models import Notes, Access, User, Change
from schemas import *
import db_utils
import sqlalchemy
import marshmallow
from datetime import datetime

note_bp = Blueprint('note', __name__)


@note_bp.route('/<int:user_id>', methods=['POST'])
@jwt_required()
def create_note(user_id):
    try:
        current_identity_id = get_jwt_identity()
        user = db_utils.get_entry_by_id(User, user_id)
        if current_identity_id != user.id:
            return jsonify(msg='Access is denied')

        note_data = NoteNoId().load(request.json)
        note = db_utils.create_entry_by_uid(Notes, user_id, **note_data)

        user = db_utils.get_entry_by_id(User, user_id)
        user_data = {"notes_count": (user.notes_count+1)}
        db_utils.update_entry(User, user_id, **user_data)

        response = make_response(jsonify(message="Added new note", status=200))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid input", status=400))
        response.status_code = 400
    except sqlalchemy.exc.OperationalError as e:
        response = make_response(jsonify(message="Missing parameter", status=400))
        response.status_code = 400
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
    return response


@note_bp.route('/', methods=['GET'])#
@jwt_required()
def get_all_notes():
    note = db_utils.get_all_entry(Notes)

    response = make_response(jsonify(NoteData(many=True).dump(note)))
    response.status_code = 200
    return response


@note_bp.route('/u/<int:user_id>', methods=['GET'])
@jwt_required()
def get_notes_by_user_id(user_id):
    try:
        current_identity_id = get_jwt_identity()
        user = db_utils.get_entry_by_id(User, user_id)
        if current_identity_id != user.id:
            return jsonify(msg='Access is denied')
        note = db_utils.get_entry_by_user_id(Notes, user_id)
        for has_note in db_utils.get_all_entry_by_uid(Access, user_id):
            note.append(db_utils.get_entry_by_id(Notes, has_note.note_id))

        response = make_response(jsonify(NoteData(many=True).dump(note)))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input", status=404))
        response.status_code = 404
    return response


# TO DO USER CAN CHECK ONLY HIS NOTES
@note_bp.route('/<int:user_id>/<int:note_id>', methods=['GET'])
@jwt_required()
def get_note_by_id(user_id,note_id):
    try:
        current_identity_id = get_jwt_identity()
        user = db_utils.get_entry_by_id(User, user_id)
        if current_identity_id != user.id:
            return jsonify('Access is denied')
        owner = db_utils.is_owner(Access, user_id, note_id)
        if owner:
            note = db_utils.get_entry_by_two_id(Notes, user_id, note_id)
        else:
            note = db_utils.get_entry_by_id(Notes, note_id)

        response = make_response(jsonify(NoteData().dump(note)))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


# TO DO USER CAN CHECK ONLY HIS NOTES
@note_bp.route('/<int:user_id>/findByTitle', methods=['GET'])
@jwt_required()
def get_notes_by_title(user_id):
    try:
        current_identity_id = get_jwt_identity()
        user = db_utils.get_entry_by_id(User, user_id)
        if current_identity_id != user.id:
            return jsonify('Access is denied')
        note_data = NoteByTitle().load(request.json)
        note = db_utils.get_entry_by_title(Notes, user_id, **note_data)

        for has_note in db_utils.get_all_entry_by_uid(Access, user_id):
            note.append(db_utils.get_entry_by_id(Notes, has_note.note_id, **note_data))

        response = make_response(jsonify(NoteData(many=True).dump(note)))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid title input (No note)", status=400))
        response.status_code = 400
    except sqlalchemy.exc.OperationalError as e:
        response = make_response(jsonify(message="Missing parameter", status=400))
        response.status_code = 400
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
    return response


# TO DO USER CAN CHECK ONLY HIS NOTES
@note_bp.route('/<int:user_id>/findByTag', methods=['GET'])
@jwt_required()
def get_notes_by_tags(user_id):
    try:
        current_identity_id = get_jwt_identity()
        user = db_utils.get_entry_by_id(User, user_id)
        if current_identity_id != user.id:
            return jsonify('Access is denied')
        note_data = NoteByTag().load(request.json)
        note = db_utils.get_all_entry_by_tag(Notes, user_id, note_data['tag'])

        for has_note in db_utils.get_all_entry_by_uid(Access, user_id):
            temp = db_utils.get_all_entry_by_id_tag(Notes, has_note.note_id, note_data['tag'])
            note.append(temp)
            print(note[0].id)

        response = make_response(jsonify(NoteData(many=True).dump(note)))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid title input (No note)", status=400))
        response.status_code = 400
    return response


@note_bp.route("<int:user_id>/<int:note_id>", methods=["PUT"])
@jwt_required()
def update_note(user_id, note_id):
    try:
        current_identity_id = get_jwt_identity()
        user = db_utils.get_entry_by_id(User, user_id)
        if current_identity_id != user.id:
            return jsonify('Access is denied')
        owner = db_utils.is_owner(Access, user_id, note_id)
        note_data = NoteToUpdate().load(request.json)
        if owner:
            note = db_utils.get_entry_by_two_id(Notes, user_id, note_id)
        else:
            note = db_utils.get_entry_by_id(Notes, note_id)

        user = db_utils.get_entry_by_id(User, user_id)

        db_utils.update_entry(Notes, note_id, **note_data)
        db_utils.create_change_entry(Change, user_id, note_id, datetime.now())
        response = make_response(jsonify(message="Note data updated", status=200))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input (No note or access)", status=400))
        response.status_code = 400
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400

    return response


@note_bp.route("/owners/<int:user_id>/<int:note_id>", methods=["PUT"])
@jwt_required()
def update_note_owners(user_id, note_id):
    try:
        current_identity_id = get_jwt_identity()
        user = db_utils.get_entry_by_id(User, user_id)
        if current_identity_id != user.id:
            return jsonify('Access is denied')
        if db_utils.get_entry_by_id_count(Access, note_id) > 5:
            response = make_response(jsonify(message="Too much editors", status=400))
            response.status_code = 400
            return response
        access_data = AccessToCreate().load(request.json)
        note = db_utils.get_entry_by_two_id(Notes, user_id, note_id)
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input (No note)", status=400))
        response.status_code = 400
        return response

    if db_utils.get_entry_by_two_id_access(Access, access_data['user_id'], note_id):
        response = make_response(jsonify(message="Already has access", status=400))
        response.status_code = 400
        return response

    try:
        if access_data['user_id'] == user_id:
            response = make_response(jsonify(message="Invalid ID input (Can't give to creator)", status=400))
            response.status_code = 400
            return response
        access = db_utils.create_access_entry(Access, note_id, datetime.now(), **access_data)
        response = make_response(jsonify(message="Successfully added access", status=200))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
    return response


@note_bp.route("/owners/<int:user_id>/<int:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note_owners(user_id, note_id):
    # current_identity_id = get_jwt_identity()
    # user = db_utils.get_entry_by_id(User, user_id)
    # if current_identity_id != user.id:
    #     return jsonify('Access is denied')
    # access_data = AccessToCreate().load(request.json)
    # if access_data['user_id'] == user_id:
    #     response = make_response(jsonify(message="Invalid ID input (Can't delete rights from creator)", status=400))
    #     response.status_code = 400
    #     return response
    try:
        current_identity_id = get_jwt_identity()
        user = db_utils.get_entry_by_id(User, user_id)
        if current_identity_id != user.id:
            return jsonify('Access is denied')
        access_data = AccessToCreate().load(request.json)
        if access_data['user_id'] == user_id:
            response = make_response(jsonify(message="Invalid ID input (Can't delete rights from creator)", status=400))
            response.status_code = 400
            return response

        db_utils.delete_entry_access_by_two_id(Access, access_data['user_id'], note_id)
        response = make_response(jsonify(message="Removed access rights from this user", status=200))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input (No note)", status=400))
        response.status_code = 400
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400

    return response


@note_bp.route("/note/<int:user_id>/<int:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(user_id, note_id):
    # current_identity_id = get_jwt_identity()
    # user = db_utils.get_entry_by_id(User, user_id)
    # if current_identity_id != user.id:
    #     return jsonify('Access is denied')
    try:
        current_identity_id = get_jwt_identity()
        user = db_utils.get_entry_by_id(User, user_id)
        if current_identity_id != user.id:
            return jsonify('Access is denied')

        db_utils.get_entry_by_two_id(Notes, user_id, note_id)
        db_utils.delete_entry_access(Access, note_id)
        db_utils.delete_entry_access(Change, note_id)
        db_utils.delete_entry_by_two_id(Notes, user_id, note_id)
        response = make_response(jsonify(message="Note deleted", status=200))
        response.status_code = 200
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response
