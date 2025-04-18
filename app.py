from flask import Flask

from api import classify_email_route

app = Flask(__name__)
app.register_blueprint(classify_email_route, url_prefix="")

if __name__ == "__main__":
    app.run(debug=True)
