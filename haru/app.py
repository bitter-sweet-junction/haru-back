import os

from fastapi import FastAPI


def init_app():
    app = FastAPI()

    return app


if __name__ == "__main__":
    debug = os.environ.get("HARU_DEBUG", default="true").lower() == "true"
    host = os.environ.get("HARU_HOST", default="0.0.0.0")
    port = os.environ.get("HARU_PORT", default="9000")

    app = init_app()
    app.run(debug=debug, host=host, port=port)
