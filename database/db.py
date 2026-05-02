import sqlite3

# =========================
# CONEXIÓN
# =========================
def conectar():
    return sqlite3.connect("tienda.db", check_same_thread=False)


# =========================
# INICIALIZAR BD
# =========================
def init_db():
    conexion = conectar()
    cursor = conexion.cursor()

    # USUARIOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password BLOB,
        rol TEXT
    )
    """)

    # PRODUCTOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE,
        precio REAL,
        stock INTEGER
    )
    """)

    # VENTAS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT,
        cantidad INTEGER,
        total REAL,
        fecha TEXT
    )
    """)

    conexion.commit()
    conexion.close()


# =========================
# PRODUCTOS (CRUD)
# =========================
def obtener_productos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT nombre, precio, stock FROM productos")
    data = cursor.fetchall()

    conexion.close()

    return data


def agregar_producto(nombre, precio, stock):
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "INSERT INTO productos(nombre, precio, stock) VALUES (?, ?, ?)",
            (nombre, precio, stock)
        )
        conexion.commit()
        return True
    except:
        return False
    finally:
        conexion.close()


def actualizar_producto(nombre, precio, stock):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "UPDATE productos SET precio=?, stock=? WHERE nombre=?",
        (precio, stock, nombre)
    )

    conexion.commit()
    conexion.close()


def eliminar_producto(nombre):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM productos WHERE nombre=?", (nombre,))

    conexion.commit()
    conexion.close()


# =========================
# VENTAS
# =========================
def guardar_venta(carrito):
    conexion = conectar()
    cursor = conexion.cursor()

    for item in carrito:
        cursor.execute("""
            INSERT INTO ventas(producto, cantidad, total, fecha)
            VALUES (?, ?, ?, datetime('now'))
        """, (
            item["producto"],
            item["cantidad"],
            item["precio"] * item["cantidad"]
        ))

    conexion.commit()
    conexion.close()


# =========================
# DASHBOARD
# =========================
def obtener_ventas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM ventas")
    data = cursor.fetchall()

    conexion.close()

    return data


def ventas_por_producto():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT producto, SUM(total) 
        FROM ventas 
        GROUP BY producto
    """)

    data = cursor.fetchall()
    conexion.close()

    return data