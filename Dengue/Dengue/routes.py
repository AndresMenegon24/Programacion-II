# routes.py
from flask import render_template, request, redirect, url_for, flash, session
from models import db, Caso
from forms import CasoForm, LoginForm

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register_case():
        form = CasoForm()
        if form.validate_on_submit():
            fecha_nacimiento = form.fecha_nacimiento.data
            edad = Caso.calcular_edad(fecha_nacimiento)
            nuevo_caso = Caso(
                dni=form.dni.data,
                nombre=form.nombre.data,
                apellido=form.apellido.data,
                fecha_nacimiento=fecha_nacimiento,
                edad=edad,
                sexo=form.sexo.data,
                calle=form.calle.data,
                numero=form.numero.data,
                barrio=form.barrio.data,
                localidad=form.localidad.data,
                departamento=form.departamento.data,
                codigo_postal=form.codigo_postal.data,
                telefono=form.telefono.data,
                correo=form.correo.data,
                grupo=form.grupo.data,
                ingresa_con_vida=form.ingresa_con_vida.data
            )
            try:
                db.session.add(nuevo_caso)
                db.session.commit()
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                print(f"Error: {e}")
                return render_template('registro_casos.html', form=form, error=str(e))
        return render_template('registro_casos.html', form=form)

    @app.route('/casos')
    def view_cases():
        casos = Caso.query.all()
        casos_dict = [caso.to_dict() for caso in casos]
        return render_template('ver_casos.html', casos=casos_dict)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            if form.username.data == 'admin' and form.password.data == '1234':
                session['logged_in'] = True
                return redirect(url_for('index'))
            else:
                flash('Nombre de usuario o contraseña incorrectos', 'danger')
        return render_template('login.html', form=form)

    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        return redirect(url_for('login'))

    @app.before_request
    def require_login():
        allowed_routes = ['login', 'static']
        if request.endpoint not in allowed_routes and 'logged_in' not in session:
            return redirect(url_for('login'))
