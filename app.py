from flask import Flask, render_template, request, redirect, session, url_for
import pymysql.cursors
import logging
from datetime import datetime
import calendar

app = Flask(__name__)
app.secret_key = "your_secret_key"
logging.basicConfig(filename="app.log", level=logging.DEBUG)

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


def predict_budget(expenses):

    # Helper function to convert month names to datetime objects
    def month_to_date(month_name):
        return datetime.strptime(month_name, "%B")

    if not expenses:
        return [], [], [], []

    # Extract data
    months = [expense["month"] for expense in expenses]
    money_in = [float(expense["money_in"]) for expense in expenses]
    money_out = [float(expense["money_out"]) for expense in expenses]

    # Convert month names to datetime objects if needed
    try:
        last_month = month_to_date(months[-1])
    except ValueError:
        # If conversion fails, return empty lists or handle as needed
        return [], [], [], []

    # Simple prediction logic: using average of past data
    avg_in = sum(money_in) / len(money_in)
    avg_out = sum(money_out) / len(money_out)

    # Predict for the next 3 months
    predicted_months = []
    predicted_in = []
    predicted_out = []
    predicted_total = []

    for i in range(1, 4):  # Predict for next 3 months
        next_month = last_month.month + i
        next_year = last_month.year + (next_month - 1) // 12
        next_month = (next_month - 1) % 12 + 1

        month_name = calendar.month_name[next_month]
        month_str = f"{next_year}-{str(next_month).zfill(2)}"
        predicted_months.append(month_str)
        predicted_in.append(avg_in)
        predicted_out.append(avg_out)
        predicted_total.append(avg_in - avg_out)

    return predicted_months, predicted_in, predicted_out, predicted_total


@app.route("/forecast", methods=["POST"])
def forecast():
    try:
        if "username" in session:
            username = session["username"]

            with connection.cursor() as cursor:
                sql = "SELECT month, money_in, money_out FROM expenses WHERE username=%s ORDER BY month"
                cursor.execute(sql, (username,))
                expenses = cursor.fetchall()

            months, predicted_in, predicted_out, predicted_total = predict_budget(
                expenses
            )

            # Combine data into a list of tuples
            forecast_data = list(zip(months, predicted_in, predicted_out, predicted_total))

            return render_template(
                "forecast.html",
                forecast_data=forecast_data
            )
        else:
            return redirect("/")
    except Exception as e:
        app.logger.error(f"Error in forecast route: {e}")
        return "An error occurred", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
