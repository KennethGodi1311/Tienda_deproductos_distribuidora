import streamlit as st
import bcrypt
from database.db import conectar

def registro():

    st.markdown("## 📝 Crear cuenta")

    # -------------------------
    # BOTÓN VOLVER AL INICIO (ARRIBA)
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
    confirm_pwd = st.text_input("🔁 Confirmar contraseña", type="password")

    rol = st.selectbox("🎭 Rol", ["empleado", "admin"])

    col1, col2 = st.columns(2)

    # -------------------------
    # REGISTRAR
    # -------------------------
    with col1:
        if st.button("💾 Registrar"):

            if not user or not pwd or not confirm_pwd:
                st.warning("⚠️ Completa todos los campos")
                return

            if len(user) < 4:
                st.warning("⚠️ Usuario mínimo 4 caracteres")
                return

            if len(pwd) < 6:
                st.warning("⚠️ Contraseña mínimo 6 caracteres")
                return

            if pwd != confirm_pwd:
                st.error("❌ Las contraseñas no coinciden")
                return

            if not pwd.isalnum():
                st.warning("⚠️ Solo letras y números")
                return

            with st.spinner("Creando usuario..."):

                conexion = conectar()
                cursor = conexion.cursor()

                cursor.execute(
                    "SELECT id FROM usuarios WHERE username=?",
                    (user,)
                )

                if cursor.fetchone():
                    st.error("❌ Usuario ya existe")
                    conexion.close()
                    return

                hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())

                cursor.execute(
                    "INSERT INTO usuarios(username,password,rol) VALUES(?,?,?)",
                    (user, hashed, rol)
                )

                conexion.commit()
                conexion.close()

            st.success("✔ Usuario creado correctamente")
            st.balloons()

            st.session_state["auth_view"] = "login"
            st.rerun()

    # -------------------------
    # BOTONES ABAJO
    # -------------------------
    with col2:
        if st.button("⬅ Volver al login"):
            st.session_state["auth_view"] = "login"
            st.rerun()
            st.session_state["auth_view"] = None
            st.session_state["page"] = "inicio"
            st.rerun()

    st.markdown("---")
    st.caption("Crea una cuenta para acceder al sistema")