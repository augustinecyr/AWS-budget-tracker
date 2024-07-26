from flask import Flask, render_template, request, redirect, session, url_for
import pymysql.cursors

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection
connection = pymysql.connect(
    host="budget-tracker-user-records.cy7bg9a2u37t.us-east-1.rds.amazonaws.com",
    user="admin",
    password="budgettracker",
    db="budget_tracker",
    cursorclass=pymysql.cursors.DictCursor,
)


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    with connection.cursor() as cursor:
        sql = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()

        if user:
            session["username"] = user["username"]
            return redirect("/dashboard")
        else:
            return "Invalid Credentials"


@app.route("/dashboard")
def dashboard():
    if "username" in session:
        username = session["username"]

        with connection.cursor() as cursor:
            sql = "SELECT * FROM expenses WHERE username=%s"
            cursor.execute(sql, (username,))
            expenses = cursor.fetchall()

        return render_template("dashboard.html", expenses=expenses)
    else:
        return redirect("/")


@app.route("/add_expense", methods=["POST"])
def add_expense():
    if "username" in session:
        month = request.form["month"]
        money_in = request.form["money_in"]
        money_out = request.form["money_out"]
        total = float(money_in) - float(money_out)
        username = session["username"]

        with connection.cursor() as cursor:
            sql = "INSERT INTO expenses (username, month, money_in, money_out) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (username, month, money_in, money_out))
            connection.commit()

        return redirect("/dashboard")
    else:
        return redirect("/")


@app.route("/edit_expense/<int:id>", methods=["GET", "POST"])
def edit_expense(id):
    if "username" in session:
        if request.method == "POST":
            month = request.form["month"]
            money_in = request.form["money_in"]
            money_out = request.form["money_out"]
            # Calculate total (if needed)
            total = float(money_in) - float(money_out)
            username = session["username"]

            with connection.cursor() as cursor:
                sql = "UPDATE expenses SET month=%s, money_in=%s, money_out=%s WHERE id=%s AND username=%s"
                cursor.execute(sql, (month, money_in, money_out, id, username))
                connection.commit()

            return redirect("/dashboard")
        else:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM expenses WHERE id=%s AND username=%s"
                cursor.execute(sql, (id, session["username"]))
                expense = cursor.fetchone()

            return render_template("dashboard.html", expense_to_edit=expense)
    else:
        return redirect("/")


@app.route("/delete_expense/<int:id>", methods=["POST"])
def delete_expense(id):
    if "username" in session:
        with connection.cursor() as cursor:
            sql = "DELETE FROM expenses WHERE id=%s AND username=%s"
            cursor.execute(sql, (id, session["username"]))
            connection.commit()

        return redirect("/dashboard")
    else:
        return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
