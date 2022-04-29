#from crypt import methods
from passlib.hash import sha256_crypt as sha256
import pstats
from flask import Flask, redirect, render_template, request, session, jsonify
from passlib.hash import sha256_crypt
import login,usuarios
import os

app = Flask(__name__)
app.secret_key='979cca07654f433e81e83fbf0cbc9b15'
users_file = 'db/users.csv'
pets_file = 'db/pets.csv'
pets_type_file = 'db/pet_types.csv'


user_dict = usuarios.lee_diccionario_usuarios(users_file)
mails = usuarios.crear_lista_emails(user_dict)
pet_dict = usuarios.lee_lista_mascotas(pets_file)
common_types_list = usuarios.crear_lista_mascotas(pets_type_file)


@app.context_processor
def handle_context():
    return dict(os=os)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if 'logged_in' in session:
            return redirect('/')
        else:
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
                    return render_template("login.html",mensaje=msg)
            else:
                msg = f'Usuario no encontrado.'
                return render_template("login.html",mensaje=msg)

@app.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect("/")

@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        if 'logged_in' in session:
            return redirect("/")
        else:
            return render_template("signup.html")
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            name = request.form['name']
            email = request.form['email']
            type = 'cliente'

            mensajes = []

            if username not in user_dict and email not in mails:
                if email not in mails:
                        password_hashed = sha256_crypt.encrypt(password)
                        user_dict[username] = {
                            'username' : username,
                            'name' : name,
                            'type' : type,
                            'email' : email,
                            'password' : password_hashed
                        }
                        usuarios.update_users_file(user_dict,users_file)
                        return redirect("/login")
            else:
                if email in mails:
                    msg = f'Email ya registrado.'
                    mensajes.append(msg)
                if username in user_dict:
                    msg = f'Usuario ya existe.'
                    mensajes.append(msg)
                return render_template("signup.html",mensajes=mensajes)

@app.route("/agendar_cita", methods=['GET','POST'])
def agendar_cita():
    if request.method == 'GET':
        if 'logged_in' in session:
            user = session['username']
            print(pet_dict[user])
            return render_template("agendar_cita.html", mascotas=pet_dict[user])
        else:
            return redirect("/login")
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            name = request.form['name']
            email = request.form['email']
            type = 'cliente'

            mensajes = []

            if username not in user_dict and email not in mails:
                if email not in mails:
                        password_hashed = sha256_crypt.encrypt(password)
                        user_dict[username] = {
                            'username' : username,
                            'name' : name,
                            'type' : type,
                            'email' : email,
                            'password' : password_hashed
                        }
                        usuarios.update_users_file(user_dict,users_file)
                        return redirect("/login")
            else:
                if email in mails:
                    msg = f'Email ya registrado.'
                    mensajes.append(msg)
                if username in user_dict:
                    msg = f'Usuario ya existe.'
                    mensajes.append(msg)
                return render_template("signup.html",mensajes=mensajes)

@app.route("/administrar_mascotas", methods=['GET','POST'])
def administrar_mascotas():
    if request.method == 'GET':
        if 'logged_in' in session:
            user = session['username']
            #print(common_types_list)
            return render_template("administrar_mascotas.html", mascotas=pet_dict[user], tipos = common_types_list)
        else:
            return redirect("/login")
    else:
        if request.method == 'POST':
            user = session['username']
            if 'submit_button_delete' in request.form.keys():
                pet_name = request.form['submit_button_delete']
                pet_dict[user][pet_name]['active'] = 'False'
                usuarios.update_pets_file(pet_dict,pets_file)
                return redirect('/administrar_mascotas')
            else:
                if 'submit_button_add' in request.form.keys():
                    username = session['username']
                    pet_name = request.form['pet_name'].lower().title()
                    if request.form['select_type'] == 'Otros':
                        pet_type = request.form['other_type']
                    else :
                        pet_type = request.form['select_type']
                        pet_dict[username][pet_name] = {
                            'username' : username,
                            'pet_name' : pet_name,
                            'type'     : pet_type,
                            'active'   : 'True'
                        }
                    usuarios.update_pets_file(pet_dict,pets_file)
                return redirect('/administrar_mascotas')

if __name__ == "__main__":
    app.run(debug=True)
    