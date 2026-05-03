import streamlit as st
from database.db import init_db
from auth.login import login
from auth.registro import registro

# Páginas
from pages.inicio import inicio
from pages.productos import productos
from pages.ofertas import ofertas
from pages.acerca import acerca
from pages.contacto import contacto
from pages.chatbot import chatbot
from pages.carrito import carrito
from pages.pago import pago
from pages.dashboard import dashboard
from pages.facturas import facturas   # 🔥 NUEVO
from pages.ventas import ventas
from pages.Inventario import inventario


from utils.styles import load_styles

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Pulpería El Dragón Dorado",
    layout="wide",
    page_icon="🐉"
)

# 🔥 OCULTAR MENÚ AUTOMÁTICO DE STREAMLIT
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)

# =========================
# INIT
# =========================
load_styles()
init_db()

# =========================
# SESSION STATE
# =========================
defaults = {
    "login": False,
    "user": None,
    "rol": None,
    "auth_view": None,
    "page": "inicio",
    "carrito": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================
# FUNCIÓN NAVEGACIÓN
# =========================
def ir(pagina):
    st.session_state["page"] = pagina
    st.rerun()

# =========================
# AUTH FLOW
# =========================
if st.session_state["auth_view"] == "login":
    login()
    st.stop()

elif st.session_state["auth_view"] == "registro":
    registro()
    st.stop()

# =========================
# SIDEBAR
# =========================
st.sidebar.markdown("## 🐉 Menú")

# -------------------------
# USUARIO LOGUEADO
# -------------------------
if st.session_state["login"]:

    st.sidebar.success(f"👤 {st.session_state['user']}")
    st.sidebar.caption(f"Rol: {st.session_state['rol']}")

    st.sidebar.markdown("### 🧭 Navegación")

    if st.sidebar.button("🏠 Inicio"):
        ir("inicio")

    if st.sidebar.button("🛍️ Productos"):
        ir("productos")

    if st.sidebar.button("🔥 Ofertas"):
        ir("ofertas")

    if st.sidebar.button("ℹ️ Acerca"):
        ir("acerca")

    if st.sidebar.button("📞 Contacto"):
        ir("contacto")

    if st.sidebar.button("🤖 Chatbot"):
        ir("chatbot")

    # 🔥 NUEVO: FACTURAS
    if st.sidebar.button("🧾 Facturas"):
        ir("facturas")

    st.sidebar.markdown("---")

    # ADMIN
    if st.session_state["rol"] == "admin":
        st.sidebar.markdown("### ⚙️ Administración")

        if st.sidebar.button("📦 Inventario"):
            ir("inventario")

        if st.sidebar.button("💰 Ventas"):
            ir("ventas")

        if st.sidebar.button("📊 Dashboard"):
            ir("dashboard")

    st.sidebar.markdown("---")

    # 🛒 CARRITO
    st.sidebar.markdown("### 🛒 Carrito")
    st.sidebar.metric("Productos", len(st.session_state["carrito"]))

    if st.sidebar.button("Ver carrito"):
        ir("carrito")

    if st.sidebar.button("Ir a pagar"):
        ir("pago")

    # LOGOUT
    if st.sidebar.button("🚪 Cerrar sesión"):
        for key in ["login", "user", "rol"]:
            st.session_state[key] = None

        st.session_state["login"] = False
        st.session_state["auth_view"] = "login"
        st.session_state["page"] = "inicio"

        st.rerun()

# -------------------------
# USUARIO PÚBLICO
# -------------------------
else:

    st.sidebar.info("Modo público")

    if st.sidebar.button("🏠 Inicio"):
        ir("inicio")

    if st.sidebar.button("🛍️ Productos"):
        ir("productos")

    if st.sidebar.button("🔥 Ofertas"):
        ir("ofertas")

    if st.sidebar.button("ℹ️ Acerca"):
        ir("acerca")

    if st.sidebar.button("📞 Contacto"):
        ir("contacto")

    if st.sidebar.button("🤖 Chatbot"):
        ir("chatbot")

    st.sidebar.markdown("---")

    if st.sidebar.button("🔐 Login"):
        st.session_state["auth_view"] = "login"
        st.rerun()

    if st.sidebar.button("📝 Crear cuenta"):
        st.session_state["auth_view"] = "registro"
        st.rerun()

# =========================
# ROUTER
# =========================
page = st.session_state["page"]

if page == "inicio":
    inicio()

elif page == "productos":
    productos()

elif page == "ofertas":
    ofertas()

elif page == "acerca":
    acerca()

elif page == "contacto":
    contacto()

elif page == "chatbot":
    chatbot()

elif page == "carrito":
    carrito()

elif page == "pago":
    pago()

# 🔥 NUEVO
elif page == "facturas":
    facturas()

elif page == "dashboard":
    if st.session_state["rol"] == "admin":
        dashboard()
    else:
        st.error("🚫 No autorizado")

elif page == "inventario":
    if st.session_state["rol"] == "admin":
        inventario()
    else:
        st.error("🚫 No autorizado")

elif page == "ventas":
    ventas()