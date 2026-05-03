import streamlit as st

def chatbot():

    st.title("🤖 Asistente Inteligente")
    st.caption("Sistema guiado de compra con cumplimiento legal")

    # -------------------------
    # SESSION
    # -------------------------
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if "carrito" not in st.session_state:
        st.session_state["carrito"] = []

    if "bot_estado" not in st.session_state:
        st.session_state["bot_estado"] = "inicio"

    if "acepta_terminos" not in st.session_state:
        st.session_state["acepta_terminos"] = False

    # -------------------------
    # FUNCIONES
    # -------------------------
    def ir(pagina):
        st.session_state["page"] = pagina
        st.rerun()

    def agregar_producto(nombre, precio):
        st.session_state["carrito"].append({
            "producto": nombre,
            "precio": precio,
            "cantidad": 1
        })

    # -------------------------
    # UI BOT
    # -------------------------
    def bot_ui():

        estado = st.session_state["bot_estado"]

        # -------------------------
        # INICIO
        # -------------------------
        if estado == "inicio":

            st.info("👋 Bienvenido al sistema de compras")

            with st.expander("⚖️ Información legal importante"):
                st.markdown("""
                **Derechos del consumidor (Costa Rica)**

                - Precios incluyen IVA (13%)
                - Derecho a recibir factura
                - Información clara antes de comprar
                - Protección según Ley 7472

                Al continuar, aceptas las condiciones del sistema.
                """)

            col1, col2 = st.columns(2)

            if col1.button("🛍️ Comprar"):
                st.session_state["bot_estado"] = "comprar"
                st.rerun()

            if col2.button("🔐 Iniciar sesión"):
                st.session_state["auth_view"] = "login"
                st.rerun()

            if st.button("📝 Crear cuenta"):
                st.session_state["auth_view"] = "registro"
                st.rerun()

        # -------------------------
        # COMPRAR
        # -------------------------
        elif estado == "comprar":

            st.success("🛒 Selecciona productos")

            productos = {
                "Arroz": 1000,
                "Frijoles": 1200,
                "Leche": 800,
                "Pan": 500
            }

            for nombre, precio in productos.items():

                col1, col2 = st.columns([3,1])

                with col1:
                    st.write(f"{nombre} - ₡{precio}")

                with col2:
                    if st.button(f"Agregar {nombre}"):
                        agregar_producto(nombre, precio)
                        st.toast(f"{nombre} agregado 🛒")

            st.divider()

            if st.button("🛒 Ver carrito"):
                st.session_state["bot_estado"] = "carrito"
                st.rerun()

        # -------------------------
        # CARRITO
        # -------------------------
        elif estado == "carrito":

            st.subheader("🛒 Carrito de compra")

            carrito = st.session_state["carrito"]

            if not carrito:
                st.warning("Carrito vacío")
                st.session_state["bot_estado"] = "comprar"
                st.rerun()

            total = 0

            for item in carrito:
                subtotal = item["precio"] * item["cantidad"]
                total += subtotal
                st.write(f"{item['producto']} x{item['cantidad']} → ₡{subtotal}")

            iva = total * 0.13
            total_final = total + iva

            st.info(f"Subtotal: ₡{total}")
            st.info(f"IVA (13%): ₡{round(iva,2)}")
            st.success(f"Total final: ₡{round(total_final,2)}")

            # -------------------------
            # ⚖️ ACEPTACIÓN LEGAL
            # -------------------------
            st.divider()
            st.markdown("### ⚖️ Confirmación legal")

            st.session_state["acepta_terminos"] = st.checkbox(
                "Acepto los términos, condiciones y política de compra"
            )

            with st.expander("Ver términos legales"):
                st.markdown("""
                - Compra sujeta a disponibilidad
                - No devoluciones en productos perecederos
                - Factura será generada automáticamente
                - Pago implica aceptación contractual

                📌 Ley 7472 - Protección al consumidor
                """)

            # -------------------------
            # ACCIONES
            # -------------------------
            col1, col2, col3 = st.columns(3)

            if col1.button("➕ Seguir comprando"):
                st.session_state["bot_estado"] = "comprar"
                st.rerun()

            if col2.button("🧹 Vaciar"):
                st.session_state["carrito"] = []
                st.rerun()

            if col3.button("💳 Ir a pagar"):

                if not st.session_state["acepta_terminos"]:
                    st.error("⚠️ Debes aceptar los términos legales")
                    return

                ir("pago")

        # -------------------------
        # FOOTER LEGAL
        # -------------------------
        st.divider()
        st.caption("""
        ⚖️ Sistema con cumplimiento básico de normativa comercial  
        🛡️ Protección de datos simulada  
        📄 Facturación disponible
        """)

    # -------------------------
    # RESPUESTAS INTELIGENTES
    # -------------------------
    def responder(texto):

        t = texto.lower()

        if "derecho" in t or "legal" in t:
            return "⚖️ Este sistema cumple con normativa básica de protección al consumidor"

        if "comprar" in t:
            st.session_state["bot_estado"] = "comprar"
            return "🛍️ Vamos a comprar"

        if "carrito" in t:
            st.session_state["bot_estado"] = "carrito"
            return "🛒 Mostrando carrito"

        if "pagar" in t:
            if not st.session_state.get("acepta_terminos"):
                return "⚠️ Debes aceptar los términos antes de pagar"
            st.session_state["page"] = "pago"
            return "💳 Redirigiendo a pago"

        if "factura" in t:
            return "🧾 Se genera automáticamente al completar la compra"

        return "🤖 Usa los botones para continuar"

    # -------------------------
    # CHAT
    # -------------------------
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Escribe aquí...")

    if user_input:

        st.session_state["chat_history"].append({
            "role": "user",
            "content": user_input
        })

        respuesta = responder(user_input)

        st.session_state["chat_history"].append({
            "role": "assistant",
            "content": respuesta
        })

        st.rerun()

    # -------------------------
    # UI
    # -------------------------
    st.divider()
    bot_ui()

    # -------------------------
    # BOTONES EXTRA
    # -------------------------
    col1, col2 = st.columns(2)

    if col1.button("🧹 Limpiar chat"):
        st.session_state["chat_history"] = []
        st.rerun()

    if col2.button("🔄 Reiniciar asistente"):
        st.session_state["bot_estado"] = "inicio"
        st.rerun()