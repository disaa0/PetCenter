#INTEGRANTES
#Contreras Rivera Santiago
#Machado Encinas German

#Esta vinculado con un calendario de google: https://calendar.google.com/calendar/u/2?cid=cGV0Y2VudGVydmV0ZXJpbmFyaWE1QGdtYWlsLmNvbQ
#Falto arreglar/agregar: Informe por mes, precios totales no aparecen en el pdf generado, seccion "Olvide mi contraseña".
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

from passlib.hash import sha256_crypt as sha256
import pstats
import login,usuarios,citas,recetas,atencion
from otros import tiene_mascotas, usuario_activo
import os, random
from datetime import datetime, timedelta
from flask import Flask, redirect, render_template, request, session, jsonify, url_for
from flask_weasyprint import HTML, render_pdf
from calendario import delete_event, get_available_days_dict, create_event, search_event


app = Flask(__name__)
app.secret_key='979cca07654f433e81e83fbf0cbc9b15'
users_file = 'db/users.csv'
pets_file = 'db/pets.csv'
pets_type_file = 'db/pet_types.csv'
citas_file = 'db/citas.csv'
drugs_file = 'db/drugs.csv'
measures_file = 'db/measures.csv'
prescriptions_file = 'db/prescriptions.csv'
atencion_file = 'db/atencion.csv'


user_dict = usuarios.lee_diccionario_usuarios(users_file)
mails = usuarios.crear_lista_emails(user_dict)
pet_dict = usuarios.lee_lista_mascotas(pets_file)
common_types_list = usuarios.crear_lista_mascotas(pets_type_file)
citas_dict = citas.lee_diccionario_citas(citas_file)
drugs_dict = recetas.lee_diccionario_medicinas(drugs_file)
measures_list = recetas.crear_lista_medidas(measures_file)
prescriptions_dict = recetas.lee_diccionario_recetas(prescriptions_file)
atencion_dict = atencion.lee_diccionario_atencion(atencion_file)
superdiccionario_usuarios = usuarios.crea_diccionario_clientes(user_dict)


@app.context_processor
def handle_context():
    return dict(os=os)

@app.route("/")
def index():
    return render_template("index.html", index='index')


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
            if usuario_activo(user_dict,username):
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
            type = 'client'
            global mails

            mensajes = []

            if username not in user_dict and email not in mails:
                if email not in mails:
                        password_hashed = sha256.encrypt(password)
                        user_dict[username] = {
                            'username' : username,
                            'name' : name,
                            'type' : type,
                            'email' : email,
                            'password' : password_hashed,
                            'active' : 'True'
                        }
                        usuarios.update_users_file(user_dict,users_file)
                        mails = usuarios.crear_lista_emails(user_dict)
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
    mensajes = []
    if request.method == 'GET':
        if 'logged_in' in session:
            type = session['type']
            if 'client' in session:
                session.pop('client', None)
            availible_days_dict = get_available_days_dict()
            if type == 'client':
                user = session['username']
                session['client'] = user
                if not tiene_mascotas(pet_dict,user):
                    mascotas = ''
                    mensajes.append("Usted no tiene mascotas activas")
                else:
                    mascotas = pet_dict[user]
                #print(pet_dict[user])                
                return render_template("agendar_cita.html", mascotas=mascotas, days=availible_days_dict, is_fecha_defined=False, is_user_selected=True, usuario = user, mensajes=mensajes)
            else:
                if type == 'admin' or type == 'user':
                    mascotas = pet_dict
                    return render_template("agendar_cita.html", mascotas=pet_dict, days=availible_days_dict, is_fecha_defined=False, usuarios=user_dict, is_user_selected=False, mensajes=mensajes)
            
        else:
            return redirect("/login")
    else:
        if request.method == 'POST':
            if 'select_user' in request.form:
                user = request.form['select_user']
                print(tiene_mascotas(pet_dict, user))
                if not tiene_mascotas(pet_dict,user):
                    mensajes.append("Usuario "+ user +" sin mascotas activas")
                    return render_template("agendar_cita.html", mascotas=pet_dict, days=availible_days_dict, is_fecha_defined=False, usuarios=user_dict, is_user_selected=False, mensajes=mensajes)
                else:
                    session['client'] = user
                    return render_template("agendar_cita.html", mascotas=pet_dict[user], days=availible_days_dict, is_fecha_defined=False, is_user_selected=True, usuario = user, mensajes=mensajes)
            else:
                #print(request.form)
                if 'button_used' in request.form:
                    user = session['client']
                    if request.form['button_used'] == 'appointment':
                        fecha_texto = request.form['date_selected']
                        fecha = datetime.strptime(fecha_texto, '%d/%m/%Y')
                        fecha_formato = fecha.strftime('%Y-%m-%d')
                        mascotas = pet_dict[user]
                        if fecha_formato not in availible_days_dict:
                            mensajes.append("No puede realizar citas en periodos mayores de un año")
                            return render_template("agendar_cita.html", mascotas=mascotas, days=availible_days_dict, is_fecha_defined=False, is_user_selected=True, usuario = user, mensajes=mensajes)
                        horario = availible_days_dict[fecha_formato]
                        #print(horario[fecha_formato])
                        return render_template("agendar_cita.html", mascotas=mascotas, days=availible_days_dict, is_fecha_defined=True, fecha=fecha_texto, horario=horario, is_user_selected=True, usuario = user)
                if 'agendar' in request.form:
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


@app.route("/mascotas", methods=['GET','POST'])
def administrar_mascotas():
    mensajes = []
    if request.method == 'GET':
        if 'logged_in' in session:
            if 'client' in session:
                session.pop('client', None)
            type = session['type']
            if type == 'client':
                user = session['username']
                session['client'] = user
                #print(common_types_list)
                if not tiene_mascotas(pet_dict,user):
                    mensajes.append('Usted no tiene mascotas activas registradas')
                    mascotas = ''
                else:
                    mascotas = pet_dict[user]
                return render_template("administrar_mascotas.html", mascotas=mascotas, tipos = common_types_list, mensajes=mensajes)
            else:
                return render_template("administrar_mascotas.html", usuarios=user_dict, mascotas_completo=pet_dict, mensajes=mensajes)

        else:
            return redirect("/login")
    else:
        if request.method == 'POST':
            if 'select_user' in request.form:
                user = request.form['select_user']
                session['client'] = user
                if user not in pet_dict:
                    mensajes.append('Usuario ' + user + ' no tiene mascotas registradas')
                    mascotas = {}
                else:
                    mascotas = pet_dict[user]
                return render_template("administrar_mascotas.html", mascotas=mascotas, tipos = common_types_list, mensajes=mensajes)
            else:
                user = session['client']
                if 'submit_button_delete' in request.form.keys():
                    pet_name = request.form['submit_button_delete']
                    pet_dict[user][pet_name]['active'] = 'False'
                    usuarios.update_pets_file(pet_dict,pets_file)
                    return redirect('/mascotas')
                else:
                    if 'submit_button_add' in request.form.keys():
                        username = session['client']
                        pet_name = request.form['pet_name'].lower().title()
                        if request.form['select_type'] == 'Otros':
                            pet_type = request.form['other_type']
                        else :
                            pet_type = request.form['select_type']
                        if pet_type not in common_types_list:
                            pet_type = request.form['other_type']
                        if user not in pet_dict:
                            pet_dict[user] = {}
                        pet_dict[username][pet_name] = {
                            'username' : username,
                            'pet_name' : pet_name,
                            'type'     : pet_type,
                            'active'   : 'True'
                        }
                        usuarios.update_pets_file(pet_dict,pets_file)
                        return redirect('/mascotas')

@app.route("/recetas", methods=['GET','POST'])
def historial_recetas():
    mensajes = []
    if request.method == 'GET':
        if 'logged_in' in session:
            type = session['type']
            if 'client' in session:
                session.pop('client', None)
            if type == 'client':
                user = session['username']
                session['client'] = user
                if user not in prescriptions_dict:
                    mensajes.append('Usted no tiene recetas')
                    return render_template("historial_recetas.html", mensajes=mensajes)
                else:
                    d = {}
                    for k, v in prescriptions_dict[user].items():
                        for li in v:
                            if li['prescription_id'] not in d:
                                d[li['prescription_id']] = {}
                            d[li['prescription_id']][li['medicine_code']] = li['quantity']
                    #print(d)
                    return render_template("historial_recetas.html", recetas = prescriptions_dict[user], medicinas = drugs_dict, cantidades_dict = d)
            else:
                if session['type'] == 'user' or session['type'] == 'admin':
                    d = {}
                    #print(prescriptions_dict)
                    for u, data in prescriptions_dict.items():
                        for k, v in prescriptions_dict[u].items():
                            for li in v:
                                #print(u,k,li)
                                if u not in d.keys():
                                    d[u] = {}
                                if li['prescription_id'] not in d[u].keys():
                                    d[u][li['prescription_id']] = {}
                                d[u][li['prescription_id']][li['medicine_code']] = li['quantity']
                    return render_template("historial_recetas.html", medicinas = drugs_dict, usuarios=user_dict, recetas_completo=prescriptions_dict, cantidades_dict = d)
        else:
            return redirect("/login")
    else:
        if request.method == 'POST':
            type = session['type']
            d = {}
            if 'select_user' in request.form:
                user = request.form['select_user']
                session['client'] = user
                if not tiene_mascotas(pet_dict,user):
                    mensajes.append('Usuario ' + user + ' sin mascotas activas')
                    mascotas = {}
                else:
                    mascotas = pet_dict[user]
                if user not in prescriptions_dict:
                    mensajes.append('Usuario ' + user + ' sin recetas')
                    recetas_enviar = {}
                else:
                    for k, v in prescriptions_dict[user].items():
                        for li in v:
                            if li['prescription_id'] not in d:
                                d[li['prescription_id']] = {}
                            d[li['prescription_id']][li['medicine_code']] = li['quantity']
                    recetas_enviar = prescriptions_dict[user]
                return render_template("historial_recetas.html", recetas = recetas_enviar, mascotas=mascotas, medicinas = drugs_dict, cantidades_dict = d, mensajes=mensajes)
            else:
                user = session['client']
                pet_name = request.form['select_pet']
                hoy = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                code = datetime.now().strftime('%Y%m%d%H%M%S') + chr(random.randint(65, 122))
                medicamentos = []
                for element in request.form:
                    if element[1:] in drugs_dict:
                        medicamentos.append(element[1:])
                if user not in prescriptions_dict:
                            prescriptions_dict[user] = {}
                if code not in prescriptions_dict[user]:
                    prescriptions_dict[user][code] = []
                #print(medicamentos)
                for medicamento in medicamentos:
                    #print(user,pet_name,code,request.form['c'+medicamento],hoy)
                    prescriptions_dict[user][code].append({
                    'prescription_id'   : code,
                    'username'          : user,
                    'pet_name'          : pet_name,
                    'medicine_code'     : medicamento,
                    'quantity'          : request.form['c'+medicamento],
                    'date'              : hoy
                })
                recetas.update_prescriptions_file(prescriptions_dict,prescriptions_file)
                return redirect('/recetas')


@app.route("/citas", methods=['GET','POST'])
def historial_citas():
    mensajes = []
    if request.method == 'GET':
        if 'logged_in' in session:
            if 'client' in session:
                session.pop('client', None)
            if session['type'] == 'client':
                user = session['username']
                session['client'] = user
                #print(common_types_list)
                if user not in citas_dict:
                    mensajes.append('Ustead no ha realizado ninguna cita')
                    citas_usuario = ''
                else:
                    citas_usuario = citas_dict[user]
                return render_template("historial_citas.html", atencion = citas_usuario, sorted_dates = sorted(citas_usuario,reverse=True), hoy = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), mensajes=mensajes)
            else:
                usuarios = user_dict
                return render_template("historial_citas.html", hoy = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), usuarios=usuarios, mensajes=mensajes)
        else:
            return redirect("/login")
    else:
        if request.method == 'POST':
            type = session['type']
            if 'select_user' in request.form:
                user = request.form['select_user']
                session['client'] = user
                if user not in citas_dict:
                    mensajes.append('Usuario ' + user + ' no ha realizado citas')
                    citas_usuario = {}
                else:
                    citas_usuario = citas_dict[user]
                return render_template("historial_citas.html", atencion = citas_usuario, sorted_dates = sorted(citas_usuario,reverse=True), hoy = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), mensajes=mensajes)
            else:
                user = session['client']
                if 'submit_button_delete' in request.form.keys():
                    fecha = request.form['submit_button_delete']
                    id = search_event(fecha)
                    #print(id)
                    if delete_event(id):
                        citas_dict[user].pop(fecha)
                        citas.update_citas_file(citas_dict,citas_file)
                    return redirect('/citas')

@app.route("/atencion", methods=['GET','POST'])
def historial_atencion():
    mensajes = []
    if request.method == 'GET':
        if 'logged_in' in session:
            if 'client' in session:
                session.pop('client', None)
            if session['type'] == 'client':
                user = session['username']
                session['client'] = user
                user_dates_dict = {}
                for id, pets in atencion_dict.items():
                    for pet, dates in pets.items():
                        for date, column in dates.items():
                            if id not in user_dates_dict:
                                user_dates_dict[id] = []
                            user_dates_dict[id].append(date)
                if not tiene_mascotas(pet_dict,user):
                    mascotas = {}
                else:
                    mascotas = pet_dict[user]
                if user not in atencion_dict:
                    mensajes.append('Usted no cuenta con atenciones previas')
                    atenciones = {}
                    fechas_atenciones = []
                else:
                    fechas_atenciones = user_dates_dict[user]
                    atenciones = atencion_dict[user]
                return render_template("atencion.html", atenciones = atenciones, sorted_dates = sorted(fechas_atenciones,reverse=True), hoy = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), mascotas=mascotas, mensajes=mensajes)
            else:
                if session['type'] == 'user' or session['type'] == 'admin':
                    user_dates_dict = {}
                    for id, pets in atencion_dict.items():
                        for pet, dates in pets.items():
                            for date, column in dates.items():
                                if id not in user_dates_dict:
                                    user_dates_dict[id] = []
                                user_dates_dict[id].append(date)
                            user_dates_dict[id] = sorted(user_dates_dict[id], reverse=True)
                    fechas_atenciones = user_dates_dict
                    atenciones_completas = atencion_dict
                    return render_template("atencion.html", usuarios=user_dict, atenciones_completas=atenciones_completas, sorted_dates=fechas_atenciones,mensajes=mensajes)
        else:
            return redirect("/login")
    else:
        if request.method == 'POST':
            type = session['type']
            if 'select_user' in request.form:
                user = request.form['select_user']
                session['client'] = user
                if not tiene_mascotas(pet_dict,user):
                    mensajes.append('Usuario ' + user + ' no tiene mascotas registradas')
                    mascotas = {}
                else:
                    mascotas = pet_dict[user]
                if user not in atencion_dict:
                    mensajes.append('Usuario ' + user + ' no tiene atenciones')
                    fechas_atenciones = []
                    atenciones = {}
                else:
                    atenciones = atencion_dict[user]
                    #print(atenciones)
                    user_dates_dict = {}
                    for id, pets in atencion_dict.items():
                        for pet, dates in pets.items():
                            for date, column in dates.items():
                                if id not in user_dates_dict:
                                    user_dates_dict[id] = []
                                user_dates_dict[id].append(date)
                    fechas_atenciones = user_dates_dict[user]
                return render_template("atencion.html", atenciones = atenciones, sorted_dates = sorted(fechas_atenciones,reverse=True), hoy = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), mascotas=mascotas, mensajes=mensajes)
            else:
                if 'tipo_solicitud' in request.form.keys():
                    if request.form['tipo_solicitud'] == 'agregar_atencion':
                        user = session['client']
                        #print(request.form)
                        username = session['client']
                        pet_name = request.form['select_pet'].lower().title()
                        description = request.form['description']
                        date = request.form['date_selected']
                        sub_total = request.form['sub_total']
                        iva = request.form['iva']
                        total = request.form['total']
                        if user not in atencion_dict:
                            atencion_dict[user] = {}
                        if pet_name not in atencion_dict[user]:
                            atencion_dict[user][pet_name] = {}
                        atencion_dict[user][pet_name][date] = {
                            'username'      : username,
                            'pet_name'      : pet_name,
                            'description'   : description,
                            'date'          : date,
                            'sub_total'     : sub_total,
                            'iva'           : iva,
                            'total'         : total
                        }
                        atencion.update_atencion_file(atencion_dict,atencion_file)
                        return redirect('/atencion')
                    if request.form['tipo_solicitud'] == 'informe_dia':
                        date_selected = request.form['date_selected']
                        atenciones = [] 
                        for usuario, datos_usuario in atencion_dict.items():
                            for pet, datos_pet in datos_usuario.items():
                                for code, datos in datos_pet.items():
                                    if datos['date'] == date_selected:
                                        atenciones.append(datos)
                        if atenciones == []:
                            mensajes.append('Día sin ventas')
                        if 'pdf_check' in request.form:
                            html = render_template("atencion.html", usuarios=user_dict, atenciones_informe=atenciones, mensajes=mensajes)
                            return render_pdf(HTML(string=html))
                        else:
                            return render_template("atencion.html", usuarios=user_dict, atenciones_informe=atenciones, mensajes=mensajes)

@app.route("/usuarios", methods=['GET','POST'])
def funcion_usuarios():
    mensajes = []
    if request.method == 'GET':
        if 'logged_in' in session:
            if 'client' in session:
                session.pop('client', None)
            type = session['type']
            if type == 'admin':
                return render_template('usuarios.html', usuarios=user_dict, action='mostrar', mensajes=mensajes)
            else:
                return redirect('/')
        else:
            return redirect("/login")
    else:
        if request.method == 'POST':
            if 'select_user' in request.form:
                user = request.form['select_user']
                session['client'] = user
                return render_template("usuarios.html", usuario=user_dict[user], action='modificar', mensajes=mensajes)
            if 'agregar_usuario_boton' in request.form:
                return render_template("usuarios.html", action='agregar', mensajes=mensajes)
            if 'agregar' in request.form:
                global mails
                if 'username' in request.form:
                    username = request.form['username']
                else:
                    username = request.form['username_hidden']
                name = request.form['name']
                email = request.form['email']
                type = request.form['type']
                if username in user_dict:
                    user_dict[username]['name'] = name
                    user_dict[username]['type'] = type
                    user_dict[username]['email'] = email
                    usuarios.update_users_file(user_dict,users_file)
                    mails = usuarios.crear_lista_emails(user_dict)
                    return redirect("/usuarios")
                elif email not in mails:
                    password = request.form['password']
                    password_hashed = sha256.encrypt(password)
                    print(type)
                    user_dict[username] = {
                        'username' : username,
                        'name' : name,
                        'type' : type,
                        'email' : email,
                        'password' : password_hashed,
                        'active' : 'True'
                    }
                    usuarios.update_users_file(user_dict,users_file)
                    mails = usuarios.crear_lista_emails(user_dict)
                    return redirect("/usuarios")
                else:
                    if email in mails:
                        msg = f'Email ya registrado.'
                        mensajes.append(msg)
                    if username in user_dict:
                        msg = f'Usuario ya existe.'
                        mensajes.append(msg)
                    return render_template("usuarios.html", action='agregar', mensajes=mensajes)
            if 'submit_mostrar_eliminados' in request.form:
                return render_template('usuarios.html', usuarios=user_dict, mostrar_eliminados='True', action='mostrar', mensajes=mensajes)
            if 'submit_button_delete' in request.form:
                user = request.form['submit_button_delete']
                user_dict[user]['active'] = 'False'
                usuarios.update_users_file(user_dict,users_file)
                return render_template("usuarios.html", usuarios=user_dict, action='mostrar', mensajes=mensajes)

@app.route("/medicamentos", methods=['GET','POST'])
def funcion_medicamentos():
    mensajes = []
    if request.method == 'GET':
        if 'logged_in' in session:
            if 'client' in session:
                session.pop('client', None)
            type = session['type']
            if type == 'admin':
                return render_template('medicamentos.html', medicamentos=drugs_dict, action='mostrar', mensajes=mensajes)
            else:
                return redirect('/')
        else:
            return redirect("/login")
    else:
        if request.method == 'POST':
            if 'select_drug' in request.form:
                drug = request.form['select_drug']
                session['client'] = drug
                return render_template("medicamentos.html", medicamento=drugs_dict[drug], action='modificar', mensajes=mensajes)
            if 'agregar_medicamento_boton' in request.form:
                return render_template("medicamentos.html", action='agregar', mensajes=mensajes)
            if 'agregar' in request.form:
                if 'code' in request.form:
                    code = request.form['code']
                    tipo = 'agregar'
                else:
                    code = request.form['code_hidden']
                    tipo = 'modificar'
                name = request.form['name']
                description = request.form['description']
                presentation = request.form['presentation']
                quantity = request.form['quantity']
                measure = request.form['measure']
                price = request.form['price']
                if tipo == 'modificar' and code in drugs_dict:
                    drugs_dict[code]['name'] = name
                    drugs_dict[code]['description'] = description
                    drugs_dict[code]['presentation'] = presentation
                    drugs_dict[code]['quantity'] = quantity
                    drugs_dict[code]['measure'] = measure
                    drugs_dict[code]['price'] = price
                    recetas.update_drugs_file(drugs_dict,drugs_file)
                    return redirect("/medicamentos")
                elif tipo == 'agregar' and code not in drugs_dict:
                    drugs_dict[code] = {
                        'code'          : code,
                        'name'          : name,
                        'description'   : description,
                        'presentation'  : presentation,
                        'quantity'      : quantity,
                        'measure'       : measure,
                        'price'         : price,
                        'active'        : 'True'
                    }
                    recetas.update_drugs_file(drugs_dict,drugs_file)
                    return redirect("/medicamentos")
                else:
                    if code in drugs_dict:
                        msg = f'Medicamento con ese código ya existe.'
                        mensajes.append(msg)
                    return render_template("medicamentos.html", action='agregar', mensajes=mensajes)
            if 'submit_mostrar_eliminados' in request.form:
                return render_template('medicamentos.html', medicamentos=drugs_dict, mostrar_eliminados='True', action='mostrar', mensajes=mensajes)
            if 'submit_button_delete' in request.form:
                drug = request.form['submit_button_delete']
                drugs_dict[drug]['active'] = 'False'
                recetas.update_drugs_file(drugs_dict,drugs_file)
                return render_template("medicamentos.html", medicamentos=drugs_dict, action='mostrar', mensajes=mensajes)


if __name__ == "__main__":
    app.run(debug=True)
    