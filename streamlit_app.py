import streamlit as st
from database.db import init_db
from auth.login import login
from auth.registro import registro
from pages.inicio import inicio
from pages.productos import productos
from pages.ofertas import ofertas
from pages.acerca import acerca
from pages.contacto import contacto
from pages.chatbot import chatbot  # ✅ NUEVO
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
if "login" not in st.session_state:
    st.session_state["login"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "rol" not in st.session_state:
    st.session_state["rol"] = None

if "auth_view" not in st.session_state:
    st.session_state["auth_view"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "inicio"

if "carrito" not in st.session_state:
    st.session_state["carrito"] = []

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

    # 🤖 NUEVO CHATBOT
    if st.sidebar.button("🤖 Chatbot"):
        st.session_state["page"] = "chatbot"

    st.sidebar.markdown("---")

    # 🔥 SOLO ADMIN
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
    st.sidebar.write(f"Productos: {len(st.session_state['carrito'])}")

    if st.sidebar.button("Ver carrito"):
        st.session_state["page"] = "carrito"

    # 🚪 LOGOUT
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

    # 🤖 CHATBOT TAMBIÉN EN PÚBLICO
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
page = st.session_state.get("page", "inicio")

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

elif page == "chatbot":  # ✅ NUEVO
    chatbot()

# 🔥 PÁGINAS FUTURAS
elif page == "carrito":
    st.title("🛒 Carrito")
    st.write(st.session_state["carrito"])

elif page == "inventario":
    st.title("📦 Inventario (admin)")
    st.info("Próximamente...")

elif page == "ventas":
    st.title("💰 Ventas (admin)")
    st.info("Próximamente...")

elif page == "dashboard":
    st.title("📊 Dashboard (admin)")
    st.info("Próximamente...")