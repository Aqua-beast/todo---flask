from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    desc =  db.Column(db.String(500), nullable=False)
    date = db.Column(default=datetime.utcnow)
   
    def __repr__(self) -> str:
        return f"{self.id} - {self.task} - {self.desc}"

@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()

@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        task = request.form.get('task')
        desc = request.form.get('desc')
        if task and desc:
            todo = Todo(task=task, desc=desc)
            db.session.add(todo)
            db.session.commit()
    todos = Todo.query.all()
    return render_template('index.html', todos=todos), 200

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(id=sno).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect('/')

@app.route("/edit/<int:sno>", methods=['GET', 'POST'])
def edit(sno):
    todo = Todo.query.filter_by(id=sno).first()
    if request.method == 'POST':
        todo.task = request.form['task']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', todo=todo)

if __name__ == "__main__":
    app.run(debug=True)
