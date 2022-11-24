from flask import Flask, jsonify
from user_api import user_bp
from note_api import note_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "test"  # Change this!
jwt = JWTManager(app)

app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(note_bp, url_prefix='/api/note')


@app.errorhandler(404)
def server_error(e):
    return jsonify(message="Invalid URL provided", status=404)


#@app.errorhandler(500)
#def server_error(e):
    #return jsonify(message="Server error", status=500)


@app.route('/')
def index():
    return "/api/v1/hello-world-2"


app.run()
