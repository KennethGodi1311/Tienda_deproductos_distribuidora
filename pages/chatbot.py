import streamlit as st

def chatbot():

    st.title("🤖 Asistente Virtual")
    st.caption("Pregúntame sobre productos, compras o ayuda")

    # -------------------------
    # SESSION STATE
    # -------------------------
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if "carrito" not in st.session_state:
        st.session_state["carrito"] = []

    if "mostrar_carrito" not in st.session_state:
        st.session_state["mostrar_carrito"] = False

    # -------------------------
    # UI CARRITO (MEJORADO)
    # -------------------------
    def mostrar_carrito_ui():

        st.subheader("🛒 Tu carrito")

        carrito = st.session_state["carrito"]

        if not carrito:
            st.info("Tu carrito está vacío")
            return

        total = 0

        for i, item in enumerate(carrito):

            col1, col2, col3, col4 = st.columns([3,1,1,1])

            with col1:
                st.markdown(f"**{item['producto'].capitalize()}**")
                st.caption(f"₡{item['precio']} c/u")

            with col2:
                nueva_cantidad = st.number_input(
                    "Cant",
                    min_value=1,
                    value=item["cantidad"],
                    key=f"cant_{i}"
                )
                item["cantidad"] = nueva_cantidad

            with col3:
                subtotal = item["precio"] * item["cantidad"]
                st.write(f"₡{subtotal}")
                total += subtotal

            with col4:
                if st.button("❌", key=f"del_{i}"):
                    st.session_state["carrito"].pop(i)
                    st.rerun()

            st.divider()

        # Guardar total global
        st.session_state["total"] = total

        st.success(f"💰 Total: ₡{total}")

        col1, col2, col3 = st.columns(3)

        # Vaciar carrito
        if col1.button("🧹 Vaciar carrito"):
            st.session_state["carrito"] = []
            st.rerun()

        # Volver
        if col2.button("🏠 Volver inicio"):
            st.session_state["page"] = "inicio"
            st.session_state["mostrar_carrito"] = False
            st.rerun()

        # Ir a pago REAL 🔥
        if col3.button("💳 Ir a pagar"):
            st.session_state["page"] = "pago"
            st.session_state["mostrar_carrito"] = False
            st.rerun()

    # -------------------------
    # RESPONDER
    # -------------------------
    def responder(pregunta):

        p = pregunta.lower()

        productos = {
            "arroz": 1000,
            "frijoles": 1200,
            "azucar": 900,
            "leche": 800,
            "pan": 500
        }

        # AGREGAR PRODUCTOS
        for nombre, precio in productos.items():
            if f"agregar {nombre}" in p:

                st.session_state["carrito"].append({
                    "producto": nombre,
                    "precio": precio,
                    "cantidad": 1
                })

                return f"🛒 {nombre.capitalize()} agregado al carrito"

        # MOSTRAR CARRITO
        if "carrito" in p:
            st.session_state["mostrar_carrito"] = True
            return "🛒 Abriendo carrito..."

        # TOTAL
        if "total" in p:
            total = sum(i["precio"] * i["cantidad"] for i in st.session_state["carrito"])
            return f"💰 Total actual: ₡{total}"

        # VACIAR
        if "vaciar" in p:
            st.session_state["carrito"] = []
            return "🧹 Carrito vaciado"

        # SALUDO
        if any(x in p for x in ["hola", "buenas", "hey"]):
            return "👋 Hola, puedes escribir 'carrito' para ver tu compra"

        # INFO
        if "producto" in p:
            return "🛒 Vendemos arroz, frijoles, leche, pan"

        if "oferta" in p:
            return "🔥 Hay descuentos disponibles hoy"

        if "horario" in p:
            return "🕒 7:00 AM - 9:00 PM"

        if "ayuda" in p:
            return """
Puedes escribir:
- agregar arroz
- agregar pan
- carrito
- total
- vaciar
"""

        return "🤖 No entendí, escribe 'ayuda'"

    # -------------------------
    # MOSTRAR CHAT
    # -------------------------
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # -------------------------
    # INPUT
    # -------------------------
    user_input = st.chat_input("Escribe tu mensaje...")

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
    # MOSTRAR CARRITO
    # -------------------------
    if st.session_state["mostrar_carrito"]:
        st.divider()
        mostrar_carrito_ui()

    # -------------------------
    # BOTONES EXTRA
    # -------------------------
    col1, col2 = st.columns(2)

    if col1.button("🧹 Limpiar chat"):
        st.session_state["chat_history"] = []
        st.rerun()

    if col2.button("🛒 Ver carrito"):
        st.session_state["mostrar_carrito"] = True
        st.rerun()