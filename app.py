import os
from pathlib import Path

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


env_path = Path(__file__).with_name(".env")
load_dotenv(env_path)

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL was not loaded")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

@app.route("/api/db-test")
def db_test():
    tasks = Task.query.all()

    return jsonify([
        {
            "id": task.id,
            "title": task.title,
            "completed": task.completed
        }
        for task in tasks
    ])
@app.route("/api/db-testing", methods = ["GET","POST"])
def db_testing():
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            return jsonify(error = "Invalid Request"), 400
        title = data.get("title")
        if  not isinstance(title,str) or not title.strip():
            return jsonify(error = "Invalid format"),400
        new_task = Task(title= title,completed = False)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({
            "id" : new_task.id,
             "title": new_task.title,
             "completed" :new_task.completed
        }), 201
    
    
    tasks_list = []


tasks = [
    {
        "id": 1,
        "title": "Learn Flask",
        "completed": False
    },
    {
        "id": 2,
        "title": "Practise Python",
        "completed": True
    }
]


@app.route("/")
def home():
    return "StudyHub is running!"

@app.route("/about")
def about():
    return "StudyHub helps students organise their learning."

@app.route("/api/status")
def api_status():
    return jsonify(
    name="StudyHub",
    status="running",
    version=0.1
)
@app.route("/api/tasks", methods=["GET", "POST"])
def api_tasks():
    if request.method == "GET":
        return jsonify(tasks=tasks)

    if request.method == "POST":
        new_task = request.get_json()
        title = new_task.get("title")

        if not isinstance(title, str) or not title.strip():
            return jsonify(error="Valid title is required"), 400

        new_task["id"] = len(tasks) + 1
        new_task["completed"] = False
        tasks.append(new_task)

        return jsonify(new_task), 201

@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return jsonify(task)
    return jsonify(error="Task not found"), 404

@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def patch_task(task_id):
    data = request.get_json()
    if data is None or "completed" not in data or not isinstance(data["completed"], bool):
        return jsonify(error="Completed status must be true or false"), 400
    for task in tasks:
        if task["id"]== task_id:
            task["completed"]= data["completed"]
            return jsonify(task)
    return jsonify(error="Task not found"), 404

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return jsonify(message="Task deleted") , 200
    return jsonify(error="Task not found"), 404



if __name__ == "__main__":
    app.run(debug=True)