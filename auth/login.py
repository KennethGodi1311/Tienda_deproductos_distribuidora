import bcrypt
import streamlit as st
from database.db import conectar


def render_bootstrap_login():
    # Estilos CSS generales para la vista
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(135deg, #0f0d0e 0%, #1a1618 50%, #261c14 100%);
                color: #f8fafc;
            }
            .text-amber { color: #f59e0b !important; }
            
            /* Personalización de botones nativos */
            div.stButton > button[key="btn_home"] {
                border: 1px solid #f59e0b !important;
                color: #f59e0b !important;
                background-color: transparent !important;
                border-radius: 8px !important;
            }
            div.stButton > button[key="btn_home"]:hover {
                background-color: #f59e0b !important;
                color: #0f0d0e !important;
            }

            div.stButton > button[key="btn_forgot"] {
                border: none !important;
                background: transparent !important;
                color: #f59e0b !important;
                text-decoration: underline !important;
                padding: 0 !important;
                font-size: 0.85rem !important;
            }

            div.stButton > button[key="btn_login_submit"] {
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
                color: #0f0d0e !important;
                font-weight: bold !important;
                border: none !important;
                width: 100% !important;
                border-radius: 10px !important;
                padding: 0.6rem !important;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # 1. Barra superior de navegación (Botón Menú Principal Nativo)
    nav_col1, nav_col2 = st.columns([3, 1])
    with nav_col1:
        st.markdown(
            "### 🏪 <span class='text-amber'>SISTEMA POS & GASTRONOMÍA</span>",
            unsafe_allow_html=True,
        )
    with nav_col2:
        if st.button("🏠 Menú Principal", key="btn_home"):
            st.session_state["auth_view"] = None
            st.session_state["page"] = "inicio"
            st.rerun()

    st.write("")

    # 2. Formulario de Acceso Nativo de Streamlit
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #b45309 0%, #78350f 50%, #451a03 100%); padding: 2rem; border-radius: 15px; height: 100%;">
                <span style="background: rgba(0,0,0,0.3); border: 1px solid #f59e0b; color: #fbbf24; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;">
                    🔥 PORTAL DE COLABORADORES
                </span>
                <h2 style="color: white; margin-top: 15px;">Gestión de Pedidos & Cocina</h2>
                <p style="color: #e4e4e7;">Control integral para comandas, inventario y reservaciones en tiempo real.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.subheader("Acceso al Sistema")
        st.caption("Ingresa tus credenciales de usuario")

        with st.form("login_form_native"):
            user = st.text_input(
                "Usuario", placeholder="ej. mesero1 / chef.juan"
            )
            pwd = st.text_input(
                "Contraseña", type="password", placeholder="••••••••"
            )
            submitted = st.form_submit_button(
                "Iniciar Sesión ➔", use_container_width=True
            )

            if submitted:
                if not user or not pwd:
                    st.error("⚠️ Ingrese usuario y contraseña")
                else:
                    conn = conectar()
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT password, rol FROM usuarios WHERE username=?",
                        (user,),
                    )
                    data = cursor.fetchone()
                    conn.close()

                    if not data:
                        st.error("❌ Credenciales incorrectas")
                    else:
                        hashed_pw, rol = data
                        if isinstance(hashed_pw, bytes):
                            hashed_pw = hashed_pw.decode("utf-8")

                        try:
                            if bcrypt.checkpw(
                                pwd.encode("utf-8"), hashed_pw.encode("utf-8")
                            ):
                                st.session_state["login"] = True
                                st.session_state["user"] = user
                                st.session_state["rol"] = rol
                                st.session_state["auth_view"] = None
                                st.session_state["page"] = "inicio"
                                st.success(f"✔ ¡Bienvenido, {user}!")
                                st.rerun()
                            else:
                                st.error("❌ Contraseña incorrecta")
                        except ValueError:
                            st.error("❌ Hash corrupto en la base de datos")

        # Botón "¿Olvidaste tu contraseña?" afuera del form
        if st.button("¿Olvidaste tu contraseña?", key="btn_forgot"):
            st.session_state["auth_view"] = None
            st.session_state["page"] = "inicio"
            st.rerun()

        st.divider()

        if st.button(
            "👤 Registrar Empleado",
            key="btn_register",
            use_container_width=True,
        ):
            st.session_state["auth_view"] = "registro"
            st.rerun()


def login():
    render_bootstrap_login()