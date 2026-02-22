import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"


@app.route("/sub.html")
def sub():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))
    return render_template("sub.html", user=user)


app.secret_key = "your_secret_key"


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="todoflow",
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        identity = request.form["designation"]
        gender = request.form["gender"]
        college = request.form.get("college")
        company = request.form.get("company")
        if password != confirm_password:
            flash("Passwords do not match!")
            return render_template("register.html")
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user (username, email, pass, identity, gender, college, company) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (username, email, password, identity, gender, college, company),
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash("Registration successful! Please login.")
            return redirect(url_for("login"))
        except mysql.connector.IntegrityError:
            flash("Email already registered!")
            return render_template("register.html")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pass"]
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user WHERE email = %s AND pass = %s", (email, password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session["user"] = user
            flash("Login successful!")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials!")
            return render_template("login.html")
    return render_template("login.html")


@app.route("/profile")
def profile():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT subscription_type FROM user WHERE email = %s", (user["email"],)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    subscription_type = (
        row["subscription_type"] if row and "subscription_type" in row else "Free"
    )
    user["subscription_type"] = subscription_type
    return render_template("profile.html", user=user)


@app.route("/")
def home():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))
    return render_template("home.html", user=user)


@app.route("/mytasks")
def mytasks():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM task")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("task.html", user=user, tasks=tasks)


@app.route("/api/tasks", methods=["GET"])
def api_get_tasks():
    user = session.get("user")
    if not user:
        return {"error": "Not logged in"}, 401
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, task_name, status, note FROM task")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    mapped_tasks = [
        {
            "id": t["id"],
            "task": t["task_name"],
            "status1": t["status"],
            "notes": t["note"],
        }
        for t in tasks
    ]
    return {"tasks": mapped_tasks}


@app.route("/api/tasks", methods=["POST"])
def api_post_tasks():
    user = session.get("user")
    if not user:
        return {"error": "Not logged in"}, 401
    data = request.get_json()
    tasks = data.get("tasks", [])
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM task")  
    for task in tasks:
        cursor.execute(
            """
            INSERT INTO task (task_name, status, note)
            VALUES (%s, %s, %s)
            """,
            (
                task.get("task", ""),
                task.get("status1", "pending"),
                task.get("notes", ""),
            ),
        )
    conn.commit()
    cursor.close()
    conn.close()
    return {"success": True}


if __name__ == "__main__":
    app.run(debug=True)
