from typing import TYPE_CHECKING
import os

from flask import Flask, render_template, request

if TYPE_CHECKING:
    from werkzeug import FileStorage


# configure application
flask_app = Flask(__name__)


@flask_app.route("/")
def index():
    return render_template("index.html")


@flask_app.route("/post_file", methods=["POST"])
def post_file():
    if request.method == "POST":
        try:
            file = request.files['input_file']  # type: FileStorage
            lines = file.stream.readlines()
            flask_app.logger.info(lines)

            file.close()
            return render_template('success.html')
        except Exception as exc:
            flask_app.logger.error(exc)
            return render_template('fail.html')

    return render_template('fail.html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(debug=True, port=port)
