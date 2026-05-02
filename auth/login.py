import streamlit as st
import bcrypt
from database.db import conectar

def login():

    st.markdown("## 🔐 Bienvenido")

    # -------------------------
    # BOTÓN VOLVER AL INICIO
    # -------------------------
    if st.button("🏠 Volver al inicio"):
        st.session_state["auth_view"] = None
        st.session_state["page"] = "inicio"
        st.rerun()

    st.markdown("---")

    # -------------------------
    # INPUTS
    # -------------------------
    user = st.text_input("👤 Usuario")
    pwd = st.text_input("🔑 Contraseña", type="password")

    col1, col2 = st.columns(2)

    # -------------------------
    # LOGIN
    # -------------------------
    with col1:
        if st.button("🚀 Ingresar"):

            if not user or not pwd:
                st.warning("⚠️ Completa todos los campos")
                return

            with st.spinner("Validando..."):

                conexion = conectar()
                cursor = conexion.cursor()

                cursor.execute(
                    "SELECT password, rol FROM usuarios WHERE username=?",
                    (user,)
                )

                data = cursor.fetchone()
                conexion.close()

            if not data:
                st.error("❌ Usuario no existe")
                return

            hashed_pw, rol = data

            if isinstance(hashed_pw, str):
                hashed_pw = hashed_pw.encode()

            if bcrypt.checkpw(pwd.encode(), hashed_pw):

                st.session_state["login"] = True
                st.session_state["user"] = user
                st.session_state["rol"] = rol
                st.session_state["auth_view"] = None

                st.success(f"✔ Bienvenido {user}")
                st.balloons()

                st.rerun()

            else:
                st.error("❌ Contraseña incorrecta")

    # -------------------------
    # BOTONES DERECHA
    # -------------------------
    with col2:
        if st.button("📝 Crear cuenta"):
            st.session_state["auth_view"] = "registro"
            st.rerun()

        if st.button("🏠 Ir al inicio"):
            st.session_state["auth_view"] = None
            st.session_state["page"] = "inicio"
            st.rerun()

    # -------------------------
    # EXTRA UX
    # -------------------------
    st.markdown("---")
    st.caption("Usa tus credenciales para ingresar al sistema")