import psycopg2
def history(x):
    try:
        con = None
        cur = None
        con = psycopg2.connect(
            host = 'localhost',
            user = 'postgres',
            password = '1234',
            port = 5432,
            dbname = 'Parking')               #Connection establish from database
        cur = con.cursor()                    #start cursor
        cur.execute('SELECT * FROM PARKING_HISTORY')
        a = cur.fetchall()[-1][3]
        cur.execute('SELECT * FROM PARKING_HISTORY')
        b = cur.fetchall()[-1][4]
        print(a)
        print(b)
        insert_script = 'INSERT INTO parking_history (email,avilable,filled) VALUES (%s,%s,%s)'
        insert_values = ('d',a-1,b+1)
        # print(a)
        cur.execute(insert_script,insert_values)
        # cur.execute('''UPDATE PARKING_HISTORY
        #                SET balance = '100' 
        #                WHERE id = 4''')    
        # sql_update_query = """Update AUTH_USER set balance = %s where id = %s"""
        # cur.execute(sql_update_query, (100, 1))
        # count = cur.rowcount
        # print(count, "Record Updated successfully ")
        con.commit()
    except Exception as error:
            print(error)
    finally:
            if cur is not None:
                cur.close()                         #close cursor
            if con is not None:
                con.close()     
history('1')