import streamlit as st
import re

def contacto():

    st.title("📞 Contáctanos")

    # -------------------------
    # BOTÓN VOLVER
    # -------------------------
    if st.button("🏠 Volver al inicio"):
        st.session_state["page"] = "inicio"
        st.rerun()

    st.divider()

    col1, col2 = st.columns(2)

    # -------------------------
    # INFO
    # -------------------------
    with col1:
        st.subheader("🏢 Información")

        st.markdown("""
        **Pulpería El Dragón Dorado**  

        📍 Barrio Chino, San José  
        ☎ 2230-5698  
        📧 contacto@dragondorado.cr  

        🕒 Lunes a Domingo  
        7:00 AM - 9:00 PM
        """)

    # -------------------------
    # MAPA
    # -------------------------
    with col2:
        st.subheader("📍 Ubicación")

        st.components.v1.iframe(
            "https://www.google.com/maps?q=Barrio+Chino+San+Jose+Costa+Rica&output=embed",
            height=280
        )

    st.divider()

    # -------------------------
    # FORMULARIO
    # -------------------------
    st.subheader("📝 Enviar mensaje")

    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("👤 Nombre")
        correo = st.text_input("📧 Correo")

    with col2:
        tipo = st.selectbox("📌 Tipo de mensaje", ["Consulta", "Queja", "Sugerencia"])

    mensaje = st.text_area("💬 Mensaje")

    # -------------------------
    # VALIDACIÓN EMAIL
    # -------------------------
    def email_valido(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    # -------------------------
    # BOTÓN ENVIAR
    # -------------------------
    if st.button("📨 Enviar mensaje"):

        if not nombre or not correo or not mensaje:
            st.warning("⚠️ Complete todos los campos")
            return

        if not email_valido(correo):
            st.error("❌ Correo inválido")
            return

        # Simulación de envío
        st.success("✔ Mensaje enviado correctamente")
        st.info(f"Tipo: {tipo}")

        st.balloons()

    st.divider()

    # -------------------------
    # FOOTER
    # -------------------------
    col1, col2, col3 = st.columns(3)

    col1.info("📍 San José")
    col2.info("☎ 2230-5698")
    col3.info("📧 contacto@dragondorado.cr")

    st.markdown("---")
    st.caption("© 2025 Pulpería El Dragón Dorado")