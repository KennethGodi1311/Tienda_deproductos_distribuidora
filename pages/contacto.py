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

        # 🔥 DERECHO DEL CONSUMIDOR
        st.info("""
⚖️ Conforme a la normativa de protección al consumidor en Costa Rica,  
usted tiene derecho a presentar consultas, quejas o reclamos 
relacionados con productos o servicios adquiridos.
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
        tipo = st.selectbox(
            "📌 Tipo de mensaje",
            ["Consulta", "Queja", "Sugerencia", "Reclamo formal"]
        )

    mensaje = st.text_area("💬 Mensaje")

    # 🔥 CONSENTIMIENTO LEGAL
    acepta = st.checkbox("Acepto el tratamiento de mis datos personales")

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

        if not acepta:
            st.error("⚠️ Debe aceptar la política de datos")
            return

        # Simulación de registro (esto es clave legalmente)
        st.success("✔ Mensaje enviado correctamente")
        st.info(f"Tipo: {tipo}")

        # 🔥 IMPORTANTE (trazabilidad legal)
        if tipo == "Reclamo formal":
            st.warning("""
📌 Su reclamo ha sido registrado.
Será atendido conforme a los plazos establecidos por normativa.
""")

        st.balloons()

    st.divider()

    # -------------------------
    # 🔒 PRIVACIDAD
    # -------------------------
    with st.expander("🔒 Política de privacidad"):

        st.write("""
La información proporcionada será utilizada únicamente para atender su solicitud.

- No se compartirá con terceros.
- Se utilizará únicamente con fines de contacto.
- Se respeta la confidencialidad del usuario.

Este sistema es una simulación con fines educativos.
""")

    # -------------------------
    # FOOTER
    # -------------------------
    col1, col2, col3 = st.columns(3)

    col1.info("📍 San José")
    col2.info("☎ 2230-5698")
    col3.info("📧 contacto@dragondorado.cr")

    st.markdown("---")
    st.caption("""
© 2025 Pulpería El Dragón Dorado  

Sistema de demostración académica.  
No constituye un canal oficial de gestión legal.
""")