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
    # FOOTER
    # -------------------------
    col1, col2, col3 = st.columns(3)

    col1.info("📍 San José")
    col2.info("☎ 2230-5698")
    col3.info("📧 contacto@dragondorado.cr")

    st.markdown("---")
    st.caption("© 2025 Pulpería El Dragón Dorado")