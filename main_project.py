import mysql.connector as m
con = m.connect(host = 'localhost',user = 'root',password = 'system',database='rrs')
cur = con.cursor()
que1 = "create table if not exists user(user_id varchar(20) primary key , name varchar(30) , age int(3) ,gender char(1) ,contact varchar(10) , email varchar(50) , address varchar(20) )"
que2 = "create table if not exists log_in(user_id varchar(20) , login_name varchar(20), password varchar(20) NOT NULL , foreign key(user_id) references user(user_id))"
cur.execute(que1)
cur.execute(que2)
que6 = "create table if not exists train(train_no int primary key , train_name varchar(20) ,  station_name varchar(20) ,platform_no int )"
cur.execute(que6)
que7 = "create table if not exists route(train_no int , source varchar(20), destination varchar(20) , arrival_time int , departure_time int, foreign key(train_no) references train(train_no) )"
cur.execute(que7)
que8 = "create table if not exists status(train_no int , availble_seats int , booked_seats int , waiting_seats int , foreign key(train_no) references train(train_no))"
cur.execute(que8)
que9 = "create table if not exists ticket(train_no int , ticket_no int auto_increment primary key , seat_no int, seat_type varchar(10), passenger_name varchar(30) , passenger_age int(3) , adhaar_no bigint , gender char(1), foreign key(train_no) references train(train_no))"
cur.execute(que9)
que10 = "create table if not exists price(amount int , seat_type varchar(10))"
cur.execute(que10)




def user():
    cur = con.cursor()
    name = input('Name: ')
    age = int(input('Age: '))
    gender = input('Gender M/F: ')
    contact = input('Contact: ')
    email = input('Email: ')
    address = input('Address: ')
    user_id = gender+contact
    que3 = "insert into user values('{}','{}',{},'{}','{}','{}','{}') ".format(user_id,name,age,gender,contact,email,address)
    cur.execute(que3)
    con.commit()
    login_name = input('Enter your Login Name: ')
    password = input('Create a strong Password: ')
    que4 = "insert into log_in values('{}','{}','{}')".format(user_id,login_name,password)
    cur.execute(que4)
    con.commit()
def login():
    test = []
    userid_login =input('Enter your User ID: ')
    cur.execute("select user_id from user")
    data = cur.fetchall()
    for i in data:
        for j in i:
            test.append(j)
    if userid_login not in test:
        print("you have not registered !!")
    else:
        password = input('Enter your Password: ')
        que5 = "select password from log_in where user_id = '{}'".format(userid_login)
        cur.execute(que5)
        pswd = cur.fetchone()
        if pswd[0] == password:
            print("Access Granted")
            return True
        else:
            print("Access Denied..Please Enter correct password ")
            return False
def add_train():
    cur = con.cursor()
    train_no = int(input('Enter train Number: '))
    train_name = input('Enter train Name: ')
    platform_no = int(input('Enter Platform number: '))
    station_name = input('Enter Station Name: ')
    source = input('Enter the Source of Train: ')
    destination = input('Enter the Destination of Train: ')
    arr_time = int(input('Enter the arrival Time: '))
    dep_time = int(input('Enter the Departure Time: '))
    avl = int(input('Enter the Available Seats: '))
    booked = int(input('Enter the Booked Seats: '))
    waiting = int(input('Enter the waiting list Seats: '))
    cur.execute("insert into train values({},'{}','{}',{})".format(train_no,train_name,station_name,platform_no))
    con.commit()
    cur.execute("insert into route values({},'{}','{}',{},{})".format(train_no,source,destination,arr_time,dep_time))
    con.commit()
    cur.execute("insert into status values({},{},{},{})".format(train_no,avl,booked,waiting))
    con.commit()
def train(a):
    cur = con.cursor()
    cur.execute("select * from train where train_no={}".format(a))
    data = cur.fetchall()
    for i in data:
        print(i)
        
def route(a):
    cur = con.cursor()
    cur.execute("select * from route where train_no={}".format(a))
    data = cur.fetchall()
    for i in data:
        print(i)
        
def status(a):
    cur = con.cursor()
    cur.execute("select * from status where train_no={}".format(a))
    data = cur.fetchall()
    for i in data:
        print(i)
    

def ticket():
    test= []
    cur = con.cursor()
    amount = 0
    seatno = 5
    trainno = int(input('Enter the train number: '))
    cur.execute("select train_no from train")
    data = cur.fetchall()
    for i in data:
        for j in i:
            test.append(j)
    if trainno not in test:
        print("Enter a Valid Train Number")
    else:
        cur = con.cursor()
        no_tickets = int(input('ENTER THE NUMBER OF TICKETS: '))
        for i in range(no_tickets):
            cur = con.cursor() 
            pass_name = input('Enter Passenger Name: ')
            pass_age = int(input('Enter pass Age: '))
            pass_adhaar = int(input('Enter Adhaar Number: '))
            pass_gender = input('Enter your gender(M/F): ')
            






            print('''

                                THE FOLLOWING ARE THE COSTS PER TICKET IN DIFFERENT COACHES
                                1. 3A -- 900
                                2. 2A -- 1100
                                3. 1A -- 1550
                                4. 3E -- 750
                                5. CC -- 300
                                6. SL -- 450
                                
                                ''')
            seattype = input('Enter your Seat Type (AS PER GIVEN FORMAT): ')           
            cur.execute("select amount from price where seat_type ='{}'".format(seattype))
            result = cur.fetchone()
            amt = int(result[0])            
            amount += amt
            seatno+=1
            cur.execute("insert into ticket(train_no,seat_no,seat_type,passenger_name,passenger_age,adhaar_no,gender) values ({},{},'{}','{}',{},{},'{}')".format(trainno,seatno,seattype,pass_name,pass_age,pass_adhaar,pass_gender))
            con.commit()
            print('PLEASE CHECK THE DETAILS OF CURRENT PASSENGER...')
            cur.execute("select * from ticket where adhaar_no = {} ".format(pass_adhaar))
            data1 = cur.fetchall()
            for i in data1:
                print (i)

    
        print('THE TOTAL COST OF YOUR TICKET(S) IS ',amount)
        print()

        cur.execute("select booked_seats from status where train_no = {}".format(trainno))
        data3 = cur.fetchall()
        #bs = data3[0] + no_tickets
        cur.execute("update status set booked_seats = booked_seats + 2 where  train_no = {}".format(trainno))
        

def exit():
    print('  THANKYOU FOR USING OUR PROGRAM :)   ')
print('''


            ....WELCOME TO THE RAILWAY RESERVATION SYSTEM ....

            ''')
print()
print()

print('''

1. PRESS 1 IF YOU ARE A NEW USER
2. PRESS 2 IF YOU ALREADY HAVE AN ACCOUNT
      ''')
choice1 = int(input('Enter your Choice: '))
if choice1 == 1:
    user()
    var = login()
    if var == True:
        print('''
                        1. PRESS 1 IF YOU WANT TO VIEW TRAIN DETAILS
                        2. PRESS 2 IF YOU WANT TO BOOK A TICKET
                        3. TO EXIT

                        ''')

        choice2 = int(input('Enter your Choice: '))
        if choice2 == 1:
            print('''

                        1. PRESS 1 TO CHECK TRAIN DETAILS
                        2. PRESS 2 TO CHECK TRAIN ROUTE DETAILS
                        3. PRESS 3 TO CHECK SEAT AVILABILITY


                          ''')
            choice3 = int(input('Enter your Choice: '))
            if choice3  == 1:
                train_num=int(input("enter the train number: "))
                train(train_num)
            elif choice3 == 2:
                train_num=int(input("enter the train number: "))
                route(train_num)
            elif choice3 == 3:
                train_num=int(input("enter the train number: "))
                status(train_num)
            else:
                print('INVALID CHOICE !!!')
                exit()
        elif choice2 == 2:
            ticket()

        elif choice2 == 3:
            exit()
        else:
            exit()
    else:
        exit()

            
elif choice1 == 2:
    var = login()
    if var == True:
        
        print('''
                        1. PRESS 1 IF YOU WANT TO VIEW TRAIN DETAILS
                        2. PRESS 2 IF YOU WANT TO BOOK A TICKET
                        3. TO EXIT

                        ''')

        choice2 = int(input('Enter your Choice: '))
        if choice2 == 1:
            print('''

                        1. PRESS 1 TO CHECK TRAIN DETAILS
                        2. PRESS 2 TO CHECK TRAIN ROUTE DETAILS
                        3. PRESS 3 TO CHECK SEAT AVILABILITY


                          ''')
            choice3 = int(input('Enter your Choice: '))
            if choice3  == 1:
                train_num=int(input("enter the train number: "))
                train(train_num)
            elif choice3 == 2:
                train_num=int(input("enter the train number: "))
                route(train_num)
            elif choice3 == 3:
                train_num=int(input("enter the train number: "))
                status(train_num)
            else:
                print('INVALID CHOICE !!!')
                exit()
        elif choice2 == 2:
            ticket()

        elif choice2 == 3:
            exit()
        else:
            exit()
    else:
        exit()
else:
    print('INVALID CHOICE')
    exit()














