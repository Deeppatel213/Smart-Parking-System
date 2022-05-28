import psycopg2 #library to work with postgre
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

def cut(x):
    hostname = 'localhost'
    username = 'postgres'
    password='1234'
    port = 5432
    database = 'Parking'
    conn = None
    cur = None
    try:
        con = psycopg2.connect(
            host = hostname,
            user = username,
            password = password,
            port = port,
            dbname = database)               #Connection establish from database
        cur = con.cursor()                  #start cursor
        cur.execute('SELECT * FROM AUTH_USER')
        for record in cur.fetchall():
            print(record)
        cur.execute('''UPDATE AUTH_USER
SET balance = '100' 
WHERE id = 4''')    
        sql_update_query = """Update AUTH_USER set balance = %s where id = %s"""
        cur.execute(sql_update_query, (100, 1))
        con.commit()
        count = cur.rowcount
        print(count, "Record Updated successfully ")
    except Exception as error:
            print(error)
    finally:
            if cur is not None:
                cur.close()                         #close cursor
            if con is not None:
                con.close()     
    return redirect('/accounts/signin')