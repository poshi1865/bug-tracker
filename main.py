'''
author: Naachiket Pant
email: naachiketpant88@gmail.com

'''

import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host = 'localhost', database = 'bug_tracker', user = 'naachiket', password = '')

    if connection.is_connected():
        print("Connected")
        cursor = connection.cursor()

        #query
        query = """insert into project values(
                    1, 'Omega', 'Nice Project',
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

