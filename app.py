from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "projects.db"


def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            technology TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = sqlite3.connect(DATABASE)

    projects = conn.execute(
        "SELECT * FROM projects ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("index.html", projects=projects)


@app.route("/add", methods=["POST"])
def add_project():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    technology = request.form.get("technology", "").strip()

    if title and description and technology:
        conn = sqlite3.connect(DATABASE)

        conn.execute(
            "INSERT INTO projects (title, description, technology) VALUES (?, ?, ?)",
            (title, description, technology)
        )

        conn.commit()
        conn.close()

    return redirect(url_for("home"))


@app.route("/delete/<int:project_id>", methods=["POST"])
def delete_project(project_id):
    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "DELETE FROM projects WHERE id = ?",
        (project_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("home"))


init_db()


if __name__ == "__main__":
    app.run(debug=True)