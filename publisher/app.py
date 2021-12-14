from typing import TYPE_CHECKING
import os
import re

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField

from sender import send_msg

if TYPE_CHECKING:
    from werkzeug.datastructures import FileStorage

# configure application
flask_app = Flask(__name__)


@flask_app.route("/")
def index():
    return render_template("index.html", msg="")


class DatePickerFromTo(FlaskForm):
    date_from = DateField('DatePicker', format='%Y-%m-%d')
    date_to = DateField('DatePicker', format='%Y-%m-%d')


@flask_app.route('/report', methods=['POST','GET'])
def report():
    date_picker = DatePickerFromTo()
    if date_picker.validate_on_submit():
        # here is your date slice
        start_date = date_picker.date_from.data.strftime('%Y-%m-%d')
        end_date = date_picker.date_to.data.strftime('%Y-%m-%d')
        return start_date + " " + end_date
    return render_template('report.html', date_picker=date_picker)


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
                    return render_template("index.html", msg="Error: a log file has no '.csv' ending.")

                # read the file
                lines = file.stream.readlines()
                flask_app.logger.info(lines)

                # send the file to RabbitMQ
                for line in lines:
                    line = re.sub(rb'\r\n', b'', line)
                    send_msg(bytes(line))
            finally:
                file.close()
            return render_template("index.html", msg="Successfully sent file")
        except Exception as exc:
            flask_app.logger.error(exc)
            return render_template("index.html", msg="Sending msg failed")

    return render_template("index.html", msg="Sending msg failed")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    SECRET_KEY = os.urandom(32)
    flask_app.config['SECRET_KEY'] = SECRET_KEY
    flask_app.run(debug=True, port=port)
