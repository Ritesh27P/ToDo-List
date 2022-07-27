from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.task


@app.route('/')
def home():
    tasks = Todo.query.all()
    not_done_tasks = Todo.query.filter_by(status='0').all()
    done_tasks = Todo.query.filter_by(status='1').all()
    return render_template('index.html', task=not_done_tasks, done_task=done_tasks)


@app.route('/done', methods=['POST', 'GET'])
def done():
    task_done = request.args.get('no')
    print(task_done)
    done_task = Todo.query.filter_by(id=task_done).all()
    for i in done_task:
        i.status = 1
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        task = request.form.get('task')
        new_task = Todo(
            task=task,
            status=0
        )
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
    pass

