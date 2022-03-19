from flask import Flask, flash, render_template, request, redirect, url_for
import bcrypt
from smtplib import SMTP
from email.message import EmailMessage
import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password= '',
    port=3306,
    database='empresas'    
)
db.autocommit = True


app = Flask(__name__)

"""
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'empresas'
"""
"""
@app.get("/")
def login():
    return render_template("login.html")
"""

@app.route('/registro', methods=["GET","POST"])
def registrar():
    if request.method == 'GET':
        return render_template("registro.html")
    else:
        #recuperar datos del formulario
        nombre = request.form.get('nombre')
        contacto = request.form.get('contacto')
        direccion = request.form.get('direccion')
        correo = request.form.get('correo')
        clave = request.form.get('clave').encode('utf-8')
        passw = bcrypt.hashpw(clave, bcrypt.gensalt())
        
        msg = EmailMessage()
        msg.set_content('Su empresa ha sido registrada satisfactoriamente.')

        msg['Subject'] = 'Confirmación de registro'
        msg['From'] = "davidvivas2020@itp.edu.co"
        msg['To'] = correo

        username = 'davidvivas2020@itp.edu.co'
        password = '1085340013'

        server = SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.send_message(msg)

        server.quit()
        
        is_valid = True
        
        if nombre == "":
            flash("El nombre es requerido")
            is_valid = False 
            
        if contacto == "":
            flash("El contacto es requerido")
            is_valid = False
            
        if not contacto.isdigit():
            flash("El contacto debe de ser un número")
            is_valid = False
        
        if direccion == "":
            flash("La direccion es requerida")
            is_valid = False
        
        if correo == "":
            flash("El correo es requerido")
            is_valid = False
        
        if clave == "":
            flash("La clave es requerida")
            is_valid = False
        
        if is_valid == False:
            return render_template("registro.html",
                    nombre=nombre,
                    contacto=contacto,
                    direccion=direccion,
                    correo=correo,
                    clave=clave,
            )
        #insertar datos a la base de datos
        cursor = db.cursor()
        
        cursor.execute("insert into empresas(nombre, contacto, direccion, correo, clave) values(%s,%s,%s,%s,%s)", (
            nombre,
            contacto,
            direccion,
            correo,
            passw,
        ))
        cursor.close()
        
        return redirect(url_for('login'))

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        clave = request.form.get('clave').encode('utf-8')
        passw = bcrypt.hashpw(clave, bcrypt.gensalt())

        cursor = db.cursor()
        cursor.execute("SELECT * FROM empresas WHERE clave=%s",(clave,))
        user = cursor.fetchone()
        cursor.close()

         
        if (passw == user.encode('utf-8')):
            return render_template("home.html")
        else:
            return "correo o contraeña incorrectos"
        
    else:
        return render_template("login.html")
    



app.run(debug=True)
