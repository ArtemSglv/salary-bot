import mysql.connector

mydb = mysql.connector.connect(host='localhost', user='root', passwd='root', database='salary_bot_db')
mycursor = mydb.cursor()


def execute_select_query(query, val):
    mycursor.execute(query, val)
    return mycursor.fetchall()


def execute_insert_query(query, val):
    print(val)
    mycursor.execute(query, val)
    mydb.commit()
