from flask import Blueprint, jsonify, request, make_response
from lab6_var16.models import User, Films, Schelude, Sessions, Visiting, ScheludeHasFilms, ScheludeHasUsers
from lab7_var16.db_utils import *
from lab7_var16.schemas import *
import marshmallow
import sqlalchemy

api_blueprint = Blueprint('user', __name__)
errors = Blueprint('errors', __name__)


@errors.errorhandler(404)
def server_error(e):
    return jsonify(message="Invalid URL provided"), 404


@errors.errorhandler(500)
def server_error(e):
    return jsonify(message="Invalid data provided"), 500


@errors.app_errorhandler(marshmallow.exceptions.ValidationError)
def handle_error(error):
    response = {
        'error': {
            'code': 400,
            'message': "Your data is not valid"
        }
    }

    return jsonify(response), 400


@api_blueprint.route("/user", methods=['POST'])
def create_user():
    try:
        user_data = CreateUser().load(request.json)
        user = create(User, **user_data)
        response = make_response(jsonify(UserData().dump(user)))
        response.status_code = 200
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Creation Error',status=400))
        response.status_code = 400
        return response

@api_blueprint.route("/user/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        user = get_entry_by_id(User,user_id)
        return jsonify(UserData().dump(user))
    except:
        response = make_response(jsonify(message='User is not available',status=400))
        response.status_code = 400
        return response

@api_blueprint.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user_data = UpdateUser().load(request.json)
        user = get_entry_by_id(User,user_id)
        update_entry(user,**user_data)
        response = make_response(jsonify(UserData().dump(user)))
        response.status_code = 200
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
        return response
    except ValueError:
        response = make_response(jsonify(message='Invalid ID',status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='User not found',status=404))
        response.status_code = 404
        return response

@api_blueprint.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    #try:
    a=delete_entry(User,user_id)
    if a:
        response = make_response(jsonify(Id_of_deleted_user=user_id,status=200))
        response.status_code = 200
        return response
    else:
        response = make_response(jsonify(message='User is not available', status=400))
        response.status_code = 400
        return response

@api_blueprint.route("/sessions", methods=["POST"])
def create_session():
     try:
        session_data = CreateSession().load(request.json)
        session = create(Sessions,**session_data)
        response = make_response(jsonify(SessionData().dump(session)))
        response.status_code = 200
        return response
     except marshmallow.exceptions.ValidationError as e:
         response = make_response(jsonify(message=e.args[0], status=400))
         response.status_code = 400
         return response
     except:
         response = make_response(jsonify(message='Invalid input',status=405))
         response.status_code = 405
         return response

@api_blueprint.route("/sessions", methods=["GET"])
def get_sessions():
    session = get_entries(Sessions)
    return jsonify(SessionData(many=True).dump(session))

@api_blueprint.route("/sessions/<int:session_id>", methods=["GET"])
def get_session_by_id(session_id):
    try:
        session = get_entry_by_id(Sessions,session_id)
        return jsonify(SessionData().dump(session))
    except ValueError:
        response = make_response(jsonify(message='Invalid ID',status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Session not found', status=404))
        response.status_code = 404
        return response

@api_blueprint.route("/sessions/<int:session_id>", methods=["DELETE"])
def delete_session(session_id):
    a=delete_entry(Sessions,session_id)
    if a==True:
        response = make_response(jsonify(Id_of_deleted_session=session_id, status=200))
        response.status_code = 200
        return response
    else:
        response = make_response(jsonify(message='Session not found', status=404))
        response.status_code = 404
        return response


@api_blueprint.route("/visiting", methods=["POST"])
def create_visiting():
    try:
        visiting_data = CreateVisiting().load(request.json)
        visiting = create(Visiting, **visiting_data)
        response = make_response(jsonify(VisitingData().dump(visiting)))
        response.status_code = 200
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Invalid input',status=405))
        response.status_code = 405
        return response

@api_blueprint.route("/visiting", methods=["GET"])
def get_visiting():
    visiting = get_entries(Visiting)
    return jsonify(VisitingData(many=True).dump(visiting))

@api_blueprint.route("/visiting/<int:vis_id>", methods=["GET"])
def get_visiting_by_id(vis_id):
    try:
        visiting = get_entry_by_id(Visiting, vis_id)
        return jsonify(VisitingData().dump(visiting))
    except ValueError:
        response = make_response(jsonify(message='Invalid ID',status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Visiting session not found',status=404))
        response.status_code = 404
        return response

@api_blueprint.route("/visiting/<int:vis_id>", methods=["DELETE"])
def delete_visiting(vis_id):
    #try:
    a=delete_entry(Visiting,vis_id)
    if a==True:
        response = make_response(jsonify(ID_of_deleted_visiting=vis_id, status=200))
        response.status_code = 200
        return response
    else:
        response = make_response(jsonify(message='Visiting not found', status=404))
        response.status_code = 404
        return response

    # user buy ticket for specific Film in specific Schedule
@api_blueprint.route("/schedule_sale/<int:user_id>/<int:sch_id>/<int:film_id>", methods=["POST"])
def bound_user(user_id, sch_id, film_id):
    get_entry_by_two_id(ScheludeHasFilms,sch_id,film_id)
    create_entry(ScheludeHasUsers, user_id, sch_id)
    response = make_response(jsonify(message='User was added to schedule succssesfuly', status='200'))
    response.status_code = 200
    return response

@api_blueprint.route("/schedule", methods=["POST"])
def create_schedule():
    try:
        schedule_data = CreateSchedule().load(request.json)
        schedule = create_return(Schelude, **schedule_data)
        response = make_response(jsonify(message='Schedule was added succssesfuly', status='200'))
        response.status_code = 200
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Invalid input',status=405))
        response.status_code = 405
        return response

@api_blueprint.route("/schedule", methods=["GET"])
def get_schedule():
    schedule = get_entries(Schelude)
    return jsonify(ScheduleData(many=True).dump(schedule))

@api_blueprint.route("/schedule/<int:sch_id>", methods=["GET"])
def get_schedule_by_id(sch_id):
    try:
        schedule = get_entry_by_id(Schelude,sch_id)
        return jsonify(ScheduleData().dump(schedule))
    except ValueError:
        response = make_response(jsonify(message='Invalid ID',status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Schedule not found',status=404))
        response.status_code = 404
        return response

@api_blueprint.route("/schedule/<int:sch_id>", methods=["DELETE"])
def delete_schedule(sch_id):
    try:
        a=delete_entry(Schelude,sch_id)
        if a:
            response = make_response(jsonify(ID_of_deleted_schedule=sch_id, status=200))
            response.status_code = 200
            return response
        else:
            response = make_response(jsonify(message='Schedule not found', status=404))
            response.status_code = 404
            return response
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Schedule has session or visiting", status=400))
        response.status_code = 400
        return response


@api_blueprint.route("/films", methods=["POST"])
def create_film():
    try:
        film_data = CreateFilm().load(request.json)
        film = create_return(Films, **film_data)
        response = make_response(jsonify(message="Film was added successfully", status=200))
        response.status_code = 200
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Invalid input',status=405))
        response.status_code = 405
        return response

@api_blueprint.route("/films/<int:film_id>", methods=["PUT"])
def update_film(film_id):
    try:
        film_data = UpdateFilm().load(request.json)
        film = get_entry_by_id(Films, film_id)
        update_entry(film, **film_data)
        response = make_response(jsonify(FilmData().dump(film)))
        response.status_code = 200
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
        return response
    except ValueError:
        response = make_response(jsonify(message='Invalid ID',status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Film not found',status=404))
        response.status_code = 404
        return response

@api_blueprint.route("/films", methods=["GET"])
def get_films():
    film = get_entries(Films)
    return jsonify(FilmData(many=True).dump(film))

@api_blueprint.route("/films/<int:film_id>", methods=["GET"])
def get_film_by_id(film_id):
    try:
        film = get_entry_by_id(Films,film_id)
        return jsonify(FilmData().dump(film))
    except ValueError:
        response = make_response(jsonify(message='Invalid ID',status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Film not found', status=404))
        response.status_code = 404
        return response

@api_blueprint.route("/films/<int:film_id>", methods=["DELETE"])
def delete_film(film_id):
    a=delete_entry(Films,film_id)
    if a:
        response = make_response(jsonify(ID_of_deleted_film=film_id,status=200))
        response.status_code = 200
        return response
    else:
        response = make_response(jsonify(message='Film not found', status=400))
        response.status_code = 400
        return response


    # connect Film to Schedule
@api_blueprint.route("/schedule_film", methods=["POST"])
def bound_admin():
    try:
        admin_data = CreateSheduleFilm().load(request.json)
        if get_entry_scalar(ScheludeHasFilms,**admin_data) is not None:
            response = make_response(jsonify(message='Invalid input', status=405))
            response.status_code = 405
            return response
        admin = create(ScheludeHasFilms, **admin_data)
        response = make_response(jsonify(message="Film was added to schedule successfully", status=200))
        response.status_code = 200
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Invalid input',status=405))
        response.status_code = 405
        return response

