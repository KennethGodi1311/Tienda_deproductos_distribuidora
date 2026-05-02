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
from pages.carrito import carrito       # ✅ NUEVO
from pages.pago import pago    
from pages.dashboard import dashboard         # ✅ NUEVO

from utils.styles import load_styles

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Pulpería El Dragón Dorado",
    layout="wide",
    page_icon="🐉"
)

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
        st.session_state["page"] = "inicio"

    if st.sidebar.button("🛍️ Productos"):
        st.session_state["page"] = "productos"

    if st.sidebar.button("🔥 Ofertas"):
        st.session_state["page"] = "ofertas"

    if st.sidebar.button("ℹ️ Acerca"):
        st.session_state["page"] = "acerca"

    if st.sidebar.button("📞 Contacto"):
        st.session_state["page"] = "contacto"

    if st.sidebar.button("🤖 Chatbot"):
        st.session_state["page"] = "chatbot"

    st.sidebar.markdown("---")

    # ADMIN
    if st.session_state["rol"] == "admin":
        st.sidebar.markdown("### ⚙️ Administración")

        if st.sidebar.button("📦 Inventario"):
            st.session_state["page"] = "inventario"

        if st.sidebar.button("💰 Ventas"):
            st.session_state["page"] = "ventas"

        if st.sidebar.button("📊 Dashboard"):
            st.session_state["page"] = "dashboard"

    st.sidebar.markdown("---")

    # 🛒 CARRITO
    st.sidebar.markdown("### 🛒 Carrito")
    st.sidebar.metric("Productos", len(st.session_state["carrito"]))

    if st.sidebar.button("Ver carrito"):
        st.session_state["page"] = "carrito"

    if st.sidebar.button("Ir a pagar"):
        st.session_state["page"] = "pago"

    # LOGOUT
    if st.sidebar.button("🚪 Cerrar sesión"):
        st.session_state.clear()
        st.session_state["auth_view"] = "login"
        st.rerun()

# -------------------------
# USUARIO PÚBLICO
# -------------------------
else:

    st.sidebar.info("Modo público")

    if st.sidebar.button("🏠 Inicio"):
        st.session_state["page"] = "inicio"

    if st.sidebar.button("🛍️ Productos"):
        st.session_state["page"] = "productos"

    if st.sidebar.button("🔥 Ofertas"):
        st.session_state["page"] = "ofertas"

    if st.sidebar.button("ℹ️ Acerca"):
        st.session_state["page"] = "acerca"

    if st.sidebar.button("📞 Contacto"):
        st.session_state["page"] = "contacto"

    if st.sidebar.button("🤖 Chatbot"):
        st.session_state["page"] = "chatbot"

    st.sidebar.markdown("---")

    if st.sidebar.button("🔐 Login"):
        st.session_state["auth_view"] = "login"
        st.rerun()

    if st.sidebar.button("📝 Crear cuenta"):
        st.session_state["auth_view"] = "registro"
        st.rerun()

# =========================
# ROUTER (NAVEGACIÓN)
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

# 🔥 NUEVAS PÁGINAS REALES
elif page == "carrito":
    carrito()

elif page == "pago":
    pago()

elif page == "dashboard":
    dashboard()

# ADMIN
elif page == "inventario":
    st.title("📦 Inventario (admin)")
    st.info("Próximamente...")

elif page == "ventas":
    st.title("💰 Ventas (admin)")
    st.info("Próximamente...")

elif page == "dashboard":
    st.title("📊 Dashboard (admin)")
    st.info("Próximamente...")

elif page == "pago":
    from pages.pago import pago
    pago()