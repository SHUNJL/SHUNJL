from hashlib import sha256
import string
from flask import Flask,render_template,request,url_for,redirect
import sqlite3

app=Flask(__name__,template_folder="E:/OneDrive/桌面/software_courses/software_course/software_courses/student/templates")
app.debug=True



@app.route("/")
def home():
    return redirect('welcome')

@app.route("/welcome",methods=["GET", "POST"])
def welcome():
    return render_template('welcome.html')

@app.route("/register",methods=['GET','POST'],endpoint="register_route")
def register():
    if request.method == 'POST':        
        username = request.form.get('username')
        password = request.form.get('password')
        sure_password = request.form.get('sure_password')
        # TODO:得到用户的注册信息，在放在数据库中，要进行唯一性比对 
        
        # 如果输入的两个密码相同，返回提示
        if sure_password != password:
            return ("两次输入的密码不同")

        # 如果输入的密码非空，使用sha256对密码进行哈希处理
        if password is not None:
            password = sha256(password.encode()).hexdigest()

        conn=sqlite3.connect("E:\OneDrive\桌面\software_courses\software_course\software_courses\Database\student.sqlite")
        c=conn.cursor()

        # 检测用户名是否存在
        c.execute("SELECT * FROM login WHERE username = ?", (username,))  
        if c.fetchone() is not None:  
            return ("用户已存在！") 
        
        # 将获得的数据存入数据库
        if username is not None:
            if password is not None:
                c.execute("INSERT INTO login (username, password) VALUES (?, ?)", (username, password))  
                conn.commit()  
        conn.close()  
        
    return render_template('register.html')

@app.route("/login",methods=['GET','POST'],endpoint="login_route")  # 将路由端点改为 'login_route'
def login_route():
    if request.method == 'POST':        
        username = request.form.get('username')
        password = request.form.get('password')   
    # TODO:得到用户名和密码，后期使用数据库校验
    
        # 如果输入的密码不为空，使用sha256对密码进行哈希处理
        if password is not None:
            password = sha256(password.encode()).hexdigest()  
      
        # 连接到数据库  
        conn=sqlite3.connect("E:\OneDrive\桌面\software_courses\software_course\software_courses\Database\student.sqlite")
        c=conn.cursor()
        
        # 查找用户
        if username is not None:
            if password is not None:  
                c.execute("SELECT * FROM login WHERE username = ? AND password = ?", (username, password))  
                user = c.fetchone()  
                
                # 如果找到用户，则登录成功  
                if user:  
                    print("yes")
                    # FIXME:登录成功，设置跳转的页面   
                else:  
                    print("no")  
                    return("密码或用户名错误！")   
        conn.close() 
        
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__=='__main__':

    app.run()