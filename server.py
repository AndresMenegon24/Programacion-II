from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# Configuración de MySQL usando las variables del archivo .env
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.secret_key = 'tu_clave_secreta_aqui'  # Necesaria para usar `flash`

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO users (email, password)
                  VALUES (%s, %s)''', (email, password))
        mysql.connection.commit()
        cursor.close()
        return render_template('inicio.html', mensaje="Registro exitoso")
    return render_template('inicio.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        mysql.connection.commit()
        cursor.close()
        flash("Registro exitoso. Por favor, inicia sesión.")
        return redirect(url_for('inicio'))
    return render_template('registro.html')



@app.route('/seleccion')
def seleccion():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM equipos")  # Asegúrate de que el nombre de la tabla sea correcto
    data = cur.fetchall()
    cur.close()
    return render_template('seleccion.html', equipos=data)



@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return redirect(url_for('futbol'))
        else:
            flash("Correo o contraseña incorrectos. Inténtalo de nuevo.")
            return redirect(url_for('inicio'))

@app.route('/futbol')
def futbol():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/noticia1')
def noticia1():
    return render_template('noticia1.html')

@app.route('/noticia2')
def noticia2():
    return render_template('noticia2.html')

@app.route('/noticia3')
def noticia3():
    return render_template('noticia3.html')

@app.route('/noticia4')
def noticia4():
    return render_template('noticia4.html')

@app.route('/noticia5')
def noticia5():
    return render_template('noticia5.html')

@app.route('/resultado')
def resultado():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jugadores")  # Asegúrate de que el nombre de la tabla sea correcto
    jugador = cur.fetchall()
    cur.close()
    return render_template('resultados.html', jugadores = jugador)

@app.route('/jugadores/<int:seleccion_id>')
def mostrar_jugadores(seleccion_id):
    # Consulta SQL para obtener jugadores de la selección específica
    query = "SELECT * FROM jugadores WHERE seleccion_id = %s"
    
    cur = mysql.connection.cursor()
    cur.execute(query, (seleccion_id,))
    jugadores = cur.fetchall()
    cur.close()

@app.route('/estadistica')
def estadistica():
    cur = mysql.connection.cursor()
    query = """
    SELECT 
        p.fecha,
        s1.nombre_seleccion AS seleccion1,
        s2.nombre_seleccion AS seleccion2,
        p.goles_seleccion1,
        p.goles_seleccion2,
        p.asistencia
    FROM partidos p
    JOIN selecciones s1 ON p.seleccion1_id = s1.seleccion_id
    JOIN selecciones s2 ON p.seleccion2_id = s2.seleccion_id
    ORDER BY p.fecha ASC
    """
    cur.execute(query)
    stats = cur.fetchall()
    cur.close()

    return render_template('estadistica.html', stats=stats)



@app.route('/torneo')
def torneo():
    cur = mysql.connection.cursor()

    # Gráfico 1: Obtener datos para el gráfico por Selección
    query1 = """
    SELECT s.nombre_seleccion, 
           SUM(p.goles_seleccion1 + p.goles_seleccion2) AS goles_totales
    FROM selecciones s
    JOIN partidos p ON (p.seleccion1_id = s.seleccion_id OR p.seleccion2_id = s.seleccion_id)
    GROUP BY s.nombre_seleccion
    """
    cur.execute(query1)
    resultados1 = cur.fetchall()
    
    labels1 = [row[0] for row in resultados1]
    values1 = [row[1] for row in resultados1]

    # Gráfico 2: Obtener datos para el gráfico por fecha
    query2 = """
    SELECT p.fecha, 
           COUNT(*) AS total_partidos
    FROM partidos p
    GROUP BY p.fecha
    ORDER BY p.fecha ASC
    """
    cur.execute(query2)
    resultados2 = cur.fetchall()
    
    labels2 = [row[0].strftime('%Y-%m-%d') for row in resultados2]
    values2 = [row[1] for row in resultados2]

    cur.close()

    return render_template('torneos.html', labels1=labels1, values1=values1, labels2=labels2, values2=values2)
if __name__ == '__main__':
    app.run(port=5000, debug=True)