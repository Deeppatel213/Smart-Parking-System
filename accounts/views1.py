from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import serial
import time
import psycopg2

# # Create your views here.
def signup(request):
    if request.method == 'POST':
        first_name=request.POST['fname']
        username=request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password!=password1:
            messages.info(request,'Password not match')
            return render(request, 'Signup.html')
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username is already exist')
                print("Username is already exist")
                return render(request, 'Signin.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Username is already exist')
                print("Username is already exist")
                return render(request, 'Signup.html')
        else:
                user = User.objects.create_user(username=first_name,password = password, first_name = first_name,email=email,last_name = last_name,)
                user.save();
                print("User Created")
                return redirect('/')
    else:
        return render(request, 'Signup.html')
def signin(request):
    global user
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username,password=password)
        print("USER INFO",user)
        username = user.get_username()
        print(username)
        if user is not None:
            auth.login(request, user)
            print("USER INFO",user)
            # return render(request, 'dashboard.html')
            return redirect('/accounts/dashboard')
        else:
            messages.info(request,'User not found')
            print('usr not found')
            return render(request, 'Signin.html')
    else:
        return render(request, 'Signin.html')
def logout(request):
    auth.logout(request)
    return redirect('/')
def on(request):
    arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)
    arduino.write(bytes('0', 'utf-8'))
    time.sleep(0.05)
    print('ON')
    return redirect('/')
def off(request):
    arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)
    arduino.write(bytes('1', 'utf-8'))
    time.sleep(0.05)
    print('OFf')
    return redirect('/')
def dashboard(request):
    # try:
        username = user.get_username()
        hostname = 'localhost'
        user1 = 'postgres'
        password='1234'
        port = 5432
        database = 'Parking'
        con = None
        cur = None
        balance=0
        book = False
        filled_sloats=0
        avilable_sloats = 0
        try:
            con = psycopg2.connect(
                host = hostname,
                user = user1,
                password = password,
                port = port,
                dbname = database)               #Connection establish from database
            cur = con.cursor()
            script = "SELECT balance,book,open,inside from auth_user WHERE username='"
            script+=username
            script+="'"
            cur.execute(script)
            balance = cur.fetchall()[0][0]
            cur.execute(script)
            cur.execute(script)
            inside = cur.fetchall()[0][3]
            cur.execute(script)
            book = cur.fetchall()[0][1]
            print(book)
            cur.execute(script)
            open = cur.fetchall()[0][2]
            print(open)
            cur.execute('SELECT * FROM PARKING_HISTORY')
            avilable_sloats = cur.fetchall()[-1][4]
            cur.execute('SELECT * FROM PARKING_HISTORY')
            filled_sloats = cur.fetchall()[-1][5]
            total = int(avilable_sloats)+int(filled_sloats)
            if avilable_sloats==0:
                sloat=False
            else:
                sloat=True
            if balance>100:
                balanced = True
            else:
                balanced = False
            con.commit()
        except Exception as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()                         #close cursor
            if con is not None:
                con.close() 
        
        return render(request, 'test.html',{'balance':balance,'asloats':avilable_sloats,'fsloats':filled_sloats,'total':total,'booked':book,'balanced':balanced,'open':open,'inside':inside,'sloat':sloat})
    # except:
    #     return redirect('/accounts/signin')
def addbalance(request):
        balance_fetch = request.POST['balance']
        balance_fetch=int(balance_fetch)
    # try:
        username = user.get_username()
        hostname = 'localhost'
        user1 = 'postgres'
        password='1234'
        port = 5432
        database = 'Parking'
        con = None
        cur = None
        try:
            con = psycopg2.connect(
                host = hostname,
                user = user1,
                password = password,
                port = port,
                dbname = database)               #Connection establish from database
            cur = con.cursor()
            script = "SELECT balance from auth_user WHERE username='"
            script+=username
            script+="'"
            cur.execute(script)
            balance = cur.fetchall()[0][0]
            print(balance)
            balance=balance+balance_fetch
            print(balance)
            script="""UPDATE auth_user
            SET balance = '"""
            script+=str(balance)
            script+="""'WHERE username='"""
            script+=username
            script+="';"
            print('Payment Sucessful')
            cur.execute(script)
            con.commit()
        except Exception as error:
            print(error)
            print('Payment not Sucessful')
        finally:
            if cur is not None:
                cur.close()                         #close cursor
            if con is not None:
                con.close() 
        return redirect('/accounts/dashboard')
def book(request):
        username = user.get_username()
        hostname = 'localhost'
        user1 = 'postgres'
        password='1234'
        port = 5432
        database = 'Parking'
        con = None
        cur = None
        try:
            con = psycopg2.connect(
                host = hostname,
                user = user1,
                password = password,
                port = port,
                dbname = database)               #Connection establish from database
            cur = con.cursor()
            script = "SELECT book from auth_user WHERE username='"
            script+=username
            script+="'"
            cur.execute(script)
            book = cur.fetchall()[0][0]
            print(book)
            script="""UPDATE auth_user
            SET book = 'true'
            WHERE username='"""
            script+=username
            script+="';"
            cur.execute(script)
            cur.execute('SELECT * FROM PARKING_HISTORY')
            a = cur.fetchall()[-1][4]
            cur.execute('SELECT * FROM PARKING_HISTORY')
            b = cur.fetchall()[-1][5]
            insert_script = 'INSERT INTO parking_history (username,avilable,filled) VALUES (%s,%s,%s)'
            insert_values = (username,a-1,b+1)
            cur.execute(insert_script,insert_values)
            print('Booking Sucessful')



            script = "SELECT balance from auth_user WHERE username='"
            script+=username
            script+="'"
            cur.execute(script)
            balance = cur.fetchall()[0][0]
            print(balance)
            balance=balance-100
            print(balance)
            script="""UPDATE auth_user
            SET balance = '"""
            script+=str(balance)
            script+="""'WHERE username='"""
            script+=username
            script+="';"
            print('Payment Sucessful')
            cur.execute(script)

            con.commit()


        except Exception as error:
            print(error)
            print('Booking not Sucessful')
        finally:
            if cur is not None:
                cur.close()                         #close cursor
            if con is not None:
                con.close() 
        return redirect('/accounts/dashboard')
def cancel(request):
        username = user.get_username()
        hostname = 'localhost'
        user1 = 'postgres'
        password='1234'
        port = 5432
        database = 'Parking'
        con = None
        cur = None
        try:
            con = psycopg2.connect(
                host = hostname,
                user = user1,
                password = password,
                port = port,
                dbname = database)               #Connection establish from database
            cur = con.cursor()
            script = "SELECT book from auth_user WHERE username='"
            script+=username
            script+="'"
            cur.execute(script)
            book = cur.fetchall()[0][0]
            print(book)
            script="""UPDATE auth_user
            SET book = 'false'
            WHERE username='"""
            script+=username
            script+="';"
            cur.execute(script)
            cur.execute('SELECT * FROM PARKING_HISTORY')
            a = cur.fetchall()[-1][4]
            cur.execute('SELECT * FROM PARKING_HISTORY')
            b = cur.fetchall()[-1][5]
            insert_script = 'INSERT INTO parking_history (username,avilable,filled) VALUES (%s,%s,%s)'
            insert_values = (username,a+1,b-1)
            cur.execute(insert_script,insert_values)
            print('Booking cancel Sucessful')
            
            script = "SELECT balance from auth_user WHERE username='"
            script+=username
            script+="'"
            cur.execute(script)
            balance = cur.fetchall()[0][0]
            print(balance)
            balance=balance+90
            print(balance)
            script="""UPDATE auth_user
            SET balance = '"""
            script+=str(balance)
            script+="""'WHERE username='"""
            script+=username
            script+="';"
            print('Payment Sucessful')
            cur.execute(script)

            con.commit()

        except Exception as error:
            print(error)
            print('Booking cancel not Sucessful')
        finally:
            if cur is not None:
                cur.close()                         #close cursor
            if con is not None:
                con.close() 
        return redirect('/accounts/dashboard')
def open(request):
    username = user.get_username()
    hostname = 'localhost'
    user1 = 'postgres'
    password='1234'
    port = 5432
    database = 'Parking'
    con = None
    cur = None
    try:
        con = psycopg2.connect(
            host = hostname,
            user = user1,
            password = password,
            port = port,
            dbname = database)               #Connection establish from database
        cur = con.cursor()
        script="""UPDATE auth_user
        SET open = 'true'
        WHERE username='"""
        script+=username
        script+="';"
        cur.execute(script)
        script="""UPDATE auth_user
        SET inside = 'true'
        WHERE username='"""
        script+=username
        script+="';"
        cur.execute(script)
        script="""UPDATE auth_user
            SET book = 'false'
            WHERE username='"""
        script+=username
        script+="';"
        cur.execute(script)
        con.commit()
    except Exception as error:
        print(error)
        print('Booking cancel not Sucessful')
    finally:
        if cur is not None:
            cur.close()                         #close cursor
        if con is not None:
            con.close() 
    return redirect('/accounts/dashboard')
def exit(request):
    username = user.get_username()
    hostname = 'localhost'
    user1 = 'postgres'
    password='1234'
    port = 5432
    database = 'Parking'
    con = None
    cur = None
    try:
        con = psycopg2.connect(
            host = hostname,
            user = user1,
            password = password,
            port = port,
            dbname = database)               #Connection establish from database
        cur = con.cursor()
        script="""UPDATE auth_user
        SET open = 'false'
        WHERE username='"""
        script+=username
        script+="';"
        cur.execute(script)
        script="""UPDATE auth_user
        SET inside = 'false'
        WHERE username='"""
        script+=username
        script+="';"
        cur.execute(script)
        con.commit()
    except Exception as error:
        print(error)
        print('Booking cancel not Sucessful')
    finally:
        if cur is not None:
            cur.close()                         #close cursor
        if con is not None:
            con.close() 
    return redirect('/accounts/dashboard')