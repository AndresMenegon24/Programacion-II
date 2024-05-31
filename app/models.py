class Producto:
    def __init__(self, id, nombre, precio):
        self.id = id
        self.nombre = nombre
        self.precio = precio

class Pedido:
    def __init__(self, id, productos, nombre_cliente, telefono, direccion, fecha_hora, horario_retiro, total):
        self.id = id
        self.productos = productos  # productos es una lista de tuplas (Producto, cantidad)
        self.nombre_cliente = nombre_cliente
        self.telefono = telefono
        self.direccion = direccion
        self.fecha_hora = fecha_hora
        self.horario_retiro = horario_retiro
        self.total = total
