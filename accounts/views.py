from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import serial
import time,datetime        
import psycopg2
from django.utils import timezone
from accounts.models import Userinfo,Parking_history,Balance_history

port = 'COM5'

# # Create your views here.
def signup(request):
    if request.method == 'POST':
        first_name=request.POST['fname']
        username=request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if first_name=='' or username=='' or last_name=='' or email=='' or password=='':
            messages.info(request,'Please Fill all details')
            return render(request, 'Signup.html')
        if password!=password1:
            messages.info(request,'Password not match')
            return render(request, 'Signup.html')
        elif User.objects.filter(username=username).exists():
                messages.info(request,'Username is already exist')
                return render(request, 'Signin.html')
        elif User.objects.filter(email=email).exists():
                messages.info(request,'Email is already exist')
                return render(request, 'Signup.html')
        else:
                user = User.objects.create_user(username=first_name,password = password, first_name = first_name,email=email,last_name = last_name)
                user.save();
                temp = Userinfo(username=first_name)
                temp.save()
                user = auth.authenticate(username=username,password=password)
                auth.login(request, user)

                return redirect('/accounts/dashboard')
    else:
        return render(request, 'Signup.html')
def signin(request):
    global user
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username,password=password)
        username = request.user.username
        if user is not None:
            auth.login(request, user)
            return redirect('/accounts/dashboard')
        else:
            messages.info(request,'User not found')
            return render(request, 'Signin.html')
    else:
        return render(request, 'Signin.html')
def logout(request):
    auth.logout(request)
    return redirect('/')
def on(request):
    # arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)
    # arduino.write(bytes('0', 'utf-8'))
    time.sleep(0.05)
    return redirect('/')
def off(request):
    # arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)
    # arduino.write(bytes('1', 'utf-8'))
    time.sleep(0.05)
    return redirect('/')
def dashboard(request):
    # try:
        # arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)
        # arduino.write(bytes('hiii', 'utf-8'))

        username = None
        username = request.user.username
        x = Userinfo.objects.filter(username=username).values('book')
        for i in x:
            book = i['book']
        if book:
            pre = Parking_history.objects.all().last()
            p = Parking_history.objects.filter(user_name=username).last()
            avilable_sloats_book = p.avilable
            filled_sloats_book=p.filled
            book_time_book = p.booking_time
            id_book = p.id

            book_time = book_time_book
            book_time = book_time.time()
            now = datetime.datetime.now().time()
            now = timezone.now()
            now = now.time()

            if book_time<=now:
                username = None
                username = request.user.username
                x = (Userinfo.objects.filter(username=username).values('id','balance','open_gate','inside_gate','book'))
                for i in x:
                    id_book_if = i['id']
                    balance_book_if = i['balance']
                    open_book_if = i['open_gate']
                    inside_book_if = i['inside_gate']
                    book_book_if = i['book']
                book_book_if = False
                temp = Userinfo(username=username,id=id_book_if,open_gate=open_book_if,inside_gate=inside_book_if,book=book_book_if,balance=balance_book_if)
                temp.save()

                avilable_sloats_book+=1
                filled_sloats_book-=1    
                avi_sloat = pre.avilable+1
                fill_sloat = pre.filled-1
                temp = Parking_history(user_name=username,avilable=avi_sloat,filled=fill_sloat,booking_time=book_time_book)
                temp.save()
                # temp = Parking_history(user_name=username,avilable=avilable_sloats_book,filled=filled_sloats_book,booking_time=book_time_book)
                # temp.save()
        x = (Userinfo.objects.filter(username=username).values('id','balance','open_gate','inside_gate','book'))
        for i in x:
            id = i['id']
            balance = i['balance']
            open = i['open_gate']
            inside = i['inside_gate']
            book = i['book']
        p = Parking_history.objects.all().last()
        avilable_sloats = p.avilable
        filled_sloats=p.filled
        avilable_sloats=str(avilable_sloats)
        # arduino.write(bytes(avilable_sloats, 'utf-8'))
        # y = Userinfo(id=id,balance=200,username=username,open_gate=x['open_gate'],inside_gate=x['inside_gate'])
        # y.save()
        total = int(avilable_sloats)+int(filled_sloats)
        
        if avilable_sloats==0:
            sloat=False
        else:
            sloat=True
        if balance>100:
            balanced = True
        else:
                balanced = False
        return render(request, 'test.html',{'balance':balance,'asloats':avilable_sloats,'fsloats':filled_sloats,'total':total,'booked':book,'balanced':balanced,'open':open,'inside':inside,'sloat':sloat})
    # except:
    #     return redirect('/accounts/signin')

def addbalance(request):
    balance_fetch = request.POST['balance']
    balance_fetch=int(balance_fetch)
    username = None
    username = request.user.username
    x = (Userinfo.objects.filter(username=username).values('id','balance','open_gate','inside_gate','book'))
    for i in x:
        id = i['id']
        balance = i['balance']
        open = i['open_gate']
        inside = i['inside_gate']
        book = i['book']
    balance=balance+balance_fetch
    temp = Userinfo(username=username,id=id,open_gate=open,inside_gate=inside,book=book,balance=balance)
    temp.save()
    balance_time = datetime.datetime.now()
    balance_time = timezone.now()
    p = Balance_history.objects.all().last()
    balance_owner = p.owner_earning
    balance_owner+=balance_fetch
    x = Balance_history(user_name=username,balance_time=balance_time,owner_earning=balance_owner,balance_added=balance)
    x.save()
    return redirect('/accounts/dashboard')

def book(request):
    username = None
    username = request.user.username
    x = (Userinfo.objects.filter(username=username).values('id','balance','open_gate','inside_gate','book'))
    for i in x:
        id = i['id']
        balance = i['balance']
        open = i['open_gate']
        inside = i['inside_gate']
        book = i['book']
    balance=balance-100
    book = True
    temp = Userinfo(username=username,id=id,open_gate=open,inside_gate=inside,book=book,balance=balance)
    temp.save()
    p = Parking_history.objects.all().last()
    avilable_sloats = p.avilable
    filled_sloats=p.filled
    avilable_sloats-=1
    filled_sloats+=1
    avilable_sloats = str(avilable_sloats)
    # arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)
    # arduino.write(bytes(avilable_sloats, 'utf-8'))

    book_time = datetime.datetime.now()
    book_time+=datetime.timedelta(seconds=30)
    book_time = timezone.now()
    book_time = book_time + datetime.timedelta(seconds=30)    
    temp = Parking_history(user_name=username,avilable=avilable_sloats,filled=filled_sloats,booking_time=book_time)
    temp.save()
    return redirect('/accounts/dashboard')
def cancel(request):
    username = None
    username = request.user.username

    x = (Userinfo.objects.filter(username=username).values('id','balance','open_gate','inside_gate','book'))
    for i in x:
        id = i['id']
        balance = i['balance']
        open = i['open_gate']
        inside = i['inside_gate']
        book = i['book']
    book = False
    balance=balance+90
    temp = Userinfo(username=username,id=id,open_gate=open,inside_gate=inside,book=book,balance=balance)
    temp.save()
    p = Parking_history.objects.all().last()
    avilable_sloats = p.avilable
    filled_sloats=p.filled
    avilable_sloats+=1
    filled_sloats-=1
    # arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)
    avilable_sloats = str(avilable_sloats)
    # arduino.write(bytes(avilable_sloats, 'utf-8'))    
    temp = Parking_history(user_name=username,avilable=avilable_sloats,filled=filled_sloats)
    temp.save()
    return redirect('/accounts/dashboard')
def open(request):
    username = None
    username = request.user.username
    # arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)
    # arduino.write(bytes('50', 'utf-8'))
    time.sleep(0.05)
    time1 = datetime.datetime.now()
    time1 = timezone.now()
    x = (Userinfo.objects.filter(username=username).values('id','balance','open_gate','inside_gate','book'))
    for i in x:
        id = i['id']
        balance = i['balance']
        open = i['open_gate']
        inside = i['inside_gate']
        book = i['book']
    book = False
    open = True
    inside=True
    temp = Userinfo(username=username,id=id,open_gate=open,inside_gate=inside,book=book,balance=balance)
    temp.save()
    p = Parking_history.objects.filter(user_name=username).values('avilable','filled','id','booking_time')
    for i in p:
        avilable_sloats = i['avilable']
        filled_sloats=i['filled']
        booking_time = i['booking_time']
        booking_time = timezone.now()
        in_time = datetime.datetime.now()
        in_time = timezone.now()
        id = i['id']
    temp = Parking_history(user_name=username,avilable=avilable_sloats,filled=filled_sloats,in_time=in_time,id=id,booking_time=booking_time)
    temp.save()
    return redirect('/accounts/dashboard')
def exit(request):
    username = None
    username = request.user.username
    x = (Userinfo.objects.filter(username=username).values('id','balance','open_gate','inside_gate','book'))
    for i in x:
        id = i['id']
        balance = i['balance']
        open = i['open_gate']
        inside = i['inside_gate']
        book = i['book']
    inside=False
    open=False
    temp = Userinfo(username=username,id=id,open_gate=open,inside_gate=inside,book=book,balance=balance)
    temp.save()
    p = Parking_history.objects.filter(user_name=username).values('avilable','filled','id','in_time','booking_time')
    for i in p:
        in_time = i['in_time']
        id = i['id']
        booking_time = i['booking_time']
        booking_time = timezone.now()
        out_time = datetime.datetime.now()
        out_time = timezone.now()
    abc = Parking_history.objects.all().last()
    avilable_sloats = abc.avilable
    filled_sloats=abc.filled
    avilable_sloats+=1
    filled_sloats-=1
    temp = Parking_history(user_name=username,avilable=avilable_sloats,filled=filled_sloats,in_time=in_time,id=id,out_time=out_time,booking_time=booking_time)
    temp.save()
    temp = Parking_history(user_name=username,avilable=avilable_sloats,filled=filled_sloats,in_time=in_time,out_time=out_time)
    temp.save()
    # arduino = serial.Serial(port=port, baudrate=9600, timeout=.1)
    avilable_sloats = str(avilable_sloats)
    # arduino.write(bytes(avilable_sloats, 'utf-8'))
    return redirect('/accounts/dashboard')