from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("/", methods=["GET"])
def view_tasks():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    tasks = Task.query.all()
    return render_template("tasks.html", tasks=tasks)


@tasks_bp.route("/add", methods=["POST"])
def add_task():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    title = request.form["title"]
    if not title.strip():
        flash("Task cannot be empty.", "error")
        return redirect(url_for("tasks.view_tasks"))

    task = Task(title=title)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for("tasks.view_tasks"))


@tasks_bp.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_status(task_id):
    if "user" not in session:
        return redirect(url_for("auth.login"))

    task = Task.query.get_or_404(task_id)
    if task.status == "Pending":
        task.status = "In Progress"
    elif task.status == "In Progress":
        task.status = "Completed"
    else:
        task.status = "Pending"

    db.session.commit()
    return redirect(url_for("tasks.view_tasks"))


@tasks_bp.route("/clear", methods=["POST"])
def clear_tasks():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    Task.query.delete()
    db.session.commit()
    flash("All tasks cleared.", "info")
    return redirect(url_for("tasks.view_tasks"))
