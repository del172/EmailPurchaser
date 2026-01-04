from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.setdefault("SECRET_KEY", "dev-secret-key")

    from routes import register_routes

    register_routes(app)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
