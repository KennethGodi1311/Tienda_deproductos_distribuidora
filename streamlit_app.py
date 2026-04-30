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


# 🔥 FIX GLOBAL
st.markdown("""
<style>
iframe {
    pointer-events: none;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# ESTILOS PROFESIONALES (FIX REAL)
# -------------------------
st.markdown("""
<style>

/* Fondo general */
.stApp {
    background: linear-gradient(180deg, #020617, #0f172a);
    color: #e2e8f0;
    font-family: 'Segoe UI', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid #1e293b;
}

/* Título sidebar */
.sidebar-title {
    color: #3b82f6;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 10px;
}

/* Botones (FIX IMPORTANTE) */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #3b82f6, #2563eb);
    color: white;
    border-radius: 12px;
    height: 44px;
    border: none;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
}

/* Inputs */
.stTextInput input, 
.stTextArea textarea, 
.stSelectbox div {
    border-radius: 8px !important;
}

/* Cards */
.card {
    background: #1e293b;
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #334155;
    margin-bottom: 15px;
}

/* Títulos */
h1, h2, h3 {
    color: #3b82f6 !important;
    font-weight: 600;
}

/* Texto */
p {
    color: #cbd5f5;
}

/* Separadores */
hr {
    border: 0.5px solid #334155;
}

/* ⚠️ IMPORTANTE: quitar esto si no usas mapas */
/* iframe { pointer-events: none; } */

/* 🔥 FIX REAL DE STREAMLIT */
.block-container {
    padding-top: 2rem;
}

/* 🔥 FIX EXTRA (evita errores tipo removeChild) */
[data-testid="stMarkdownContainer"] {
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)


# -------------------------
# DB
# -------------------------
def conectar():
    return sqlite3.connect("tienda.db")

conexion = conectar()
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password BLOB,
    rol TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    precio REAL,
    stock INTEGER
)
""")

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

# -------------------------
# FACTURA PDF
# -------------------------
def generar_factura(producto, precio):
    doc = SimpleDocTemplate("factura.pdf")
    styles = getSampleStyleSheet()

    contenido = []
    contenido.append(Paragraph("Pulpería El Dragón Dorado", styles["Title"]))
    contenido.append(Paragraph(f"Producto: {producto}", styles["Normal"]))
    contenido.append(Paragraph(f"Precio: ₡{precio}", styles["Normal"]))
    contenido.append(Paragraph(f"Fecha: {datetime.now()}", styles["Normal"]))

    doc.build(contenido)

# -------------------------
# PRODUCTOS DEMO (más simples)
# -------------------------
productos_demo = [
    ("Arroz", 1500),
    ("Frijoles", 1200),
    ("Leche", 900),
    ("Pan", 800),
    ("Huevos", 2500),
]

# -------------------------
# PAGINAS
# -------------------------
if "carrito" not in st.session_state:
    st.session_state["carrito"] = []

def inicio():
    st.title("🐉 Pulpería El Dragón Dorado")
    st.caption("Ofertas todos los días 🛒 | Rápido, cerca y confiable")

    st.divider()

    # -------------------------
    # ESTADO
    # -------------------------
    if "categoria" not in st.session_state:
        st.session_state["categoria"] = "Todos"

    # -------------------------
    # BOTONES CATEGORÍA (MEJORADOS)
    # -------------------------
    st.subheader("🧭 Categorías")

    col1, col2, col3, col4, col5 = st.columns(5)

    if col1.button("🥫 Abarrotes"):
        st.session_state["categoria"] = "Abarrotes"

    if col2.button("🥛 Lácteos"):
        st.session_state["categoria"] = "Lacteos"

    if col3.button("🥖 Panadería"):
        st.session_state["categoria"] = "Panaderia"

    if col4.button("🍳 Básicos"):
        st.session_state["categoria"] = "Basicos"

    if col5.button("🔄 Todos"):
        st.session_state["categoria"] = "Todos"

    st.info(f"Mostrando: {st.session_state['categoria']}")

    st.divider()

    # -------------------------
    # PRODUCTOS EXPANDIDOS
    # -------------------------
    productos = [
        # Abarrotes
        {"nombre": "Arroz", "precio": 1500, "cat": "Abarrotes"},
        {"nombre": "Frijoles", "precio": 1200, "cat": "Abarrotes"},
        {"nombre": "Azúcar", "precio": 900, "cat": "Abarrotes"},
        {"nombre": "Sal", "precio": 500, "cat": "Abarrotes"},

        # Lácteos
        {"nombre": "Leche", "precio": 900, "cat": "Lacteos"},
        {"nombre": "Queso", "precio": 1800, "cat": "Lacteos"},
        {"nombre": "Yogurt", "precio": 700, "cat": "Lacteos"},
        {"nombre": "Mantequilla", "precio": 1200, "cat": "Lacteos"},

        # Panadería
        {"nombre": "Pan", "precio": 800, "cat": "Panaderia"},
        {"nombre": "Queque", "precio": 1500, "cat": "Panaderia"},
        {"nombre": "Galletas", "precio": 600, "cat": "Panaderia"},
        {"nombre": "Empanadas", "precio": 1000, "cat": "Panaderia"},

        # Básicos
        {"nombre": "Huevos", "precio": 2500, "cat": "Basicos"},
        {"nombre": "Aceite", "precio": 2200, "cat": "Basicos"},
        {"nombre": "Café", "precio": 3000, "cat": "Basicos"},
        {"nombre": "Atún", "precio": 1300, "cat": "Basicos"},
    ]

    st.subheader("🛒 Productos")

    cols = st.columns(3)

    index = 0
    for p in productos:

        if st.session_state["categoria"] != "Todos" and p["cat"] != st.session_state["categoria"]:
            continue

        with cols[index % 3]:
            st.markdown(f"""
            <div class="card">
                <h4>{p["nombre"]}</h4>
                <p>💰 ₡{p["precio"]}</p>
                <small>{p["cat"]}</small>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Comprar", key=p["nombre"]):
                st.success(f"{p['nombre']} agregado ✔️")

        index += 1

    # -------------------------
    # OFERTAS
    # -------------------------
    st.divider()
    st.subheader("🔥 Ofertas del día")

    col1, col2 = st.columns(2)

    col1.success("🍚 Arroz ₡1200")
    col2.warning("🥖 Pan ₡600")

    # -------------------------
    # INFO
    # -------------------------
    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.info("📍 Barrio Chino, San José")
    col2.info("☎ 2230-5698")
    col3.info("🕒 7:00 AM - 9:00 PM")

def productos():

    st.title("🛍️ Productos (sin login)")

    lista = [
        {"nombre": "Arroz", "precio": 1000},
        {"nombre": "Frijoles", "precio": 1200},
        {"nombre": "Azúcar", "precio": 900},
    ]

    for p in lista:

        st.write(f"{p['nombre']} - ₡{p['precio']}")

        if st.button(f"Agregar {p['nombre']}"):
            st.session_state["carrito"].append({
                "producto": p["nombre"],
                "precio": p["precio"],
                "cantidad": 1
            })

def ofertas():

    st.title("🔥 Ofertas")

    lista = [
        {"nombre": "Leche", "precio": 800, "desc": 10},
        {"nombre": "Pan", "precio": 500, "desc": 20},
    ]

    for o in lista:

        final = o["precio"] - (o["precio"] * o["desc"] / 100)

        st.write(f"{o['nombre']} - ₡{final}")

        if st.button(f"Comprar {o['nombre']}"):
            st.session_state["carrito"].append({
                "producto": o["nombre"],
                "precio": final,
                "cantidad": 1
            })

def acerca():
    st.title("🏢 Sobre Nosotros")

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("""
        ### 🐉 Pulpería El Dragón Dorado

        Somos una pulpería costarricense comprometida con brindar productos 
        esenciales de calidad a precios accesibles para nuestra comunidad.

        Nuestro enfoque es ofrecer una experiencia cercana, rápida y confiable.
        """)

        st.markdown("#### 🎯 Misión")
        st.write("Ofrecer productos de primera necesidad con excelente atención y precios justos.")

        st.markdown("#### 👁️ Visión")
        st.write("Ser una pulpería reconocida en San José por su servicio y confianza.")

    with col2:
        st.markdown("### 📍 Ubicación")
        st.info("Barrio Chino, San José")

    # ✅ MAPA SEGURO (SIN st.empty)
    st.markdown("""
    <iframe src="https://www.google.com/maps?q=Barrio+Chino+San+Jose+Costa+Rica&output=embed"
    width="100%" height="300"
    style="border:0;border-radius:10px;"></iframe>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.success("📍 Barrio Chino, San José")
    col2.success("☎ 2230-5698")
    col3.success("📧 contacto@dragondorado.cr")

    # ✅ FOOTER SIMPLE (estable)
    st.markdown("---")
    st.caption("© 2025 Pulpería El Dragón Dorado")
    
def contacto():
    st.title("📞 Contáctanos")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏢 Información")

        st.write("""
        Pulpería El Dragón Dorado  
        📍 San José, Barrio Chino  

        ☎ 2230-5698 
                  
        📧 contacto@dragondorado.cr  

        🕒 Lunes a Domingo  
        7:00 AM - 9:00 PM
        """)

    with col2:
        st.subheader("📍 Ubicación")

        st.components.v1.iframe(
            "https://www.google.com/maps?q=Barrio+Chino+San+Jose+Costa+Rica&output=embed",
            height=250
        )

    st.divider()

    st.subheader("📝 Enviar mensaje")

    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre")
        correo = st.text_input("Correo")

    with col2:
        tipo = st.selectbox("Tipo", ["Consulta", "Queja", "Sugerencia"])

    mensaje = st.text_area("Mensaje")

    if st.button("Enviar"):
        if nombre and correo and mensaje:
            st.success("Mensaje enviado ✔️")
        else:
            st.warning("Complete todos los campos")

    st.divider()
    st.caption("© 2025 Pulpería El Dragón Dorado")

# -------------------------
# CONTROL SEGURO INICIAL
# -------------------------
import streamlit as st
import bcrypt

# LOGIN
if "login" not in st.session_state:
    st.session_state["login"] = False

# USUARIO ACTUAL
if "user" not in st.session_state:
    st.session_state["user"] = None

# ROL
if "rol" not in st.session_state:
    st.session_state["rol"] = None

# VISTA PRINCIPAL (MENÚ)
if "view" not in st.session_state:
    st.session_state["view"] = "inicio"

# VISTA AUTH (login / registro)
if "auth_view" not in st.session_state:
    st.session_state["auth_view"] = None

# CARRITO
if "carrito" not in st.session_state:
    st.session_state["carrito"] = []


# -------------------------
# LOGIN
# -------------------------
def login():

    st.markdown("## 🔐 Bienvenido de nuevo")

    user = st.text_input("👤 Usuario")
    pwd = st.text_input("🔑 Contraseña", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Ingresar"):

            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute(
                "SELECT password, rol FROM usuarios WHERE username=?",
                (user,)
            )

            data = cursor.fetchone()
            conexion.close()

            if data:

                hashed_pw, rol = data

                if isinstance(hashed_pw, str):
                    hashed_pw = hashed_pw.encode()

                if bcrypt.checkpw(pwd.encode(), hashed_pw):

                    st.session_state["login"] = True
                    st.session_state["user"] = user
                    st.session_state["rol"] = rol
                    st.session_state["auth_view"] = None

                    st.success("✔ Login correcto")
                    st.rerun()

                else:
                    st.error("❌ Contraseña incorrecta")
            else:
                st.error("❌ Usuario no existe")

    with col2:
        if st.button("📝 Crear cuenta"):
            st.session_state["auth_view"] = "registro"
            st.rerun()


# -------------------------
# REGISTRO (VALIDADO)
# -------------------------
def registro():

    st.markdown("## 📝 Crear nueva cuenta")

    new_user = st.text_input("👤 Usuario")

    new_pass = st.text_input("🔑 Contraseña", type="password")

    rol = st.selectbox("🎭 Rol", ["empleado", "admin"])

    if st.button("💾 Registrar"):

        if len(new_user) < 4:
            st.error("Usuario muy corto (mínimo 4)")
            return

        if len(new_pass) < 6:
            st.error("Contraseña muy corta (mínimo 6)")
            return

        if not new_pass.isalnum():
            st.error("Solo letras y números en contraseña")
            return

        hashed = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt())

        conexion = conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "INSERT INTO usuarios(username,password,rol) VALUES(?,?,?)",
                (new_user, hashed, rol)
            )
            conexion.commit()
            st.success("✔ Usuario creado")

            st.session_state["auth_view"] = "login"
            st.rerun()

        except:
            st.error("❌ Usuario ya existe")

        conexion.close()

    if st.button("⬅ Volver al login"):
        st.session_state["auth_view"] = "login"
        st.rerun()


# -------------------------
# PROTECCIÓN REAL
# -------------------------
def require_login():
    if not st.session_state["login"]:
        st.warning("🔐 Debes iniciar sesión")
        st.stop()


# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("🛒 SUPERMERCADO POS")

# =========================
# PUBLICO (SIN LOGIN)
# =========================
if not st.session_state["login"]:

    st.sidebar.markdown("### 🧭 Público")

    if st.sidebar.button("🏠 Inicio"):
        inicio()

    if st.sidebar.button("🛍️ Productos"):
        productos()   # 👈 ahora SÍ es público

    if st.sidebar.button("🔥 Ofertas"):
        ofertas()     # 👈 ahora SÍ es público

    if st.sidebar.button("ℹ️ Acerca"):
        acerca()

    if st.sidebar.button("📞 Contacto"):
        contacto()

    st.sidebar.markdown("---")

    if st.sidebar.button("🔐 Login"):
        st.session_state["auth_view"] = "login"
        st.rerun()

    if st.sidebar.button("📝 Crear cuenta"):
        st.session_state["auth_view"] = "registro"
        st.rerun()

    
if not st.session_state["login"]:

    if st.session_state["auth_view"] == "registro":
        registro()
        st.stop()

    elif st.session_state["auth_view"] == "login":
        login()
        st.stop()

# =========================
# PRIVADO
# =========================
else:

    st.sidebar.markdown(f"👤 {st.session_state['user']}")

    if st.sidebar.button("📊 Dashboard"):
        dashboard()

    if st.sidebar.button("🛒 Compra"):
        compra()

    if st.sidebar.button("🧾 Factura"):
        factura()

    if st.sidebar.button("📦 Inventario"):
        inventario()

    if st.sidebar.button("💰 Caja"):
        ventas()

    if st.sidebar.button("🚪 Cerrar sesión"):
        st.session_state["login"] = False
        st.session_state["user"] = None
        st.session_state["rol"] = None
        st.session_state["auth_view"] = "login"
        st.rerun()

        