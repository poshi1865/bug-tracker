'''
author: Naachiket Pant
email: naachiketpant88@gmail.com
'''

import mysql.connector
from mysql.connector import Error
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('./index.html', title = 'Bug-Tracker')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8000)
   
#Dictionaries with tables and values
developer = {'developer_id':0, 'name': '', 'email': '', 'project_id': 0}
issue = {'issue_id': 0, 'project_id': 0, 'title': '', 'description': '', 'priority': '', 'created_on': '',
         'due_date': '', 'assigned_to_developer_id': 0}
manager = {'manager_id': 0, 'manager_name': ''}
project = {'project_id': 0, 'name': '', 'description': '', 'date_created': ''}
solved_bugs = {'issue_id': 0, 'resolution_summary': '', 'closed_on': '', 'resolved_by_dev_id': 0, 'project_id': 0}

def insert(cursor, table, values):
    query = ''
    if table == 'developer':
        query = """insert into developer values(
                   %s, %s, %s, %s)"""

    elif table == 'issue':
        query = """insert into issue values(
                   %s, %s, %s, %s, %s, %s, %s, %s)"""

    elif table == 'manager':
        query = """insert into manager values(
                   %s, %s)"""

    elif table == 'project':
        query = """insert into project values(
                   %s, %s, %s, %s)"""

    elif table == 'solved_bugs':
        query = """insert into solved_bugs values(
                   %s, %s, %s, %s, %s)"""

    #storing values in a tuple
    record = tuple(values)
    cursor.execute(query, record)

#MAIN PROGRAM
try:
    connection = mysql.connector.connect(host = 'localhost', database = 'bug_tracker',
                                         user = 'naachiket', password = '')

    if connection.is_connected():
        print("Connected")

        #cursor object
        cursor = connection.cursor()

        values = [1, 'Naachiket Pant', 'naachiketpant88@gmail.com', 2]
        insert(cursor, 'developer', values)

        connection.commit()

except Error as e:
    print(e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed")
