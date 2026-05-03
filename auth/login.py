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

                # 🔥 SIEMPRE asegurar string limpio
                if isinstance(hashed_pw, bytes):
                    hashed_pw = hashed_pw.decode("utf-8")

                try:
                    if bcrypt.checkpw(
                        pwd.encode("utf-8"),
                        hashed_pw.encode("utf-8")
                    ):

                        st.session_state["login"] = True
                        st.session_state["user"] = user
                        st.session_state["rol"] = rol

                        st.session_state["page"] = "inicio"
                        st.session_state["auth_view"] = None
                        st.session_state["auth_mode"] = "login"

                        st.success(f"✔ Bienvenido {user}")
                        st.rerun()

                    else:
                        st.error("❌ Contraseña incorrecta")

                except ValueError:
                    st.error("❌ Hash corrupto. Borra usuarios y regístralos de nuevo.")
                    return

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

            codigo = str(random.randint(100000, 999999))

            st.session_state["codigo"] = codigo
            st.session_state["user_reset"] = user
            st.session_state["expira"] = time.time() + 300

            enviado = enviar_codigo(correo, codigo)

            if enviado:
                st.success("📧 Código enviado a tu correo")
            else:
                st.error("❌ Error enviando correo")

        codigo_input = st.text_input("🔢 Código recibido")
        nueva_password = st.text_input("🔑 Nueva contraseña", type="password")
        confirmar = st.text_input("🔑 Confirmar contraseña", type="password")

        if st.button("✅ Restablecer contraseña"):

            if time.time() > st.session_state.get("expira", 0):
                st.error("⏰ El código expiró")
                return

            if codigo_input != st.session_state.get("codigo"):
                st.error("❌ Código incorrecto")
                return

            if nueva_password != confirmar:
                st.error("❌ Las contraseñas no coinciden")
                return

            # 🔥 CLAVE: guardar como STRING (NO bytes)
            hashed = bcrypt.hashpw(
                nueva_password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

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