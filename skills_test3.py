from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

# YOUR CODE STARTS HERE

@app.route("/api/test",methods = ["GET"])
def get_task():
    tasks= Task.query.all()
    return jsonify([{
        "id":task.id,
        "title":task.title,
        "completed":task.completed

    }
    for task in tasks
    ])

@app.route("/api/test",methods =["POST"])
def new_task():
    data = request.get_json()
    if data is None:
        return jsonify(error = "Invalid Input"),400

    title = data.get("title")

    if not isinstance(title,str) or not title.strip():
        return jsonify(error = "Invalid Format"),404

    new_task = Task(title = title , completed = False)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({
        "id":new_task.id,
        "title":new_task.title,
        "completed": new_task.completed
    })

@app.route("/api/task/<int:task_id",method = ["GET"])
def get_task(task_id):#
    new_task = db.session.get(Task,task_id)
    if new_task is None:
        return jsonify(error = "Does not exist"),404
    return jsonify({
        "id": new_task.id,
        "title":new_task.title,
        "completed": new_task.completed
    })

@app.route("/api/task/<int:task_id",method = ["DELETE"])
def delete_task(task_id):
    Dtask = db.session.get(Task,task_id)
    if Dtask is None:
        return jsonify(error = "Invalid request"),404
    db.session.delete(Dtask)
    db.session.commit()
    return jsonify(message = "Succesfully Deleted"),201