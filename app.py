from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import time
import datetime

app = Flask(__name__)
# mysql db connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sarvesh@localhost/mytest'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


# creating table student
class Studenttest(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))
    dateadd = db.Column(db.String(50))
    datemod = db.Column(db.String(50))

    def __init__(self, name, city, addr, pin, dateadd, datemod):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin
        self.dateadd = dateadd
        self.datemod = datemod


@app.route('/')
def show_all():
    return render_template('show_all.html', students=Studenttest.query.all())


# Method for adding new student
@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            # To add timestamp when new user is created
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            dateadd = timestamp
            student = Studenttest(request.form['name'], request.form['city'], request.form['addr'], request.form['pin'],
                                  dateadd, dateadd)

            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        if not request.form['newname'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            # To add timestamp when new user is created
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            datemod = timestamp
            oldid = request.form['oldid']
            student = Studenttest.query.filter_by(id=oldid).first()
            student.name = request.form['newname']
            student.city = request.form['city']
            student.addr = request.form['addr']
            student.pin = request.form['pin']
            student.id = request.form['newid']
            student.datemod = datemod
            db.session.commit()
            flash('Record was successfully updated')
            return redirect(url_for('show_all'))
    return redirect(url_for('show_all'))


@app.route('/updaterecord', methods=['post', 'get'])
def updaterecord():
    currentname = request.form.get("name")
    currentid = request.form.get("studentid")
    studentupdate = Studenttest.query.filter_by(id=currentid).first()

    return render_template("updaterecord.html", students=studentupdate)


# Method for deleting student
@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("name")
    student = Studenttest.query.filter_by(name=name).first()
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('show_all'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
