from flask import render_template, request, redirect, url_for, flash, session
from app import app, mysql
from app.models import Producto, Pedido
import MySQLdb
from datetime import datetime, timedelta

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT * FROM productos")
        productos_data = cursor.fetchall()
        productos = [Producto(id=row[0], nombre=row[1], precio=row[2]) for row in productos_data]

        pedidos = session.pop('detalle_pedido', None)
        mensaje_exito = session.pop('mensaje_exito', None)
    except MySQLdb.ProgrammingError as e:
        productos = []
        pedidos = []
        mensaje_exito = None
        print(f"Error: {e}")
    cursor.close()

    return render_template('index.html', productos=productos, pedidos=pedidos, mensaje_exito=mensaje_exito)

@app.route('/agregar_pedido', methods=['POST'])
def agregar_pedido():
    nombre_cliente = request.form['nombre_cliente']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    fecha_hora = datetime.now()  # Guardar el momento exacto del pedido
    horario_retiro = request.form['horario_retiro'] if request.form['horario_retiro'] else None
    productos_seleccionados = request.form.getlist('productos')
    cantidades = request.form.getlist('cantidades')

    # Validación del lado del servidor
    if not productos_seleccionados or not nombre_cliente or not telefono or not direccion:
        flash('Todos los campos son obligatorios y debe seleccionar al menos un producto.')
        return redirect(url_for('index'))

    # Validar que el horario de retiro sea al menos 30 minutos después del momento actual
    if horario_retiro:
        horario_retiro_dt = datetime.combine(fecha_hora.date(), datetime.strptime(horario_retiro, '%H:%M').time())
        if horario_retiro_dt < fecha_hora + timedelta(minutes=30):
            flash('El pedido tiene una demora de al menos 30 minutos desde el momento en que se hace el pedido.')
            return redirect(url_for('index'))

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO pedidos (nombre_cliente, telefono, direccion, fecha_hora, horario_retiro) VALUES (%s, %s, %s, %s, %s)", (nombre_cliente, telefono, direccion, fecha_hora, horario_retiro))
    pedido_id = cursor.lastrowid

    detalles = []
    for producto_id, cantidad in zip(productos_seleccionados, cantidades):
        cursor.execute("INSERT INTO pedido_productos (pedido_id, producto_id, cantidad) VALUES (%s, %s, %s)", (pedido_id, producto_id, cantidad))
        cursor.execute("SELECT nombre, precio FROM productos WHERE id = %s", (producto_id,))
        producto_data = cursor.fetchone()
        detalles.append((producto_data[0], producto_data[1], cantidad))

    total = sum(precio * int(cantidad) for _, precio, cantidad in detalles)

    pedido_detalle = {
        'id': pedido_id,
        'nombre_cliente': nombre_cliente,
        'telefono': telefono,
        'direccion': direccion,
        'fecha_hora': fecha_hora,
        'horario_retiro': horario_retiro,
        'detalles': detalles,
        'total': total
    }

    session['detalle_pedido'] = pedido_detalle
    session['mensaje_exito'] = 'Su pedido se procesó correctamente'

    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/eliminar_pedido/<int:pedido_id>', methods=['POST'])
def eliminar_pedido(pedido_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM pedido_productos WHERE pedido_id = %s", (pedido_id,))
    cursor.execute("DELETE FROM pedidos WHERE id = %s", (pedido_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'pizzeria' and password == 'pizzeria':
            session['logged_in'] = True
            return redirect(url_for('pedidos'))
        else:
            flash('Usuario o contraseña incorrectos.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/pedidos')
def pedidos():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT id, nombre_cliente, telefono, direccion, fecha_hora, horario_retiro FROM pedidos ORDER BY horario_retiro DESC")
        pedidos_data = cursor.fetchall()
        pedidos = []
        for row in pedidos_data:
            pedido_id = row[0]
            cursor.execute("""
                SELECT productos.nombre, productos.precio, pedido_productos.cantidad 
                FROM pedido_productos 
                JOIN productos ON pedido_productos.producto_id = productos.id 
                WHERE pedido_productos.pedido_id = %s
            """, (pedido_id,))
            productos_pedido = cursor.fetchall()
            productos_obj = [(Producto(id=None, nombre=p[0], precio=p[1]), p[2]) for p in productos_pedido]
            total = sum(p[1] * p[2] for p in productos_pedido)
            pedidos.append(Pedido(id=pedido_id, productos=productos_obj, nombre_cliente=row[1], telefono=row[2], direccion=row[3], fecha_hora=row[4], horario_retiro=row[5], total=total))
    except MySQLdb.ProgrammingError as e:
        pedidos = []
        print(f"Error: {e}")
    cursor.close()

    return render_template('pedidos.html', pedidos=pedidos)


@app.route('/borrar_pedidos', methods=['GET', 'POST'])
def borrar_pedidos():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute("TRUNCATE TABLE pedidos")
        mysql.connection.commit()
        cursor.close()
        flash('Todos los pedidos han sido eliminados.')
        return redirect(url_for('index'))
    return render_template('borrar_pedidos.html')

