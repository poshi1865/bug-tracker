'''
author: Naachiket Pant
email: naachiketpant88@gmail.com

'''

import mysql.connector
from mysql.connector import Error


developer = {'developer_id': 0, 'name' : '', 'email' : '', 'project_id': 0}
manager = {'manager_id' : 0, 'manager_name' : ''}
project = {'project_id' : 0, 'name' : '', 'description' : '', 'date_created' : ''}
issue = {'issue_id' : 0, 'project_id' : 0, 'title' : '', 'description' : '', 'priority' : '', 'created_on' : '', 'due_date' : '', 'assigned_to_developer_id' : int}




try:
    connection = mysql.connector.connect(host = 'localhost', database = 'bug_tracker',
                 user = 'naachiket', password = '')

    if connection.is_connected():
        print("Connected")
        cursor = connection.cursor()

        #query
        query = """insert into project values(
                   2, 'Project2', 'This is project 2',
                   '2090-06-26')"""

        cursor.execute(query)
        connection.commit()

except Error as e:
    print(e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed")

