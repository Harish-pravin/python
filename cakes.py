import streamlit as st
from PIL import Image
import mysql.connector
con=mysql.connector.connect(host="localhost",user="root",password="Harish@879",database="hl_store")
res=con.cursor()
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
email1=[]
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked=False
def callback():
    st.session_state.button_clicked=True
def user_registration():
    det=[]
    qry1="select email from cus_det"
    res.execute(qry1)
    data=res.fetchall()
    for i in data:
        det.append(i[0])
    customer_name=st.text_input("enter the name:",placeholder="enter your name")
    city=st.text_input("enter the city:",placeholder="enter your city")
    state=st.text_input("enter the state",placeholder="enter your state")
    password=st.text_input("enter the password",type="password",placeholder="create your new password")
    email=st.text_input("enter your email",placeholder="enter your email")
    eml=email.endswith("@gmail.com")
    pas=len(password)
    if st.button("submit"):
        if email not in det:
            if pas>=6:
                if eml:
                    qry="insert into cus_det (customer_name,city,state,password,email) values(%s,%s,%s,%s,%s)"
                    val=(customer_name,city,state,password,email)
                    res.execute(qry,val)
                    con.commit()
                    st.success("registered")
                else:
                    st.error("enter proper email id")
            else:
                st.error("your password is short...create minimum 6 character")
        else:
            st.error("mail is already there so use another mail")
def employee_registration():
    det=[]
    qry1="select email from employee"
    res.execute(qry1)
    data=res.fetchall()
    for i in data:
        det.append(i[0])
    emp_name=st.text_input("enter the name:",placeholder="enter your name")
    city=st.text_input("enter the city:",placeholder="enter your city")
    role=st.text_input("enter the role",placeholder="enter your role")
    password=st.text_input("enter the password",type="password",placeholder="create your password")
    email=st.text_input("enter your email",placeholder="enter your email")
    eml=email.endswith("@gmail.com")
    pas=len(password)
    if st.button("submit"):
        if email not in det:
            if pas>=6:
                if eml:
                    qry="insert into employee (emp_name,city,role,password,email) values(%s,%s,%s,%s,%s)"
                    val=(emp_name,city,role,password,email)
                    res.execute(qry,val)
                    con.commit()
                    st.success("registered")
                else:
                    st.error("enter proper email id")
            else:
                st.error("your password is short...create minimum 6 character")
        else:
            st.error("mail is already there so use another mail")
def user_validate():
    email=st.text_input("enter your email id:",placeholder="enter your email")
    email1.append(email)
    password=st.text_input("enter the a password",type="password",placeholder="enter your password")
    if st.button("Enter",on_click=callback) or st.session_state.button_clicked:
        det=[]
        qry="select email from cus_det"
        res.execute(qry)
        data=res.fetchall()
        for i in data:
            det.append(i[0])
        if email in det:
            qry1="select password from cus_det where email=%s"
            val=(email,)
            res.execute(qry1,val)
            data=res.fetchall()
            dpass=data[0][0]
            if(password==dpass):
                 st.info("loged in")
                 pur=st.radio("welcome",["select","purchase","cancel"])
                 if(pur=="select"):
                     st.title("select anyone")
                 elif(pur=="purchase"):
                    jc=st.radio("select",["select","Cake","Shake"])
                    if jc=="Cake":
                        purchase()
                    elif jc=="Shake":
                        juice_purchase()
                 elif(pur=="cancel"):
                    jk=st.radio("select",["select","cake","shake"])
                    if jk=="cake":
                        cancel()
                    elif jk=="shake":
                        juice_cancel()
            else:
                st.info("check your password")
        else:
            st.info("check your id")
def employee_validate():
    email=st.text_input("enter your email id:",placeholder="enter your email")
    password=st.text_input("enter the a password",type="password",placeholder="enter your password")
    if st.button("Enter",on_click=callback) or st.session_state.button_clicked:
        det=[]
        qry="select email from employee"
        res.execute(qry)
        data=res.fetchall()
        for i in data:
            det.append(i[0])
        if email in det:
            qry1="select password from employee where email=%s"
            val=(email,)
            res.execute(qry1,val)
            data=res.fetchall()
            dpass=data[0][0]
            if(password==dpass):
                 st.info("loged in")
                 sel=st.selectbox("welcome",["select","new stock","stock update"])
                 if sel=="select":
                     st.info("select anyone")
                 elif sel=="new stock":
                    js=st.radio("select",["select","cake","shake"])
                    if js=="cake":
                        new_stock()
                    elif js=="shake":
                        juice_new_stock()
                 elif sel =="stock update":
                    su=st.radio("select",["select","cake","shake"])
                    if su=="cake":
                        stock_update()
                    elif su=="shake":
                        juice_stock_update()
            else:
                st.info("check your password")
        else:
            st.info("check your id")
  
def new_stock():
    product_name=st.text_input("enter the product_name:")
    per_qty_price=st.number_input("enter the per_qty_price:",value=0 ,step=5)
    qty=st.number_input("enter the qty",value=0,step=1)
    if st.button("submit"):
        qry="insert into product_det (product_name,per_qty_price,qty) values(%s,%s,%s)"
        val=(product_name,per_qty_price,qty)
        res.execute(qry,val)
        con.commit()
        st.info("stock updated")
        qry="select * from product_det"
        res.execute(qry)
        data=res.fetchall()
        df=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price","qty"])
        st.dataframe(df)
def juice_new_stock():
    product_name=st.text_input("enter the product_name:")
    per_qty_price=st.number_input("enter the per_qty_price:",value=0 ,step=5)
    if st.button("submit"):
        qry="insert into juice (product_name,per_qty_price) values(%s,%s)"
        val=(product_name,per_qty_price)
        res.execute(qry,val)
        con.commit()
        st.info("stock updated")
        qry="select * from juice"
        res.execute(qry)
        data=res.fetchall()
        df=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price"])
        st.dataframe(df)
def stock_update():
    a=st.radio("welcome",["select","qty","price"])
    if(a=="select"):
        st.info("select anyone")
    elif(a=="qty"):
        qry="select * from product_det"
        res.execute(qry)
        data=res.fetchall()
        df=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price","qty"])
        st.dataframe(df)
        product_id=st.text_input("enter the product_id:")
        pro=product_id.isnumeric()
        if st.button("submit",on_click=callback) or st.session_state.button_clicked:
            if pro:
                qry1="select * from product_det where product_id=%s"
                val=(product_id,)
                res.execute(qry1,val)
                data=res.fetchall()
                f=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price","qty"])
                st.dataframe(f)
                qty=st.number_input("enter the update qty:",value=0,step=5)
                aqty=qty
                if st.button("apply"):
                    qry2="select qty from product_det where product_id=%s"
                    val=(product_id,)
                    res.execute(qry2,val)
                    data=res.fetchall()
                    sqty=data[0][0]
                    qty=aqty+sqty
                    qry3="update product_det set qty=%s where product_id=%s"
                    val=(qty,product_id)
                    res.execute(qry3,val)
                    con.commit()
                    st.info("updated")
                    qry4="select * from product_det where product_id=%s"
                    val=(product_id,)
                    res.execute(qry4,val)
                    data=res.fetchall()
                    d=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price","qty"])
                    st.dataframe(d)
    elif(a=="price"):
        qry="select * from product_det"
        res.execute(qry)
        data=res.fetchall()
        df=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price","qty"])
        st.dataframe(df)
        product_id=st.text_input("enter the product_id:")
        pro=product_id.isnumeric()
        if st.button("submit",on_click=callback) or st.session_state.button_clicked:
            if pro:
                qry1="select * from product_det where product_id=%s"
                val=(product_id,)
                res.execute(qry1,val)
                data=res.fetchall()
                df=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price","qty"])
                st.dataframe(df)
                per_qty_price=st.number_input("enter the update price:",value=5,step=5)
                if st.button("apply"):
                    qry2="update product_det set per_qty_price=%s where product_id=%s"
                    val=(per_qty_price,product_id)
                    res.execute(qry2,val)
                    con.commit()
                    print("updated")
                    qry3="select * from product_det where product_id=%s"
                    val=(product_id,)
                    res.execute(qry3,val)
                    data=res.fetchall()
                    df=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price","qty"])
                    st.dataframe(df)
def juice_stock_update():
        qry="select * from juice"
        res.execute(qry)
        data=res.fetchall()
        df=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price"])
        st.dataframe(df)
        product_id=st.text_input("enter the product_id:")
        pro=product_id.isnumeric()
        if st.button("submit",on_click=callback) or st.session_state.button_clicked:
            if pro:
                qry1="select * from juice where product_id=%s"
                val=(product_id,)
                res.execute(qry1,val)
                data=res.fetchall()
                df=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price"])
                st.dataframe(df)
                per_qty_price=st.number_input("enter the update price:",value=5,step=5)
                if st.button("apply"):
                    qry2="update juice set per_qty_price=%s where product_id=%s"
                    val=(per_qty_price,product_id)
                    res.execute(qry2,val)
                    con.commit()
                    print("updated")
                    qry3="select * from juice where product_id=%s"
                    val=(product_id,)
                    res.execute(qry3,val)
                    data=res.fetchall()
                    df=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price"])
                    st.dataframe(df)
def purchase():
    qry="select * from product_det"
    res.execute(qry)
    data=res.fetchall()
    df=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price","qty"])
    st.dataframe(df)
    product_id=st.text_input("enter the product_id:")
    pro=product_id.isnumeric()
    if st.button("enter",on_click=callback) or st.session_state.button_clicked:
        if pro==True:
            qry1="select * from product_det where product_id=%s"
            val=(product_id,)
            res.execute(qry1,val)
            data=res.fetchall()
            df=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price","qty"])
            st.dataframe(df)
            qty=st.number_input("enter the qty you want?:",value=0,step=1)
            if st.button("submit", st.session_state.button_clicked):
                dqty=qty
                qry="select qty from product_det where product_id=%s"
                val=(product_id,)
                res.execute(qry,val)
                data=res.fetchall()
                sqty=data[0][0]
                if dqty<=sqty:
                    qry2="update product_det set qty=%s where product_id=%s"
                    qty=sqty-dqty
                    val=(qty,product_id)
                    res.execute(qry2,val)
                    con.commit()
                    qry="select * from product_det where product_id=%s"
                    val=(product_id,)
                    res.execute(qry,val)
                    data=res.fetchall()
                    df=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price","qty"])
                    st.dataframe(df)
                    qry3="select product_name,per_qty_price from product_det where product_id=%s"
                    val=(product_id,)
                    res.execute(qry3,val)
                    data=res.fetchall()
                    product_name=data[0][0]
                    per_qty_price=data[0][1]
                    qty=dqty
                    total_amount=per_qty_price*qty
                    qry4="insert into order_details(product_id,product_name,per_qty_price,qty,total_amount) values (%s,%s,%s,%s,%s)"
                    val=(product_id,product_name,per_qty_price,qty,total_amount)
                    res.execute(qry4,val)
                    con.commit()
                    st.success("purchased")
                    qry5="select * from order_details order by order_id desc limit 1"
                    res.execute(qry5)
                    data=res.fetchall()
                    oi=data[0][0]
                    pi=data[0][1]
                    nm=data[0][2]
                    pprice=data[0][3]
                    qy=data[0][4]
                    ta=data[0][5]
                    df=pd.DataFrame(data,columns=["order_id","product_id","product_name","per_qty_price","qty","total_amount"])
                    st.dataframe(df)
                    sender="harishpravin333@gmail.com"
                    password="niahaebuoxrcgrre"
                    reciever=email1[0]
                    message=MIMEMultipart()
                    message["From"]=sender
                    message["To"]=reciever
                    message["Subject"]="Invoice"
                    body=f" your order id is:{oi}\n product id:{pi}\n name:{nm}\n per qty price:{pprice}\n qty:{qy}\n total amount:{ta}"
                    message.attach(MIMEText(body,"plain"))
                    server=smtplib.SMTP("smtp.gmail.com",587)
                    server.starttls()
                    server.login(sender,password)
                    text=message.as_string()
                    server.sendmail(sender,reciever,text)
                    st.info("mail send succesfully")
                    server.quit()
                else:
                    st.error(f"we have {sqty} qty is available")
def juice_purchase():
    qry="select * from juice"
    res.execute(qry)
    data=res.fetchall()
    df=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price"])
    st.dataframe(df)
    product_id=st.text_input("enter the product_id:")
    pro=product_id.isnumeric()
    if st.button("enter",on_click=callback) or st.session_state.button_clicked:
        if pro==True:
            qry1="select * from juice where product_id=%s"
            val=(product_id,)
            res.execute(qry1,val)
            data=res.fetchall()
            df=pd.DataFrame(data,columns=["product_id","product_name","per_qty_price"])
            st.dataframe(df)
            qty=st.number_input("enter the qty you want?:",value=0,step=1)
            if st.button("submit", st.session_state.button_clicked):
                    qry3="select product_name,per_qty_price from juice where product_id=%s"
                    val=(product_id,)
                    res.execute(qry3,val)
                    data=res.fetchall()
                    product_name=data[0][0]
                    per_qty_price=data[0][1]
                    total_amount=per_qty_price*qty
                    qry4="insert into juice_order_details(product_id,product_name,per_qty_price,qty,total_amount) values (%s,%s,%s,%s,%s)"
                    val=(product_id,product_name,per_qty_price,qty,total_amount)
                    res.execute(qry4,val)
                    con.commit()
                    st.success("purchased")
                    qry5="select * from juice_order_details order by order_id desc limit 1"
                    res.execute(qry5)
                    data=res.fetchall()
                    oi=data[0][0]
                    pi=data[0][1]
                    nm=data[0][2]
                    pprice=data[0][3]
                    qy=data[0][4]
                    ta=data[0][5]
                    df=pd.DataFrame(data,columns=["order_id","product_id","product_name","per_qty_price","qty","total_amount"])
                    st.dataframe(df)
                    sender="harishpravin333@gmail.com"
                    password="niahaebuoxrcgrre"
                    reciever=email1[0]
                    message=MIMEMultipart()
                    message["From"]=sender
                    message["To"]=reciever
                    message["Subject"]="Invoice"
                    body=f" your order id is:{oi}\n product id:{pi}\n name:{nm}\n per qty price:{pprice}\n qty:{qy}\n total amount:{ta}"
                    message.attach(MIMEText(body,"plain"))
                    server=smtplib.SMTP("smtp.gmail.com",587)
                    server.starttls()
                    server.login(sender,password)
                    text=message.as_string()
                    server.sendmail(sender,reciever,text)
                    st.info("mail send succesfully")
                    server.quit()
def cancel():
    qry="select * from order_details"
    res.execute(qry,)
    data=res.fetchall()
    df=pd.DataFrame(data,columns=["order_id","product_id","product_name","per_qty_price","qty","total_amount"])
    st.dataframe(df)
    order_id=st.text_input("enter your orderid:")
    product_id=st.text_input("enter your product_id")
    pro=product_id.isnumeric()
    if st.button("apply",on_click=callback) or st.session_state.button_clicked:
        if pro==True:
            qry="select * from order_details where order_id=%s"
            val=(order_id,)
            res.execute(qry,val)
            data=res.fetchall()
            df=pd.DataFrame(data,columns=["order_id","product_id","product_name","per_qty_price","qty","total_amount"])
            st.dataframe(df) 
            qty=st.number_input("enter your return qty:",value=0,step=1)
            rqty=qty
            if st.button("submit"):
                if(qty>0):
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
                        df=pd.DataFrame(data,columns=["order_id","product_id","product_name","per_qty_price","qty","total_amount"])
                        st.dataframe(df)
                        qry8="select qty from order_details where order_id=%s"
                        val=(order_id,)
                        res.execute(qry8,val)
                        data=res.fetchall()
                        cqty=data[0][0]
                        if(cqty==0):
                            qry9="delete from order_details where order_id=%s"
                            val=(order_id,)
                            res.execute(qry9,val)
                            con.commit()
                    else:
                        st.info("check return qty")
def juice_cancel():
    qry="select * from juice_order_details"
    res.execute(qry,)
    data=res.fetchall()
    df=pd.DataFrame(data,columns=["order_id","product_id","product_name","per_qty_price","qty","total_amount"])
    st.dataframe(df)
    order_id=st.text_input("enter your orderid:")
    product_id=st.text_input("enter your product_id")
    pro=product_id.isnumeric()
    if st.button("apply",on_click=callback) or st.session_state.button_clicked:
        if pro==True:
            qry="select * from juice_order_details where order_id=%s"
            val=(order_id,)
            res.execute(qry,val)
            data=res.fetchall()
            df=pd.DataFrame(data,columns=["order_id","product_id","product_name","per_qty_price","qty","total_amount"])
            st.dataframe(df) 
            qty=st.number_input("enter your return qty:",value=0,step=1)
            rqty=qty
            if st.button("submit"):
                if(rqty>0):
                    qry4="select qty from juice_order_details where order_id=%s"
                    val=(order_id,)
                    res.execute(qry4,val)
                    data=res.fetchall()
                    oqty=data[0][0]
                    if rqty>0 and oqty>=rqty:
                        qry5="update juice_order_details set qty=%s where order_id=%s"
                        qty=oqty-rqty
                        val=(qty,order_id)
                        res.execute(qry5,val)
                        con.commit()
                        qry5="select total_amount from juice_order_details where order_id=%s"
                        val=(order_id,)
                        res.execute(qry5,val)
                        data=res.fetchall()
                        oamount=data[0][0]
                        qry6="select per_qty_price from juice where product_id=%s"
                        val=(product_id,)
                        res.execute(qry6,val)
                        data=res.fetchall()
                        samount=data[0][0]
                        qry7="update juice_order_details set total_amount=%s where order_id=%s"
                        a=samount*rqty
                        total_amount=oamount-a
                        val=(total_amount,order_id)
                        res.execute(qry7,val)
                        con.commit()
                        qry="select * from juice_order_details where order_id=%s"
                        val=(order_id,)
                        res.execute(qry,val)
                        data=res.fetchall()
                        df=pd.DataFrame(data,columns=["order_id","product_id","product_name","per_qty_price","qty","total_amount"])
                        st.dataframe(df)
                        qry8="select qty from juice_order_details where order_id=%s"
                        val=(order_id,)
                        res.execute(qry8,val)
                        data=res.fetchall()
                        cqty=data[0][0]
                        if(cqty==0):
                            qry9="delete from juice_order_details where order_id=%s"
                            val=(order_id,)
                            res.execute(qry9,val)
                            con.commit()
                    else:
                        st.info("check return qty")
wel=st.sidebar.selectbox("Welcome",["select","user","employee"])
if wel=="select":
    st.header("Select your option")
elif wel=="user":
    user=st.sidebar.selectbox("user",["select","registration","login"])
    if user=="select":
        st.header("Welcome To Cake Heist")
        image=Image.open("C:/Users/Harish/Downloads/il_570xN.2793565535_h7v3.jpg")
        st.image(image,use_column_width=True)
    elif user=="registration":
        st.subheader("Register")
        user_registration()
    elif(user=="login"):
        st.subheader("Login")
        user_validate()
elif wel=="employee":
    employee=st.sidebar.selectbox("employee",["select","registration","login"])
    if employee=="select":
        st.header("welcome employee")
    elif(employee=="registration"):
        st.subheader("Register")
        employee_registration()
    elif(employee=="login"):
        st.subheader("Login")
        employee_validate()