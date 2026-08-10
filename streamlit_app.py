import streamlit as st
from auth.login import login
from auth.registro import registro
from database.db import init_db

# Páginas
from pages.acerca import acerca
from pages.carrito import carrito
from pages.chatbot import chatbot
from pages.contacto import contacto
from pages.dashboard import dashboard
from pages.facturas import facturas
from pages.inicio import inicio
from pages.Inventario import inventario
from pages.ofertas import ofertas
from pages.pago import pago
from pages.perfil import perfil
from pages.productos import productos
from pages.ventas import ventas
from utils.styles import load_styles

# =========================
# CONFIGURACIÓN DE PÁGINA
# =========================
st.set_page_config(
    page_title="GodínezTech RestoControl POS", layout="wide", page_icon="🐉"
)

# =========================
# ESTILOS CSS RESPONSIVOS (MOBILE & DESKTOP ULTRA PRO)
# =========================
st.markdown(
    """
<style>
    /* 1. Reset Global y Ocultar Sidebar */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none !important; }
    
    .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 98% !important;
    }

    /* 2. CONTROL GLOBAL DE IMÁGENES (Para que no se vean gigantes) */
    div[data-testid="stImage"] img {
        max-height: 220px !important;
        object-fit: cover !important;
        border-radius: 12px !important;
        border: 1px solid rgba(0, 242, 254, 0.2) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
    }

    /* 3. Estilo del Contenedor Topbar */
    div[data-testid="stHorizontalBlock"] {
        background: #090d16;
        border: 1px solid rgba(0, 242, 254, 0.18);
        border-radius: 14px;
        padding: 6px 10px;
        align-items: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
        margin-bottom: 20px;
    }

    /* 4. Estilo General de Botones en la Navbar */
    div[data-testid="stHorizontalBlock"] .stButton > button {
        background: #111827 !important;
        color: #94a3b8 !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        padding: 0.35rem 0.5rem !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
        white-space: nowrap !important;
    }

    /* Hover de Botones */
    div[data-testid="stHorizontalBlock"] .stButton > button:hover {
        background: #1e293b !important;
        color: #38bdf8 !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.3) !important;
    }

    /* Botón Destacado Cyan */
    .btn-cyan .stButton > button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #0f172a !important;
        border: none !important;
        font-weight: 700 !important;
        box-shadow: 0 0 12px rgba(0, 242, 254, 0.4) !important;
    }

    /* Botón Morado */
    .btn-purple .stButton > button {
        background: transparent !important;
        border: 1px solid #a855f7 !important;
        color: #c084fc !important;
    }

    /* Brand Logo */
    .brand-title {
        color: #00f2fe;
        font-weight: 800;
        font-size: 1.1rem;
        letter-spacing: -0.5px;
        white-space: nowrap;
    }

    /* ========================================================= */
    /* 5. MEDIA QUERIES PARA CELULARES Y TABLETS (RESPONSIVE)     */
    /* ========================================================= */
    @media (max-width: 768px) {
        /* Permite scroll horizontal en la Topbar sin amontonar verticalmente */
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch;
            padding: 8px 4px !important;
            gap: 6px !important;
        }
        
        /* Ajustar ancho mínimo de columnas en móvil */
        div[data-testid="column"] {
            min-width: max-content !important;
            flex: 0 0 auto !important;
        }

        /* Reducir imágenes aún más en celular */
        div[data-testid="stImage"] img {
            max-height: 160px !important;
        }

        /* Ocultar texto secundario de la marca si no cabe */
        .brand-subtext {
            display: none !important;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# INICIALIZACIÓN DE DATOS
# =========================
load_styles()
init_db()

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


def ir(pagina):
    st.session_state["page"] = pagina
    st.rerun()


# =========================
# FLUJO DE AUTENTICACIÓN
# =========================
if st.session_state["auth_view"] == "login":
    login()
    st.stop()

elif st.session_state["auth_view"] == "registro":
    registro()
    st.stop()

# =========================
# BARRA DE NAVEGACIÓN HORIZONTAL RESPONSIVA
# =========================
if st.session_state["login"]:
    # NAVBAR USUARIO LOGUEADO
    cols = st.columns([1.8, 0.8, 0.9, 0.9, 0.9, 0.9, 0.9, 1.1, 1.1, 0.8])

    with cols[0]:
        st.markdown(
            f'<div class="brand-title">🐉 RestoPOS <span class="brand-subtext" style="font-size:0.75rem; color:#94a3b8; font-weight:normal;">({st.session_state["user"]})</span></div>',
            unsafe_allow_html=True,
        )

    if cols[1].button("🏠 Inicio"):
        ir("inicio")
    if cols[2].button("🍽️ Menú"):
        ir("productos")
    if cols[3].button("🔥 Ofertas"):
        ir("ofertas")
    if cols[4].button("ℹ️ Acerca"):
        ir("acerca")
    if cols[5].button("📞 Contacto"):
        ir("contacto")
    if cols[6].button("🤖 Bot"):
        ir("chatbot")

    if st.session_state["rol"] == "admin":
        if cols[7].button("⚙️ Admin"):
            ir("dashboard")
    else:
        if cols[7].button("🧾 Facturas"):
            ir("facturas")

    with cols[8]:
        st.markdown('<div class="btn-cyan">', unsafe_allow_html=True)
        if st.button(f"🛒 Pedido ({len(st.session_state['carrito'])})"):
            ir("carrito")
        st.markdown("</div>", unsafe_allow_html=True)

    if cols[9].button("🚪 Salir"):
        for key in ["login", "user", "rol"]:
            st.session_state[key] = None
        st.session_state["login"] = False
        st.session_state["auth_view"] = "login"
        st.session_state["page"] = "inicio"
        st.rerun()

else:
    # NAVBAR PÚBLICA
    cols = st.columns([2, 0.8, 0.8, 0.8, 0.8, 0.8, 0.9, 1.1, 1.3])

    with cols[0]:
        st.markdown(
            '<div class="brand-title">🐉 RestoControl POS</div>',
            unsafe_allow_html=True,
        )

    if cols[1].button("Inicio"):
        ir("inicio")
    if cols[2].button("Menú"):
        ir("productos")
    if cols[3].button("Ofertas"):
        ir("ofertas")
    if cols[4].button("Acerca"):
        ir("acerca")
    if cols[5].button("Contacto"):
        ir("contacto")
    if cols[6].button("Sommelier"):
        ir("chatbot")

    with cols[7]:
        st.markdown('<div class="btn-purple">', unsafe_allow_html=True)
        if st.button("📝 Registro"):
            st.session_state["auth_view"] = "registro"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with cols[8]:
        st.markdown('<div class="btn-cyan">', unsafe_allow_html=True)
        if st.button("🔐 Iniciar Sesión →"):
            st.session_state["auth_view"] = "login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# ENRUTADOR DE PÁGINAS (ROUTER)
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
elif page == "facturas":
    facturas()
elif page == "dashboard":
    if st.session_state["rol"] == "admin":
        dashboard()
    else:
        st.error("🚫 Acceso denegado")
elif page == "inventario":
    if st.session_state["rol"] == "admin":
        inventario()
    else:
        st.error("🚫 Acceso denegado")
elif page == "ventas":
    ventas()
elif page == "perfil":
    perfil()