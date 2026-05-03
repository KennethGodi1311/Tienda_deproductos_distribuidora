import streamlit as st
import os
import bcrypt
from database.db import conectar


def perfil():

    st.title("👤 Mi perfil")

    usuario = st.session_state.get("user")

    if not usuario:
        st.warning("Debes iniciar sesión")
        return

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, foto, nombre, correo, telefono, direccion, edad
        FROM usuarios
        WHERE username=?
    """, (usuario,))

    data = cursor.fetchone()
    conn.close()

    if not data:
        st.error("Usuario no encontrado")
        return

    username_actual, foto_actual, nombre, correo, telefono, direccion, edad = data

    # -------------------------
    # FOTO
    # -------------------------
    st.subheader("🖼️ Foto de perfil")

    if foto_actual and os.path.exists(foto_actual):
        st.image(foto_actual, width=150)
    else:
        st.info("No tienes foto aún")

    nueva_foto = st.file_uploader("Subir nueva foto", type=["jpg", "png", "jpeg"])

    st.divider()

    # -------------------------
    # DATOS
    # -------------------------
    st.subheader("📋 Información personal")

    col1, col2 = st.columns(2)

    with col1:
        nuevo_username = st.text_input("👤 Usuario", value=username_actual)
        nuevo_nombre = st.text_input("🧑 Nombre completo", value=nombre or "")
        nuevo_correo = st.text_input("📧 Correo", value=correo or "")

    with col2:
        nuevo_telefono = st.text_input("📱 Teléfono", value=telefono or "")
        nueva_direccion = st.text_area("🏠 Dirección", value=direccion or "")
        nueva_edad = st.number_input("🎂 Edad", min_value=0, max_value=120, value=edad or 18)

    st.divider()

    # -------------------------
    # PASSWORD
    # -------------------------
    st.subheader("🔐 Seguridad")

    nueva_password = st.text_input("Nueva contraseña", type="password")
    confirmar_password = st.text_input("Confirmar contraseña", type="password")

    # -------------------------
    # GUARDAR
    # -------------------------
    if st.button("💾 Guardar cambios", use_container_width=True):

        try:
            conn = conectar()
            cursor = conn.cursor()

            ruta_foto = foto_actual

            # -------------------------
            # FOTO
            # -------------------------
            if nueva_foto:
                carpeta = "assets/usuarios"
                os.makedirs(carpeta, exist_ok=True)

                ruta_foto = f"{carpeta}/{nuevo_username}.jpg"

                with open(ruta_foto, "wb") as f:
                    f.write(nueva_foto.read())

            # -------------------------
            # PASSWORD (CORREGIDO 🔥)
            # -------------------------
            if nueva_password:

                if nueva_password != confirmar_password:
                    st.error("❌ Las contraseñas no coinciden")
                    return

                hashed = bcrypt.hashpw(
                    nueva_password.encode("utf-8"),
                    bcrypt.gensalt()
                ).decode("utf-8")

                cursor.execute("""
                    UPDATE usuarios
                    SET password=?
                    WHERE username=?
                """, (hashed, usuario))

            # -------------------------
            # EMAIL VALIDATION
            # -------------------------
            if nuevo_correo and "@" not in nuevo_correo:
                st.error("❌ Correo inválido")
                return

            # -------------------------
            # UPDATE GENERAL
            # -------------------------
            cursor.execute("""
                UPDATE usuarios
                SET username=?, foto=?, nombre=?, correo=?, telefono=?, direccion=?, edad=?
                WHERE username=?
            """, (
                nuevo_username,
                ruta_foto,
                nuevo_nombre,
                nuevo_correo,
                nuevo_telefono,
                nueva_direccion,
                nueva_edad,
                usuario
            ))

            conn.commit()
            conn.close()

            st.session_state["user"] = nuevo_username

            st.success("✅ Perfil actualizado correctamente")
            st.balloons()

        except Exception as e:
            st.error(f"❌ Error al guardar: {e}")

    st.markdown("---")
    st.caption("⚖️ Datos protegidos y usados solo para gestión del sistema")