import mysql.connector
con=mysql.connector.connect(host="localhost",user="root",password="Harish@879",database="HL_Store")
res=con.cursor()
from tabulate import tabulate
def user_registration():
    customer_name=input("enter the name:")
    city=input("enter the city:")
    state=input("enter the state")
    qry="insert into cus_det (customer_name,city,state) values(%s,%s,%s)"
    val=(customer_name,city,state)
    res.execute(qry,val)
    con.commit()
    print("registered")
def employee_registration():
    emp_name=input("enter the name:")
    city=input("enter the city:")
    role=input("enter the role")
    qry="insert into employee (emp_name,city,role) values(%s,%s,%s)"
    val=(emp_name,city,role)
    res.execute(qry,val)
    con.commit()
    print("registered")
def user_validate():
    det=[]
    qry="select customer_id from cus_det"
    res.execute(qry)
    data=res.fetchall()
    for i in data[0]:
        det.append(1)
    customer_id=int(input("enter your custumer id:"))
    if customer_id in det:
        print("success")
        a=input("1.purchase\n 2.cancel").lower()
        if a=="1":
            purchase()
        elif a=="2":
            cancel()
    else:
        print("check your id")
def employee_validate():
    det=[]
    qry="select emp_id from employee"
    res.execute(qry)
    data=res.fetchall()
    for i in data[0]:
        det.append(1)
    emp_id=int(input("enter your emp id:"))
    if emp_id in det:
        print("success")
        a=input("1.new stock\n 2.update stock").lower()
        if(a=="1"):
            new_stock()
        elif(a=="2" or a=="update stock"):
            stock_update()
    else:
        print("check your id")
def new_stock():
    product_name=input("enter the product_name:")
    per_qty_price=input("enter the per_qty_price:")
    qty=input("enter the qty")
    qry="insert into product_det (product_name,per_qty_price,qty) values(%s,%s,%s)"
    val=(product_name,per_qty_price,qty)
    res.execute(qry,val)
    con.commit()
    print("stock updated")
    qry="select * from product_det"
    res.execute(qry)
    data=res.fetchall()
    print(tabulate(data,headers=["product_id","product_name","per_qty_price","qty"]))
def stock_update():
    a=input("what you want to update 1.qty\n2.price")
    if(a=="1" or a=="qty"):
        qry="select * from product_det"
        res.execute(qry)
        data=res.fetchall()
        print(tabulate(data,headers=["product_id","product_name","per_qty_price","qty"]))
        product_id=int(input("enter the product_id:"))
        qry1="select * from product_det where product_id=%s"
        val=(product_id,)
        res.execute(qry1,val)
        data=res.fetchall()
        print(tabulate(data,headers=["product_id","product_name","per_qty_price","qty"]))
        qty=int(input("enter the update qty:"))
        qry2="update product_det set qty=%s where product_id=%s"
        val=(qty,product_id)
        res.execute(qry2,val)
        con.commit()
        print("updated")
        qry3="select * from product_det where product_id=%s"
        val=(product_id,)
        res.execute(qry3,val)
        data=res.fetchall()
        print(tabulate(data,headers=["product_id","product_name","per_qty_price","qty"]))
    elif(a=="2" or a=="price"):
        qry="select * from product_det"
        res.execute(qry)
        data=res.fetchall()
        print(tabulate(data,headers=["product_id","product_name","per_qty_price","qty"]))
        product_id=int(input("enter the product_id:"))
        qry1="select * from product_det where product_id=%s"
        val=(product_id,)
        res.execute(qry1,val)
        data=res.fetchall()
        print(tabulate(data,headers=["product_id","product_name","per_qty_price","qty"]))
        per_qty_price=int(input("enter the update price:"))
        qry2="update product_det set per_qty_price=%s where product_id=%s"
        val=(per_qty_price,product_id)
        res.execute(qry2,val)
        con.commit()
        print("updated")
        qry3="select * from product_det where product_id=%s"
        val=(product_id,)
        res.execute(qry3,val)
        data=res.fetchall()
        print(tabulate(data,headers=["product_id","product_name","per_qty_price","qty"]))
def purchase():
    qry="select * from product_det"
    res.execute(qry)
    data=res.fetchall()
    print(tabulate(data,headers=["product_id","product_name","per_qty_price","qty"]))
    product_id=int(input("enter the product_id:"))
    qry1="select * from product_det where product_id=%s"
    val=(product_id,)
    res.execute(qry1,val)
    data=res.fetchall()
    print(tabulate(data,headers=["product_id","product_name","per_qty_price","qty"]))
    qty=int(input("enter the qty you want?:"))
    dqty=qty
    qry="select qty from product_det where product_id=%s"
    val=(product_id,)
    res.execute(qry,val)
    data=res.fetchall()
    sqty=data[0][0]
    qry2="update product_det set qty=%s where product_id=%s"
    qty=sqty-dqty
    val=(qty,product_id)
    res.execute(qry2,val)
    con.commit()
    qry="select * from product_det"
    res.execute(qry)
    data=res.fetchall()
    print(tabulate(data,headers=["product_id","product_name","per_qty_price","qty"]))
    qry3="select product_name,per_qty_price from product_det where product_id=%s"
    val=(product_id,)
    res.execute(qry3,val)
    data=res.fetchall()
    product_name=data[0][0]
    per_qty_price=data[0][1]
    qty=dqty
    total_amount=per_qty_price*qty
    qry4="insert into order_details(product_id,product_name,per_qty_price,qty,total_amount) values(%s,%s,%s,%s,%s)"
    val=(product_id,product_name,per_qty_price,qty,total_amount)
    res.execute(qry4,val)
    con.commit()
    print("Than you for purchasing note your order id")
    qry="select * from order_details"
    res.execute(qry)
    data=res.fetchall()
    print(tabulate(data,headers=["order_id","product_id","product_name","per_qty_price","qty"]))
def cancel():
    order_id=int(input("enter your order_id:"))
    qry="select * from order_details where order_id=%s"
    val=(order_id,)
    res.execute(qry,val)
    data=res.fetchall()
    print(tabulate(data,headers=["order_id","product_id","product_name","per_qty_price","qty","total_amount"]))
    order_id=int(input("enter your order_id:"))
    product_id=int(input("enter your product_id:"))
    qry="select * from order_details where order_id=%s"
    val=(order_id,)
    res.execute(qry,val)
    data=res.fetchall()
    print(tabulate(data,headers=["order_id","product_id","product_name","per_qty_price","qty","total_amount"]))
    qty=int(input("enter your return qty:"))
    rqty=qty
    qry4="select qty from order_details where order_id=%s"
    val=(order_id,)
    res.execute(qry4,val)
    data=res.fetchall()
    oqty=data[0][0]
    if(rqty<=oqty and oqty>= 0):
        qry1="select qty from product_det where product_id=%s"
        val=(product_id,)
        res.execute(qry1,val)
        data=res.fetchall()
        sqty=data[0][0]
        qry2="update product_det set qty=%s where product_id=%s"
        qty=sqty+rqty
        val=(qty,product_id)
        res.execute(qry2,val)
        con.commit()
        qry="select * from product_det"
        res.execute(qry)
        data=res.fetchall()
        print(tabulate(data,headers=["product_id","product_name","per_qty_price","qty"]))
        qry5="update order_details set qty=%s where order_id=%s"
        qty=oqty-rqty
        val=(qty,order_id)
        res.execute(qry5,val)
        con.commit()
        qry5="select total_amount from order_details where order_id=%s"
        val=(order_id,)
        res.execute(qry5,val)
        data=res.fetchall()
        oamount=data[0][0]
        qry6="select per_qty_price from product_det where product_id=%s"
        val=(product_id,)
        res.execute(qry6,val)
        data=res.fetchall()
        samount=data[0][0]
        qry7="update order_details set total_amount=%s where order_id=%s"
        a=samount*rqty
        total_amount=oamount-a
        val=(total_amount,order_id)
        res.execute(qry7,val)
        con.commit()
        qry="select * from order_details where order_id=%s"
        val=(order_id,)
        res.execute(qry,val)
        data=res.fetchall()
        print(tabulate(data,headers=["order_id","product_id","product_name","per_qty_price","qty","total_amount"]))
    else:
        print("something error")
while True:
    print("welcome.-.!")
    s=input("1.user\n 2.employee").lower()
    if(s=="1" or s=="user"):
        n=input("1.create account\n 2.Login").lower()
        if(n=="1" or "create account"):
            user_registration()
        elif(n=="2" or n=="login"):
            user_validate()
    elif(s=="2" or s=="employee"):
        x=input("1.employee registration\n 2.log in")
        if(x=="1" or x=="employee registration"):
            employee_registration()
        elif(x=="2" or x=="log in"):
            employee_validate()