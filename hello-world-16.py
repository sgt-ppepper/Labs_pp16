from flask import Flask
from lab7_var16.blueprint import api_blueprint, errors
app = Flask(__name__)

app.register_blueprint(api_blueprint)
app.register_blueprint(errors)

@app.route('/api/v1/hello-world-16')
def hello_world():
    return 'Hello World! 16'

if __name__ == '__main__':
    app.run()
