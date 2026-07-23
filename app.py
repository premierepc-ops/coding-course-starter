import os
from dotenv import load_dotenv
from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

app = Flask(__name__)

if not os.environ.get("SECRET_KEY"):
    raise RuntimeError(
        "Missing SECRET_KEY. Set it in Railway Variables or a local .env file "
        "(copy from .env.example)."
    )

app.secret_key = os.environ["SECRET_KEY"]
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

from blueprints.aboutme import aboutme_bp

app.register_blueprint(aboutme_bp, url_prefix="/aboutme")


@app.route("/healthz")
def healthz():
    return "ok", 200


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
