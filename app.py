from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
  __tablename__ = 'persons'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)

  def __repr__(self):
    return f'person.id: {self.id}, person.name: {self.name}'

db.create_all()

@app.route('/')
def index():
  return render_template('index.html', data=Person.query.all())

@app.route('/create', methods=['POST'])
def create():
  name = request.form.get('name', '')
  person = Person(name=name)
  db.session.add(person)
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/createjson', methods=['POST'])
def createjson():
  name = request.get_json()['name']
  person = Person(name=name)
  print(person)
  db.session.add(person)
  db.session.commit()
  return jsonify({
    'name': person.name
  })

