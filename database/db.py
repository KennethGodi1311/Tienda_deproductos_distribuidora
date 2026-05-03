import sqlite3
from datetime import datetime

# =========================
# CONEXIÓN
# =========================
def conectar():
    return sqlite3.connect("tienda.db", check_same_thread=False)


# =========================
# INIT DB
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

    # 🔥 FACTURAS (NUEVO)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT,
        fecha TEXT,
        total REAL,
        metodo_pago TEXT
    )
    """)

    conexion.commit()
    conexion.close()


# =========================
# PRODUCTOS
# =========================
def obtener_productos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT nombre, precio, stock FROM productos")
    data = cursor.fetchall()

    conn.close()
    return data


def agregar_producto(nombre, precio, stock):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO productos(nombre, precio, stock) VALUES (?, ?, ?)",
            (nombre, precio, stock)
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def actualizar_producto(nombre, precio, stock):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE productos SET precio=?, stock=? WHERE nombre=?",
        (precio, stock, nombre)
    )

    conn.commit()
    conn.close()


def eliminar_producto(nombre):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM productos WHERE nombre=?", (nombre,))

    conn.commit()
    conn.close()


# =========================
# VENTAS
# =========================
def guardar_venta(carrito):
    conn = conectar()
    cursor = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for item in carrito:

        # 🔥 VALIDAR STOCK
        cursor.execute(
            "SELECT stock FROM productos WHERE nombre=?",
            (item["producto"],)
        )
        resultado = cursor.fetchone()

        if resultado:
            stock_actual = resultado[0]

            if stock_actual < item["cantidad"]:
                raise Exception(f"Stock insuficiente para {item['producto']}")

            # 🔥 DESCONTAR STOCK
            cursor.execute(
                "UPDATE productos SET stock = stock - ? WHERE nombre=?",
                (item["cantidad"], item["producto"])
            )

        # GUARDAR VENTA
        cursor.execute("""
            INSERT INTO ventas(producto, cantidad, total, fecha)
            VALUES (?, ?, ?, ?)
        """, (
            item["producto"],
            item["cantidad"],
            item["precio"] * item["cantidad"],
            fecha
        ))

    conn.commit()
    conn.close()


# =========================
# FACTURAS
# =========================
def guardar_factura(numero, total, metodo_pago):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO facturas(numero, fecha, total, metodo_pago)
        VALUES (?, ?, ?, ?)
    """, (
        numero,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total,
        metodo_pago
    ))

    conn.commit()
    conn.close()


# =========================
# DASHBOARD
# =========================
def obtener_ventas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ventas")
    data = cursor.fetchall()

    conn.close()
    return data


def ventas_por_producto():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT producto, SUM(total)
        FROM ventas
        GROUP BY producto
    """)

    data = cursor.fetchall()
    conn.close()

    return data