

from flask import Flask , jsonify , request 

app = Flask(__name__)

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
            

if __name__ == "__main__":
    app.run(debug=True)