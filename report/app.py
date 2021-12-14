import os
import re

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.fields import DateField

# configure application
from postgres_connector import PostgresConnector

flask_app = Flask(__name__)

DATA = None


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
            with PostgresConnector() as conn:
                global DATA
                DATA = [re.sub(r'\(|\)', '', el[0]).split(",") for el in conn.get_data(start_date, end_date)]
            # return redirect(url_for('table', data=['test', 'test1']))
            return redirect(url_for('table'))

    return render_template('report.html', date_picker=date_picker)


@flask_app.route('/table', methods=['GET'])
def table():
    global DATA
    data = DATA
    return render_template('table.html', fetched_data=data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    SECRET_KEY = os.urandom(32)
    flask_app.config['SECRET_KEY'] = SECRET_KEY
    flask_app.run(debug=True, port=port)
