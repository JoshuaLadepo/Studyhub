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



@app.route("/api/tasks", methods = ["GET","POST"])
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

    if request.method == "GET":
        tasks = Task.query.all()
        return jsonify([
            {
                "id":task.id,
                "title":task.title,
                "completed":task.completed
            }
            for task in tasks
        ]
        )
        
    
@app.route("/api/tasks/<int:task_id>",methods = ["GET"])
def db_get(task_id):
    
        task = db.session.get(Task,task_id)
        if task is None:
            return jsonify(error = "Task not found"), 404
        return jsonify({
            "id":task.id,
            "title":task.title,
            "completed":task.completed
        })

@app.route("/api/tasks/<int:task_id>", methods = ["PATCH"])
def db_update(task_id):
    task = db.session.get(Task,task_id)
    if task is None:
        return jsonify(error= "Task not found"),404

    data= request.get_json()
    if data is None:
        return jsonify(error = "Invalid Request"),400
    completed = data.get("completed")
    if  not isinstance(completed,bool):
        return jsonify(error= "Invalid character format"),400

    task.completed= completed
    db.session.commit()

    return jsonify(
        {
            "id":task.id,
            "title":task.title,
            "completed":task.completed
        }
    )

@app.route("/api/tasks/<int:task_id>",methods=["DELETE"])
def db_delete(task_id):
    task = db.session.get(Task,task_id)
    if task is None:
        return jsonify(error = "Task not found"),404
    db.session.delete(task)
    db.session.commit()
    return jsonify(message = "Task deleted")
    




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



if __name__ == "__main__":
    app.run(debug=True)