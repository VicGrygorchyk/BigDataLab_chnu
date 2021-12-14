import os

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.fields import DateField


# configure application
flask_app = Flask(__name__)


class DatePickerFromTo(FlaskForm):
    date_from = DateField('DatePicker', format='%Y-%m-%d')
    date_to = DateField('DatePicker', format='%Y-%m-%d')


@flask_app.route("/")
def index():
    return redirect(url_for('report'))


@flask_app.route('/report', methods=['POST', 'GET'])
def report():
    date_picker = DatePickerFromTo()
    if request.method == "POST":
        if date_picker.validate_on_submit():
            # here is your date slice
            start_date = date_picker.date_from.data.strftime('%Y-%m-%d')
            end_date = date_picker.date_to.data.strftime('%Y-%m-%d')
            return start_date + " " + end_date
    return render_template('report.html', date_picker=date_picker)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    SECRET_KEY = os.urandom(32)
    flask_app.config['SECRET_KEY'] = SECRET_KEY
    flask_app.run(debug=True, port=port)
