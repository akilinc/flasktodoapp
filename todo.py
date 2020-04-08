from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/abdurrahman.kilinc/Spyder/akTODO/todo.db'
app.secret_key = "todoapp"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    iscompleted = db.Column(db.Boolean)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route("/")
def index():
    resultset = Todo.query.all()
    return render_template("index.html", _tuple=resultset)

@app.route("/add", methods=["POST"])
def addtask():
    title = request.form.get("input_title")
    todo = Todo(title=title, iscompleted=False)
    db.session.add(todo)
    db.session.commit()
    flash("Kayıt başarı ile eklendi...", "success")
    return redirect(url_for("index"))

@app.route("/complete/<taskid>", methods=["GET"])
def completetask(taskid):
    task = Todo.query.filter_by(id=taskid).first()
    task.iscompleted = not task.iscompleted
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<taskid>", methods=["GET"])
def deletetask(taskid):
    task = Todo.query.filter_by(id=taskid).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)