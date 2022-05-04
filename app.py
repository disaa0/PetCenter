#from crypt import methods
from dataclasses import replace
from passlib.hash import sha256_crypt as sha256
import pstats
import login,usuarios,citas,recetas
import os
from datetime import datetime, timedelta
from flask import Flask, redirect, render_template, request, session, jsonify
from calendario import delete_event, get_available_days_dict, create_event, search_event


app = Flask(__name__)
app.secret_key='979cca07654f433e81e83fbf0cbc9b15'
users_file = 'db/users.csv'
pets_file = 'db/pets.csv'
pets_type_file = 'db/pet_types.csv'
citas_file = 'db/citas.csv'
drugs_file = 'db/drugs.csv'
prescriptions_file = 'db/prescriptions.csv'


user_dict = usuarios.lee_diccionario_usuarios(users_file)
mails = usuarios.crear_lista_emails(user_dict)
pet_dict = usuarios.lee_lista_mascotas(pets_file)
common_types_list = usuarios.crear_lista_mascotas(pets_type_file)
citas_dict = citas.lee_diccionario_citas(citas_file)
drugs_dict = recetas.lee_diccionario_medicinas(drugs_file)
prescriptions_dict = recetas.lee_diccionario_recetas(prescriptions_file)


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
                contrasenia_correcta = sha256.verify(password,password_hashed)
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
                        password_hashed = sha256.encrypt(password)
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
    availible_days_dict = get_available_days_dict()
    if request.method == 'GET':
        if 'logged_in' in session:
            user = session['username']
            #print(pet_dict[user])
            availible_days_dict = get_available_days_dict()
            #print(availible_days_dict)
            return render_template("agendar_cita.html", mascotas=pet_dict[user], days=availible_days_dict, is_fecha_defined=False)
        else:
            return redirect("/login")
    else:
        user = session['username']
        if request.method == 'POST':
            mensajes = []
            print(request.form['button_used'])
            if request.form['button_used'] == 'appointment':
                fecha_texto = request.form['date_selected']
                fecha = datetime.strptime(fecha_texto, '%d/%m/%Y')
                fecha_formato = fecha.strftime('%Y-%m-%d')
                horario = availible_days_dict[fecha_formato]
                #print(horario[fecha_formato])
                return render_template("agendar_cita.html", mascotas=pet_dict[user], days=availible_days_dict, is_fecha_defined=True, fecha=fecha_texto, horario=horario)
            else:
                tiempo = request.form['hora']
                ini = datetime.strptime(tiempo, '%Y-%m-%d %H:%M:%S')
                inicio1 = ini.isoformat()
                fin = ini + timedelta(hours=1)
                final1 = fin.isoformat()
                inicio = inicio1.replace('T',' ')
                final = final1.replace('T',' ')

                if user not in citas_dict:
                    citas_dict[user] = {}
                if inicio not in citas_dict[user]:
                    citas_dict[user][inicio] = {}

                citas_dict[user][inicio] = {
                    'username':user,
                    'pet_name':request.form['select_pet'],
                    'appointment_type':request.form['select_attention'],
                    'start':inicio,
                    'end':final
                }
                pet_name = citas_dict[user][inicio]['pet_name']
                pet_type = pet_dict[user][pet_name]['type']
                client_name = user_dict[user]['name']
                appointment_type = citas_dict[user][inicio]['appointment_type']
                

                title = 'Cita ' + appointment_type + ' - ' + user
                text = 'Cliente: ' + client_name + '\n' + 'Mascota: ' + pet_name + '\n' + 'Tipo: ' + pet_type
                create_event(title, text, inicio1, final1)
                citas.update_citas_file(citas_dict, citas_file)            
                return redirect('/')


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

@app.route("/recetas", methods=['GET'])
def historial_recetas():
    if request.method == 'GET':
        if 'logged_in' in session:
            user = session['username']
            #print(common_types_list)

            d = {}
            for k, v in prescriptions_dict[user].items():
                for li in v:
                    if li['prescription_id'] not in d:
                        d[li['prescription_id']] = {}
                    d[li['prescription_id']][li['medicine_code']] = li['quantity']
            print(d)

            return render_template("historial_recetas.html", recetas = prescriptions_dict[user], medicinas = drugs_dict, cantidades_dict = d)
        else:
            return redirect("/login")

@app.route("/atencion", methods=['GET','POST'])
def historial_atencion():
    if request.method == 'GET':
        if 'logged_in' in session:
            user = session['username']
            #print(common_types_list)

            citas_usuario = citas_dict[user]

            return render_template("historial_atencion.html", atencion = citas_usuario, sorted_dates = sorted(citas_usuario,reverse=True), hoy = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            return redirect("/login")
    else:
        if request.method == 'POST':
            user = session['username']
            if 'submit_button_delete' in request.form.keys():
                fecha = request.form['submit_button_delete']
                id = search_event(fecha)
                print(id)
                if delete_event(id):
                    citas_dict[user].pop(fecha)
                    citas.update_citas_file(citas_dict,citas_file)
                
                return redirect('/atencion')
if __name__ == "__main__":
    app.run(debug=True)
    