from waitress import serve
import app


serve(app.app, host="localhost", port=5000)