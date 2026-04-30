import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import bcrypt
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(
    page_title="Pulpería El Dragón Dorado",
    layout="wide"
)

# -------------------------
# ESTILOS
# -------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #020617, #0f172a);
    color: #e2e8f0;
    font-family: 'Segoe UI', sans-serif;
}

section[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid #1e293b;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #3b82f6, #2563eb);
    color: white;
    border-radius: 12px;
    height: 44px;
    border: none;
    font-weight: 600;
}

.card {
    background: #1e293b;
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #334155;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# DB
# -------------------------
def conectar():
    return sqlite3.connect("tienda.db")

def init_db():
    conn = conectar()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password BLOB,
        rol TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS productos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        precio REAL,
        stock INTEGER
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS ventas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT,
        cantidad INTEGER,
        total REAL,
        fecha TEXT
    )""")

    conn.commit()
    conn.close()

init_db()

# -------------------------
# SESSION STATE
# -------------------------
if "login" not in st.session_state:
    st.session_state.login = False

if "user" not in st.session_state:
    st.session_state.user = None

if "rol" not in st.session_state:
    st.session_state.rol = None

if "auth_view" not in st.session_state:
    st.session_state.auth_view = "login"

if "carrito" not in st.session_state:
    st.session_state.carrito = []

if "categoria" not in st.session_state:
    st.session_state.categoria = "Todos"

# -------------------------
# FACTURA
# -------------------------
def generar_factura(producto, precio):
    doc = SimpleDocTemplate("factura.pdf")
    styles = getSampleStyleSheet()

    contenido = [
        Paragraph("Pulpería El Dragón Dorado", styles["Title"]),
        Paragraph(f"Producto: {producto}", styles["Normal"]),
        Paragraph(f"Precio: ₡{precio}", styles["Normal"]),
        Paragraph(f"Fecha: {datetime.now()}", styles["Normal"])
    ]

    doc.build(contenido)

# -------------------------
# PÁGINAS
# -------------------------
def inicio():
    st.title("🐉 Pulpería El Dragón Dorado")

    productos = [
        {"nombre": "Arroz", "precio": 1500, "cat": "Abarrotes"},
        {"nombre": "Leche", "precio": 900, "cat": "Lacteos"},
        {"nombre": "Pan", "precio": 800, "cat": "Panaderia"},
        {"nombre": "Huevos", "precio": 2500, "cat": "Basicos"},
    ]

    st.subheader("🛒 Productos")

    cols = st.columns(3)
    i = 0

    for p in productos:
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card">
                <h4>{p['nombre']}</h4>
                <p>₡{p['precio']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Comprar {p['nombre']}", key=p['nombre']):
                st.session_state.carrito.append(p)
                st.success("Agregado al carrito")

        i += 1


def productos():
    st.title("🛍️ Productos")
    st.write("Vista pública de productos")


def ofertas():
    st.title("🔥 Ofertas")
    st.write("Ofertas disponibles")


def acerca():
    st.title("🏢 Sobre Nosotros")
    st.write("Pulpería El Dragón Dorado - calidad y confianza")


def contacto():
    st.title("📞 Contacto")
    st.write("Tel: 2230-5698")


def dashboard():
    st.title("📊 Dashboard")
    st.write("Panel administrativo")


def compra():
    st.title("🛒 Compra")
    st.write(st.session_state.carrito)


def factura():
    st.title("🧾 Factura")
    st.write("Generación de factura")


def inventario():
    st.title("📦 Inventario")
    st.write("Control de productos")


def ventas():
    st.title("💰 Ventas")
    st.write("Registro de ventas")

# -------------------------
# LOGIN
# -------------------------
def login():
    st.title("🔐 Login")

    user = st.text_input("Usuario")
    pwd = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        conn = conectar()
        c = conn.cursor()

        c.execute("SELECT password, rol FROM usuarios WHERE username=?", (user,))
        data = c.fetchone()
        conn.close()

        if data:
            hashed, rol = data
            if isinstance(hashed, str):
                hashed = hashed.encode()

            if bcrypt.checkpw(pwd.encode(), hashed):
                st.session_state.login = True
                st.session_state.user = user
                st.session_state.rol = rol
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        else:
            st.error("Usuario no existe")

# -------------------------
# REGISTRO
# -------------------------
def registro():
    st.title("📝 Registro")

    user = st.text_input("Usuario")
    pwd = st.text_input("Contraseña", type="password")
    rol = st.selectbox("Rol", ["empleado", "admin"])

    if st.button("Registrar"):
        hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())

        conn = conectar()
        c = conn.cursor()

        try:
            c.execute("INSERT INTO usuarios VALUES(NULL,?,?,?)", (user, hashed, rol))
            conn.commit()
            st.success("Usuario creado")
            st.session_state.auth_view = "login"
            st.rerun()
        except:
            st.error("Usuario ya existe")

        conn.close()

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("🛒 Menú")

if st.sidebar.button("Inicio"):
    inicio()

if st.sidebar.button("Productos"):
    productos()

if st.sidebar.button("Ofertas"):
    ofertas()

if st.sidebar.button("Acerca"):
    acerca()

if st.sidebar.button("Contacto"):
    contacto()

st.sidebar.markdown("---")

if st.sidebar.button("Login"):
    st.session_state.auth_view = "login"
    st.rerun()

if st.sidebar.button("Registro"):
    st.session_state.auth_view = "registro"
    st.rerun()

# -------------------------
# AUTH FLOW
# -------------------------
if not st.session_state.login:

    if st.session_state.auth_view == "registro":
        registro()
    else:
        login()

    st.stop()

# -------------------------
# SIDEBAR LOGEADO
# -------------------------
st.sidebar.title("🛠️ Panel")

if st.sidebar.button("Dashboard"):
    dashboard()

if st.sidebar.button("Compra"):
    compra()

if st.sidebar.button("Factura"):
    factura()

if st.sidebar.button("Inventario"):
    inventario()

if st.sidebar.button("Ventas"):
    ventas()

if st.sidebar.button("Cerrar sesión"):
    st.session_state.login = False
    st.session_state.auth_view = "login"
    st.rerun()