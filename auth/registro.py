import bcrypt
import streamlit as st
from database.db import conectar


def render_bootstrap_registro():
    # Estilos CSS
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(135deg, #0f0d0e 0%, #1a1618 50%, #261c14 100%);
                color: #f8fafc;
            }
            .text-amber { color: #f59e0b !important; }
            .text-subtext { color: #e4e4e7 !important; }
            
            /* Botón superior nativo */
            div.stButton > button[key="btn_reg_home"] {
                border: 1px solid #f59e0b !important;
                color: #f59e0b !important;
                background-color: transparent !important;
                border-radius: 8px !important;
            }
            div.stButton > button[key="btn_reg_home"]:hover {
                background-color: #f59e0b !important;
                color: #0f0d0e !important;
            }

            /* Botón para volver al login */
            div.stButton > button[key="btn_go_login"] {
                border: 1px solid #f59e0b !important;
                color: #f59e0b !important;
                background: transparent !important;
                border-radius: 20px !important;
            }
            div.stButton > button[key="btn_go_login"]:hover {
                background: #f59e0b !important;
                color: #0f0d0e !important;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # 1. BARRA SUPERIOR (Menú Principal)
    nav_col1, nav_col2 = st.columns([3, 1])
    with nav_col1:
        st.markdown(
            "### 👤 <span class='text-amber'>RESTO-POS ONBOARDING</span>",
            unsafe_allow_html=True,
        )
    with nav_col2:
        if st.button("🏠 Menú Principal", key="btn_reg_home"):
            st.session_state["auth_view"] = None
            st.session_state["page"] = "inicio"
            st.rerun()

    st.write("")

    # 2. ESTRUCTURA DE 2 COLUMNAS (BRANDING Y FORMULARIO)
    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #b45309 0%, #78350f 50%, #451a03 100%); padding: 2rem; border-radius: 15px; height: 100%;">
                <span style="background: rgba(0,0,0,0.3); border: 1px solid #f59e0b; color: #fbbf24; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem;">
                    👤 ALTA DE PERSONAL
                </span>
                <h2 style="color: white; margin-top: 15px;">Crear Usuario</h2>
                <p class="text-subtext">Habilita accesos al sistema para meseros, chefs, cajeros o administradores del restaurante.</p>
                <br>
                <div style="margin-bottom: 12px;">
                    <strong>🔒 Seguridad con Bcrypt</strong><br>
                    <small class="text-subtext">Las credenciales se almacenan con encriptación segura.</small>
                </div>
                <div>
                    <strong>🪪 Perfiles de Permisos</strong><br>
                    <small class="text-subtext">Acceso adaptado a comandas o administración.</small>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.subheader("Crear Usuario")
        st.caption("Asigna credenciales para el sistema gastronómico")

        # Formulario nativo de registro
        with st.form("register_form_native"):
            user = st.text_input(
                "Nombre de Usuario",
                placeholder="ej. mesero.juan",
                help="Mínimo 4 caracteres",
            ).strip()

            rol = st.selectbox(
                "Rol en Sistema",
                options=["empleado", "admin"],
                format_func=lambda x: (
                    "Empleado / Mesero"
                    if x == "empleado"
                    else "Administrador / Chef"
                ),
            )

            pwd_col1, pwd_col2 = st.columns(2)
            with pwd_col1:
                pwd = st.text_input(
                    "Contraseña", type="password", placeholder="••••••••"
                )
            with pwd_col2:
                confirm_pwd = st.text_input(
                    "Confirmar Contraseña",
                    type="password",
                    placeholder="••••••••",
                )

            submitted = st.form_submit_button(
                "✔ Registrar Empleado", use_container_width=True
            )

            if submitted:
                if not user or not pwd or not confirm_pwd:
                    st.warning("⚠️ Completa todos los campos del formulario")
                elif len(user) < 4:
                    st.warning("⚠️ El usuario debe tener al menos 4 caracteres")
                elif len(pwd) < 6:
                    st.warning(
                        "⚠️ La contraseña debe tener al menos 6 caracteres"
                    )
                elif pwd != confirm_pwd:
                    st.error("❌ Las contraseñas no coinciden")
                elif not pwd.isalnum():
                    st.warning(
                        "⚠️ La contraseña solo debe contener letras y números"
                    )
                else:
                    with st.spinner(
                        "Registrando personal en el sistema POS..."
                    ):
                        conexion = conectar()
                        cursor = conexion.cursor()

                        cursor.execute(
                            "SELECT id FROM usuarios WHERE username=?", (user,)
                        )

                        if cursor.fetchone():
                            st.error(
                                f"❌ El usuario '{user}' ya existe en el sistema"
                            )
                            conexion.close()
                        else:
                            hashed = bcrypt.hashpw(
                                pwd.encode("utf-8"), bcrypt.gensalt()
                            ).decode("utf-8")

                            cursor.execute(
                                "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
                                (user, hashed, rol),
                            )
                            conexion.commit()
                            conexion.close()

                            st.success(
                                "✔ Usuario registrado exitosamente. Redirigiendo al login..."
                            )
                            st.balloons()
                            st.session_state["auth_view"] = "login"
                            st.rerun()

        st.divider()

        # Botón para regresar al Menú Principal / Inicio
        col_text, col_btn = st.columns([1.5, 1])
        with col_text:
            st.caption("¿Deseas volver a la tienda?")
        with col_btn:
            if st.button("🏠 Ir a la Tienda", key="btn_go_inicio"):
                st.session_state["auth_view"] = None
                st.session_state["page"] = "inicio"
                st.rerun()


def registro():
    render_bootstrap_registro()