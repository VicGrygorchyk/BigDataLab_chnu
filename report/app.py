import os
import re
import csv
from io import StringIO

from flask import Flask, render_template, request, redirect, url_for, Response
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
                global SOURCE
                data = conn.get_data(start_date, end_date)
                DATA = [re.sub(r'\(|\)|\s+', '', el[0]).split(",") for el in data]
            # return redirect(url_for('table', data=['test', 'test1']))
            return redirect(url_for('table'))

    return render_template('report.html', date_picker=date_picker)


@flask_app.route('/table', methods=['GET'])
def table():
    data = DATA
    return render_template('table.html', fetched_data=data)


@flask_app.route("/get_csv")
def get_csv():

    def generate():
        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(('date', 'country', 'city', 'click_price'))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # write each log item
        w.writerows(DATA)

        yield data.getvalue()

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"}
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    SECRET_KEY = os.urandom(32)
    flask_app.config['SECRET_KEY'] = SECRET_KEY
    flask_app.run(debug=True, port=port)
