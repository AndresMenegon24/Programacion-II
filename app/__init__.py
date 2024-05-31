from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esto por una clave secreta segura

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'                                                  
app.config['MYSQL_PASSWORD'] = ''  
app.config['MYSQL_DB'] = 'pizzeria'

mysql = MySQL(app)

from app import routes
