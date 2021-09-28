from typing import TYPE_CHECKING
import os

from flask import Flask, render_template, request

from sender import send_msg

if TYPE_CHECKING:
    from werkzeug.datastructures import FileStorage


# configure application
flask_app = Flask(__name__)


@flask_app.route("/")
def index():
    return render_template("index.html")


@flask_app.route("/post_file", methods=["POST"])
def post_file():
    """Get a file from UI and send it to RabbitMQ."""
    if request.method == "POST":
        try:
            # get the file from web UI
            file = request.files['input_file']  # type: FileStorage
            try:
                # check the file is csv
                if not file.filename.endswith('.csv'):
                    return render_template('fail.html')

                # read the file
                lines = file.stream.readlines()
                flask_app.logger.info(lines)

                # send the file to RabbitMQ
                for line in lines:
                    send_msg(bytes(line))
            finally:
                file.close()
            return render_template('success.html')
        except Exception as exc:
            flask_app.logger.error(exc)
            return render_template('fail.html')

    return render_template('fail.html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(debug=True, port=port)
