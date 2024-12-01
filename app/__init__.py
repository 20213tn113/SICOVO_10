from operator import imatmul

from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail
from werkzeug.utils import secure_filename
import os

from .models.ModeloCompra import ModeloCompra
from .models.ModeloLibro import ModeloLibro
from .models.ModeloUsuario import ModeloUsuario

from .models.entities.Compra import Compra
from .models.entities.Libro import Libro
from .models.entities.Usuario import Usuario

from .consts import *
from .emails import confirmacion_compra, confirmacion_compraU, confirmacion_registro

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)
mail = Mail()
app.config['UPLOAD_FOLDER'] = 'app/static/img/portadas'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


@login_manager_app.user_loader
def load_user(id):
    return ModeloUsuario.obtener_por_id(db, id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = Usuario(
            None, request.form['usuario'], request.form['password'], None, None, None, None, None)
        usuario_logeado = ModeloUsuario.login(db, usuario)
        if usuario_logeado != None:
            login_user(usuario_logeado)
            flash(MENSAJE_BIENVENIDA, 'success')
            return redirect(url_for('index'))
        else:
            flash(LOGIN_CREDENCIALESINVALIDAS, 'warning')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash(LOGOUT, 'success')
    return redirect(url_for('login'))


@app.route('/bienvenida')
def bienvenida():
    return render_template('auth/bienvenida.html')


@app.route('/registroExitoso')
def registroExitoso():
    flash(MENSAJE_REGISTRADO, 'success')
    return redirect(url_for('login'))


@app.route('/registroUsuario')
def registroUsuario():
    return render_template('auth/registro_usuario.html')


@app.route('/redicaddbook')
def redicaddbook():
    return render_template('auth/addbook.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    print("Llega a la funcion")
    data = {}




    try:
        print("0")
    except Exception as ex:
        data['mensaje'] = format(ex)
        data['exito'] = False
    return jsonify(data)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    data = {}
    try:
        isbn = request.form.get('isbn')
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        fecha_edi = request.form.get('fecha_edi')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        # print(isbn)
        # print(titulo)
        # print(autor)
        # print(fecha_edi)
        # print(descripcion)
        # print(precio)

        imagen = request.files.get('imagen')
        print(imagen)

        if imagen and allowed_file(imagen.filename):
            print("Parte 2")
            filename = secure_filename(imagen.filename)
            print(filename)

            print("1")
            # imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print("2")
            # imagen.save(imagen_path)
            print("3")
            insert = ModeloLibro.insert_libro(db,isbn,titulo, autor,fecha_edi, precio, descripcion, filename)
            print("4")
            insert = True
            print("5")
            data['exito'] = insert

            flash('Libro añadido exitosamente!', 'success')
            print("5")
            return jsonify(data)

            # return redirect(url_for('login'))
        else:
            print("Formato no valido")
            flash('Formato de imagen no permitido', 'danger')
            data['mensaje'] = "Formato no valido"
            data['exito'] = False
    except Exception as ex:
        data['mensaje'] = format(ex)
        data['exito'] = False
    return jsonify(data)


@app.route('/redic')
def redic():
    return render_template('auth/addbook.html')


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    data_request = request.get_json()
    data = {}
    try:
        nombre = data_request['nombre']
        apellido = data_request['apellido']
        nombre_completo = nombre + ' ' + apellido
        usuario = Usuario(
            None, data_request['usuario'], data_request['password'], nombre_completo, data_request['domicilio'],
            data_request['correo'], data_request['telefono'], 2)
        usuario_creado = ModeloUsuario.registrar_usuario(db, usuario)
        data['exito'] = usuario_creado
        libro = None
        confirmacion_registro(app, mail, usuario.usuario, libro, usuario.correo)
    except Exception as ex:
        data['mensaje'] = format(ex)
        data['exito'] = False
    return jsonify(data)


@app.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.tipousuario.id == 1:
            try:

                libros_vendidos = ModeloLibro.listar_libros_vendidos(db)
                data = {
                    'titulo': 'Libros Vendidos',
                    'libros_vendidos': libros_vendidos
                }
                return render_template('index.html', data=data)
            except Exception as ex:
                return render_template('errores/error.html', mensaje=format(ex))
        else:
            try:
                compras = ModeloCompra.listar_compras_usuario(db, current_user)
                data = {
                    'titulo': 'Mis compras',
                    'compras': compras
                }
                return render_template('index.html', data=data)
            except Exception as ex:
                return render_template('errores/error.html', mensaje=format(ex))
    else:
        return redirect(url_for('login'))


@app.route('/libros')
@login_required
def listar_libros():
    try:
        libros = ModeloLibro.listar_libros(db)
        data = {
            'titulo': 'Listado de libros',
            'libros': libros
        }
        return render_template('listado_libros.html', data=data)
    except Exception as ex:
        return render_template('errores/error.html', mensaje=format(ex))


@app.route('/biblioteca')
def biblioteca():
    try:
        libros = ModeloLibro.obtener_libros(db)
        for libro in libros:
            print(libro.titulo)
        return render_template('auth/biblioteca.html', libros=libros)
    except Exception as ex:
        return render_template('errores/error.html', mensaje=format(ex))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/comprarLibro', methods=['POST'])
@login_required
def comprar_libro():
    data_request = request.get_json()

    data = {}
    try:
        #libro = Libro(data_request['isbn'], None, None, None, None)
        libro = ModeloLibro.leer_libro(db, data_request['isbn'])
        compra = Compra(None, libro, current_user)
        data['exito'] = ModeloCompra.registrar_compra(db, compra)
        correo = ModeloUsuario.obtener_gmail(db, current_user.id)

        # confirmacion_compra(mail, current_user, libro) #ENVIO NORMAL
        #confirmacion_compra(app, mail, current_user, libro) #ENVIO ASINCRONO
        confirmacion_compraU(app, mail, current_user, libro, correo)

    except Exception as ex:
        data['mensaje'] = format(ex)
        data['exito'] = False
    return jsonify(data)


def pagina_no_encontrada(error):
    return render_template('errores/404.html'), 404


def pagina_no_autorizada(error):
    return redirect(url_for('login'))


def inicializar_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    mail.init_app(app)
    app.register_error_handler(401, pagina_no_autorizada)
    app.register_error_handler(404, pagina_no_encontrada)
    return app
