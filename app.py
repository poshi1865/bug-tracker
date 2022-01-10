from flask import Flask, render_template, redirect, url_for, request
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'naachiket'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'bug_tracker'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "GET":
        connection = mysql.connect()
        cursor = connection.cursor()

        cursor.execute("select * from issue")
        data = cursor.fetchall()
        connection.close()

        return render_template("index.html", query = data)

    if request.method == "POST":
        return redirect("/report_bug")

@app.route('/report_bug', methods=['POST', 'GET'])
def report_bug():
    if request.method == "POST":
        return "BUG REPORTED"
    else:
        return render_template("report_bug.html")

if __name__ == "__main__":
    app.run(port = 8000, debug=True)


