import streamlit as st

def acerca():

    st.title("🏢 Sobre Nosotros")

    # -------------------------
    # BOTÓN VOLVER
    # -------------------------
    if st.button("🏠 Volver al inicio"):
        st.session_state["page"] = "inicio"
        st.rerun()

    st.divider()

    col1, col2 = st.columns([2,1])

    # -------------------------
    # INFO PRINCIPAL
    # -------------------------
    with col1:
        st.markdown("""
        ### 🐉 Pulpería El Dragón Dorado

        Somos una pulpería costarricense comprometida con brindar productos 
        esenciales de calidad a precios accesibles para nuestra comunidad.

        Nuestro objetivo es ofrecer una experiencia rápida, cercana y confiable.
        """)

        st.markdown("#### 🎯 Misión")
        st.write("Ofrecer productos de primera necesidad con excelente atención y precios justos.")

        st.markdown("#### 👁️ Visión")
        st.write("Ser una pulpería líder en San José reconocida por su calidad y servicio.")

        # -------------------------
        # VALORES
        # -------------------------
        st.markdown("#### 💡 Valores")
        st.success("✔ Atención al cliente")
        st.success("✔ Calidad en productos")
        st.success("✔ Precios accesibles")
        st.success("✔ Confianza")

        st.divider()

        # -------------------------
        # ⚖️ MARCO LEGAL (NUEVO 🔥)
        # -------------------------
        st.markdown("#### ⚖️ Cumplimiento Legal")

        st.info("""
Este sistema se desarrolla conforme a principios básicos del comercio electrónico 
y protección al consumidor en Costa Rica.

✔ Transparencia en precios  
✔ Información clara al consumidor  
✔ Registro de transacciones  
✔ Protección de datos personales  
""")

        # -------------------------
        # 📜 TÉRMINOS Y CONDICIONES
        # -------------------------
        with st.expander("📜 Términos y Condiciones"):

            st.write("""
El uso de este sistema implica la aceptación de las siguientes condiciones:

- Los precios mostrados incluyen impuestos aplicables (IVA 13%).
- Toda compra genera un comprobante digital.
- El usuario debe proporcionar información veraz.
- Este sistema es una simulación con fines educativos.
""")

        # -------------------------
        # 🔒 PRIVACIDAD
        # -------------------------
        with st.expander("🔒 Política de Privacidad"):

            st.write("""
Nos comprometemos a proteger la información del usuario.

- No compartimos datos con terceros.
- La información se utiliza únicamente para fines del sistema.
- Cumplimos principios básicos de protección de datos personales.
""")

    # -------------------------
    # INFO LATERAL
    # -------------------------
    with col2:
        st.markdown("### 📍 Ubicación")
        st.info("Barrio Chino, San José")

        st.markdown("### 🕒 Horario")
        st.warning("Lunes a Domingo\n7:00 AM - 9:00 PM")

        st.markdown("### ☎ Contacto")
        st.success("2230-5698")

    st.divider()

    # -------------------------
    # MAPA
    # -------------------------
    st.subheader("📍 Encuéntranos")

    st.components.v1.iframe(
        "https://www.google.com/maps?q=Barrio+Chino+San+Jose+Costa+Rica&output=embed",
        height=350
    )

    st.divider()

    # -------------------------
    # FOOTER LEGAL (🔥 CLAVE)
    # -------------------------
    st.caption("""
© 2025 Pulpería El Dragón Dorado  

Este sistema constituye una simulación académica de comercio electrónico.  
No representa una plataforma oficial de facturación electrónica ante el Ministerio de Hacienda de Costa Rica.
""")