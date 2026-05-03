import sqlite3
from datetime import datetime

# =========================
# CONEXIÓN
# =========================
def conectar():
    return sqlite3.connect("tienda.db", check_same_thread=False)

# =========================
# MIGRACIONES (🔥 CLAVE)
# =========================
def agregar_columna_si_no_existe(cursor, tabla, columna_def):
    try:
        cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna_def}")
    except:
        pass


# =========================
# INIT DB
# =========================
def init_db():
    conexion = conectar()
    cursor = conexion.cursor()

    # =========================
    # USUARIOS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password BLOB,
        rol TEXT,
        fecha_creacion TEXT,
        activo INTEGER DEFAULT 1
    )
    """)

    # 🔥 PERFIL COMPLETO
    agregar_columna_si_no_existe(cursor, "usuarios", "foto TEXT")
    agregar_columna_si_no_existe(cursor, "usuarios", "nombre TEXT")
    agregar_columna_si_no_existe(cursor, "usuarios", "correo TEXT")
    agregar_columna_si_no_existe(cursor, "usuarios", "telefono TEXT")
    agregar_columna_si_no_existe(cursor, "usuarios", "direccion TEXT")
    agregar_columna_si_no_existe(cursor, "usuarios", "edad INTEGER")


    # =========================
    # PRODUCTOS (MEJORADO 🔥)
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE,
        nombre TEXT UNIQUE,
        categoria TEXT,
        precio REAL,
        stock INTEGER,
        imagen TEXT, -- 🔥 ruta o URL de imagen
        fecha_creacion TEXT,
        activo INTEGER DEFAULT 1
    )
    """)
    

    # =========================
    # VENTAS
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT,
        cantidad INTEGER,
        total REAL,
        fecha TEXT
    )
    """)

    # =========================
    # FACTURAS (LEGAL 🔥)
    # =========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT,
        fecha TEXT,
        total REAL,
        metodo_pago TEXT,
        estado TEXT DEFAULT 'emitida'
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

    cursor.execute("""
        SELECT nombre, precio, stock, imagen, categoria
        FROM productos
        WHERE activo = 1
    """)

    data = cursor.fetchall()
    conn.close()
    return data


def agregar_producto(nombre, precio, stock, categoria, imagen=None):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO productos(codigo, nombre, categoria, precio, stock, imagen, fecha_creacion)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            f"PROD-{int(datetime.now().timestamp())}",
            nombre,
            categoria,
            precio,
            stock,
            imagen,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def actualizar_producto(nombre, precio, stock, categoria, imagen=None):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE productos 
        SET precio=?, stock=?, categoria=?, imagen=?
        WHERE nombre=?
    """, (precio, stock, categoria, imagen, nombre))

    conn.commit()
    conn.close()


def eliminar_producto(nombre):
    conn = conectar()
    cursor = conn.cursor()

    # 🔥 Soft delete (legalmente mejor)
    cursor.execute("""
        UPDATE productos SET activo = 0 WHERE nombre=?
    """, (nombre,))

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

        cursor.execute(
            "SELECT stock FROM productos WHERE nombre=? AND activo=1",
            (item["producto"],)
        )
        resultado = cursor.fetchone()

        if resultado:
            stock_actual = resultado[0]

            if stock_actual < item["cantidad"]:
                raise Exception(f"Stock insuficiente para {item['producto']}")

            cursor.execute(
                "UPDATE productos SET stock = stock - ? WHERE nombre=?",
                (item["cantidad"], item["producto"])
            )

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