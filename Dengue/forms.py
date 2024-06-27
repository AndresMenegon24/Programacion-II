from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError
from datetime import date

class CasoForm(FlaskForm):
    dni = StringField('DNI', validators=[DataRequired(), Length(min=7, max=20)])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d', validators=[DataRequired()])
    edad = IntegerField('Edad', render_kw={'readonly': True})
    sexo = SelectField('Sexo', choices=[('M', 'Masculino'), ('F', 'Femenino')], validators=[DataRequired()])
    calle = StringField('Calle', validators=[DataRequired(), Length(max=100)])
    numero = IntegerField('Número', validators=[DataRequired(), NumberRange(min=1)])
    barrio = StringField('Barrio', validators=[DataRequired(), Length(max=100)])
    localidad = StringField('Localidad', validators=[DataRequired(), Length(max=100)])
    departamento = StringField('Departamento', validators=[DataRequired(), Length(max=100)])
    codigo_postal = StringField('Código Postal', validators=[DataRequired(), Length(max=10)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(max=20)])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=100)])
    grupo = SelectField('Grupo', choices=[
        ('A', 'Grupo A: Dengue sin signos de alarma ni comorbilidades'),
        ('B', 'Grupo B: Dengue sin signos de alarma con comorbilidades o riesgo social'),
        ('C', 'Grupo C: Dengue con signos de alarma')
    ], validators=[DataRequired()])
    ingresa_con_vida = BooleanField('Ingresa con Vida')
    submit = SubmitField('Registrar')

    def validate_fecha_nacimiento(form, field):
        if field.data >= date.today():
            raise ValidationError("La fecha de nacimiento no puede ser en el futuro.")
