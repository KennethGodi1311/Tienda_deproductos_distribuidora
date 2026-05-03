import streamlit as st
import bcrypt
import random
import time
from database.db import conectar
from utils.email import enviar_codigo

def login():

    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"

    modo = st.session_state["auth_mode"]

    st.markdown("## 🔐 Acceso al sistema")

    if st.button("🏠 Volver al inicio"):
        st.session_state["auth_view"] = None
        st.session_state["page"] = "inicio"
        st.rerun()

    st.markdown("---")

    # ================= LOGIN =================
    if modo == "login":

        user = st.text_input("👤 Usuario")
        pwd = st.text_input("🔑 Contraseña", type="password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🚀 Ingresar"):

                if not user or not pwd:
                    st.warning("⚠️ Completa todos los campos")
                    return

                conn = conectar()
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT password, rol FROM usuarios WHERE username=?",
                    (user,)
                )

                data = cursor.fetchone()
                conn.close()

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

                    st.success(f"✔ Bienvenido {user}")
                    st.rerun()

                else:
                    st.error("❌ Contraseña incorrecta")

        with col2:
            if st.button("📝 Crear cuenta"):
                st.session_state["auth_view"] = "registro"
                st.rerun()

        st.markdown("---")

        if st.button("🔑 ¿Olvidaste tu contraseña?"):
            st.session_state["auth_mode"] = "recuperar"
            st.rerun()

    # ================= RECUPERAR =================
    elif modo == "recuperar":

        st.subheader("🔄 Recuperar contraseña")

        user = st.text_input("👤 Usuario")

        if st.button("📩 Enviar código"):

            conn = conectar()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT correo FROM usuarios WHERE username=?",
                (user,)
            )
            data = cursor.fetchone()
            conn.close()

            if not data or not data[0]:
                st.error("❌ Usuario sin correo registrado")
                return

            correo = data[0]

            # 🔥 GENERAR CÓDIGO
            codigo = str(random.randint(100000, 999999))

            # GUARDAR EN SESIÓN
            st.session_state["codigo"] = codigo
            st.session_state["user_reset"] = user
            st.session_state["expira"] = time.time() + 300  # 5 min

            # 🔥 ENVIAR EMAIL REAL
            enviado = enviar_codigo(correo, codigo)

            if enviado:
                st.success("📧 Código enviado a tu correo")
            else:
                st.error("❌ Error enviando correo")

        # INPUTS
        codigo_input = st.text_input("🔢 Código recibido")
        nueva_password = st.text_input("🔑 Nueva contraseña", type="password")
        confirmar = st.text_input("🔑 Confirmar contraseña", type="password")

        if st.button("✅ Restablecer contraseña"):

            # VALIDAR EXPIRACIÓN
            if time.time() > st.session_state.get("expira", 0):
                st.error("⏰ El código expiró")
                return

            if codigo_input != st.session_state.get("codigo"):
                st.error("❌ Código incorrecto")
                return

            if nueva_password != confirmar:
                st.error("❌ Las contraseñas no coinciden")
                return

            hashed = bcrypt.hashpw(nueva_password.encode(), bcrypt.gensalt())

            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE usuarios
                SET password=?
                WHERE username=?
            """, (hashed, st.session_state["user_reset"]))

            conn.commit()
            conn.close()

            st.success("✔ Contraseña actualizada")
            st.session_state["auth_mode"] = "login"
            st.rerun()

        st.markdown("---")

        if st.button("⬅ Volver"):
            st.session_state["auth_mode"] = "login"
            st.rerun()

    st.markdown("---")
    st.caption("🔐 Sistema seguro con recuperación por correo")