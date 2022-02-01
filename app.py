from flask import Flask, render_template, redirect, url_for, request
from flaskext.mysql import MySQL
from datetime import date

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'bug_tracker'
app.config['MYSQL_DATABASE_HOST'] = ''
mysql.init_app(app)

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email == "admin@gmail.com" and password == "rvitm123":
            return redirect("/")
        elif email == "" and password == "":
            return render_template("login.html", error=0)
        else:
            return render_template("login.html", error=1)

    if request.method == "GET":
        return render_template("login.html")

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "GET":

        #Establish connection with database
        connection = mysql.connect()
        cursor = connection.cursor()

        cursor.execute("select * from issue")
        data = list(cursor.fetchall())

        #Taking runtime bugs from intellij
        cursor.execute("""select max(issue_id) from
                          (select issue_id from issue union all select issue_id from resolved_bugs) T""")
        try:
            issue_id_new = int(str(cursor.fetchone()[0])) + 1
        except:
            issue_id_new = 1

        log_file = open("iLogs", "r")
        flag = 0
        s = log_file.read().splitlines()
        log_file.close()
        open("iLogs", "w").close() #erase contents of file
        error_message = "" 
        title = ""

        #getting error message 
        flag = 0
        for i in s:
            i = i.strip()
            if i.startswith("Exception"):
                x = i.split()
                for a in x:
                    if a.startswith("java.lang"):
                        error_message = error_message + a
                        title = a[10:]
                        title = title[0:len(title) - 1]
                if "at" in i:
                    error_message = error_message + i

            if i.startswith("at"):
                error_message = error_message + " " +  i
                break
        
        #Check if there is already a bug for that error
        same = False
        for i in data:
            if i[3] == error_message or error_message == "":
                same = True
                
        if same == False:
            cursor.execute("select project_id from project where name=%s","Sorting Visualizer")
            project_id = int(cursor.fetchone()[0])
            cursor.execute("select developer_id from developer where project_id=%s", project_id)
            assign_to = int(cursor.fetchone()[0])

            #Adding bug to table
            report = []
            report.append(issue_id_new) #create new issue_id
            report.append(project_id) #Appending project id for Sorting Visualizer
            report.append(title)
            report.append(error_message)
            report.append("Low")
            report.append(date.today().strftime('%Y-%m-%d'))
            report.append(date.today().strftime('%Y-%m-%d'))
            report.append(assign_to)
            print(report)

            #Forming query
            query = """insert into issue values
            (%s, %s, %s, %s, %s, %s, %s, %s)"""

            try:
                cursor.execute(query, report)
            except:
                return "INVALID ENTRIES FOR ISSUE PLEASE CHECK AND TRY AGAIN"

        ####################################

        #Get the names corresponding to the project_id and developer_id
        i = 0
        for i in range(len(data)):
            data[i] = list(data[i])
            p_id = data[i][1]
            d_id = data[i][7]
            desc = data[i][3]
            cursor.execute("select name from project where project_id=%s", p_id)
            project_name = cursor.fetchone()[0]
            cursor.execute("select name from developer where developer_id=%s", d_id)
            developer_name = cursor.fetchone()[0]
            data[i][1] = project_name + " (id: " + str(p_id) + ")"
            data[i][7] = developer_name + " (id: " + str(d_id) + ")"

        connection.commit()
        connection.close()

        return render_template("index.html", query = data)

    elif request.method == "POST":
        return redirect("/report_bug")

@app.route('/projects', methods=['POST', 'GET'])
def projects():
    if request.method == "GET":
        connection = mysql.connect()
        cursor = connection.cursor()

        cursor.execute("select * from project")
        data = cursor.fetchall()
        connection.close()

        return render_template("projects.html", query = data)

    elif request.method == "POST":
        return redirect("/add_project")

@app.route('/developers', methods=['POST', 'GET'])
def developers():

    if request.method == "GET":
        connection = mysql.connect()
        cursor = connection.cursor()

        cursor.execute("select * from developer")
        data = list(cursor.fetchall())

        #Get the names corresponding to the project_id
        i = 0
        for i in range(len(data)):
            data[i] = list(data[i])
            p_id = data[i][3]
            cursor.execute("select name from project where project_id=%s", p_id)
            project_name = cursor.fetchone()[0]
            data[i][3] = project_name + " (id: " + str(p_id) + ")"

        connection.close()
        return render_template("developers.html", query = data)

    elif request.method == "POST":
        return redirect("/add_dev")

@app.route('/report_bug', methods=['POST', 'GET'])
def report_bug():
    if request.method == "POST":
        #Establish connection with database
        connection = mysql.connect()
        cursor = connection.cursor()

        report = []

        #getting new issue_id
        cursor.execute("""select max(issue_id) from
                          (select issue_id from issue union all select issue_id from resolved_bugs) T""")
        try:
            issue_id_new = int(str(cursor.fetchone()[0])) + 1
        except:
            issue_id_new = 1

        report.append(issue_id_new) #create new issue_id
        report.append(request.form.get("project_id"))
        report.append(request.form.get("bug_title"))
        report.append(request.form.get("bug_desc"))
        report.append(request.form.get("bug_priority"))
        report.append(date.today().strftime('%Y-%m-%d'))
        report.append(request.form.get("due_date"))
        report.append(request.form.get("assigned_to"))

        #Forming query
        query = """insert into issue values
        (%s, %s, %s, %s, %s, %s, %s, %s)"""

        try:
            cursor.execute(query, report)
        except:
            return "INVALID ENTRIES FOR ISSUE PLEASE CHECK AND TRY AGAIN"

        connection.commit()
        connection.close()
        return redirect("/")
    else:
        return render_template("report_bug.html")

@app.route('/add_project', methods=['POST', 'GET'])
def add_project():
    if request.method == "POST":
        #Establish connection with database
        connection = mysql.connect()
        cursor = connection.cursor()
        data = []

        #Getting last developer_id and adding 1 to it
        cursor.execute("select max(project_id) from project")
        try:
            project_id_new = int(str(cursor.fetchone()[0])) + 1
        except:
            project_id_new = 1

        try:
            data.append(project_id_new)
            data.append(request.form.get("name"))
            data.append(request.form.get("desc"))
            data.append(date.today().strftime('%Y-%m-%d'))
            
            for i in data:
                if i == "":
                    return "CANNOT ENTER NULL VALUES"

            #Forming query
            query = """insert into project values(%s, %s, %s, %s)"""
            cursor.execute(query, data)
        except:
            return "INVALID ENTRIES FOR PROJECT PLEASE CHECK AND TRY AGAIN"

        connection.commit()
        connection.close()
        return redirect("/projects")
    else:
        return render_template("add_project.html")

@app.route('/add_dev', methods=['POST', 'GET'])
def add_dev():
    if request.method == "POST":
        #Establish connection with database
        connection = mysql.connect()
        cursor = connection.cursor()
        data = []

        #Getting last developer_id and adding 1 to it
        cursor.execute("select max(developer_id) from developer")
        try:
            developer_id_new = int(str(cursor.fetchone()[0])) + 1
        except:
            developer_id_new = 1


        try:
            data.append(developer_id_new)
            data.append(request.form.get("name"))
            data.append(request.form.get("email"))
            data.append(int(request.form.get("project_id")))

            #Forming query
            query = """insert into developer values(%s, %s, %s, %s)"""
            cursor.execute(query, data)
        except:
            return "INVALID ENTRIES FOR DEVELOPER PLEASE CHECK AND TRY AGAIN"

        connection.commit()
        connection.close()
        return redirect("/developers")
    else:
        return render_template("add_dev.html")

@app.route('/submit_resolution', methods=['POST', 'GET'])
def submit_resolution():
    if request.method == "GET":
        return render_template("submit_resolution.html")
    elif request.method == "POST":
        #Establish connection with database
        connection = mysql.connect()
        cursor = connection.cursor()
        data = []

        try:
            bug_title = request.form.get("bug_title")
            bug_id = int(request.form.get("bug_id"))
            cursor.execute("select project_id from issue where issue_id = %s", bug_id)
            project_id = int(cursor.fetchone()[0])

            #check if bug title exists
            cursor.execute("select title from issue where issue_id = %s", bug_id)
            if cursor.fetchone()[0] != bug_title:
                connection.close()
                return "Input bug title is wrong, does not match"

            data.append(bug_id)
            data.append(request.form.get("reso_summary"))
            data.append(date.today().strftime('%Y-%m-%d'))
            data.append(int(request.form.get("developer_id")))
            data.append(project_id)

            #insert into resolved_bugs table
            cursor.execute("insert into resolved_bugs values(%s,%s,%s,%s,%s)", data)

            #delete from issue table
            cursor.execute("delete from issue where issue_id = %s", bug_id)

        except:
            connection.close()
            return "INVALID ENTRIES"

        connection.commit()
        connection.close()
        return "Submitted successfully"

if __name__ == "__main__":
    app.run(port = 8000, debug=True)
