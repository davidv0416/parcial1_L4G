from flask import Flask, flash, render_template, request, redirect, url_for
import bcrypt
from smtplib import SMTP
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

@app.get("/")
def login():
    return render_template("login.html")

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
        password = bcrypt.hashpw(clave, bcrypt.gensalt())
        
        
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
            password,
        ))
        cursor.close()
        
        return redirect(url_for('login'))

"""@app.route('/login', methods=["GET","POST"])
def login():
    if request.method
"""


app.run(debug=True)
