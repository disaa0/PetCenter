from crypt import methods
from flask import Flask, redirect, render_template, request, session, jsonify
from passlib.hash import sha256_crypt
import login,usuarios
import os

app = Flask(__name__)
app.secret_key='979cca07654f433e81e83fbf0cbc9b15'

user_dict = usuarios.lee_diccionario_usuarios('db/users.csv')
mails = usuarios.crear_lista_emails(user_dict)

@app.context_processor
def handle_context():
    return dict(os=os)

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if username in user_dict:
                password_hashed = user_dict[username]['password']
                contrasenia_correcta = sha256_crypt.verify(password,password_hashed)
                if contrasenia_correcta == True:
                    session['username'] = username
                    session['name']   = user_dict[username]['name']
                    session['logged_in']= True
                    session['type'] = user_dict[username]['type']
                    return redirect("/")
                else:
                    msg = f'La contraseña es incorrecta para el usuario {username}'
                    return render_template("login.html",mensaje=msg, alerta=True)
            else:
                msg = f'Usuario no encontrado.'
                return render_template("login.html",mensaje=msg)

@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            name = request.form['name']
            email = request.form['email']
            type = 'cliente'

            if username not in user_dict:
                if email not in emails:
                        password_hashed = sha256_crypt.encrypt(password)
                        session['username'] = username
                        session['name']   = user_dict[username]['name']
                        session['logged_in']= True
                        session['type'] = user_dict[username]['type']
                        return redirect("/")
                else:
                    msg = f'La contraseña es incorrecta para el usuario {username}'
                    return render_template("login.html",mensaje=msg, alerta=True)
            else:
                msg = f'Email ya registrado.'
                return render_template("signup.html",mensaje=msg)
        else:
            msg = f'Usuario ya existe.'
            return render_template("signup.html",mensaje=msg)
if __name__ == "__main__":
    app.run(debug=True)
    