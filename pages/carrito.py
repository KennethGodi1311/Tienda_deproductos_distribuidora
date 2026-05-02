import streamlit as st

def carrito():
    """
    Vista principal del carrito de compras.
    Permite visualizar productos, modificar cantidades,
    eliminar elementos y proceder al pago.
    """

    # Título de la página
    st.title("🛒 Carrito de compras")

    # Inicializar carrito si no existe
    if "carrito" not in st.session_state:
        st.session_state["carrito"] = []

    carrito = st.session_state["carrito"]

    # -------------------------
    # VALIDACIÓN: CARRITO VACÍO
    # -------------------------
    if not carrito:
        st.info("Tu carrito está vacío")

        # Botón para volver al inicio
        if st.button("🏠 Volver a inicio"):
            st.session_state["page"] = "inicio"
            st.rerun()

        return

    total = 0  # acumulador del total

    # -------------------------
    # LISTADO DE PRODUCTOS
    # -------------------------
    for i, item in enumerate(carrito):

        # Layout en columnas
        col1, col2, col3, col4 = st.columns([3,1,1,1])

        # Nombre y precio
        with col1:
            st.markdown(f"### {item['producto'].capitalize()}")
            st.caption(f"Precio unitario: ₡{item['precio']}")

        # Cantidad editable
        with col2:
            cantidad = st.number_input(
                "Cantidad",
                min_value=1,
                value=item["cantidad"],
                key=f"cant_{i}"
            )
            item["cantidad"] = cantidad

        # Subtotal
        with col3:
            subtotal = item["precio"] * item["cantidad"]
            st.write(f"₡{subtotal}")
            total += subtotal

        # Eliminar producto
        with col4:
            if st.button("❌", key=f"delete_{i}"):
                carrito.pop(i)
                st.rerun()

        st.divider()

    # -------------------------
    # TOTAL GENERAL
    # -------------------------
    st.success(f"💰 Total a pagar: ₡{total}")

    # -------------------------
    # ACCIONES
    # -------------------------
    col1, col2, col3 = st.columns(3)

    # Vaciar carrito
    with col1:
        if st.button("🧹 Vaciar carrito"):
            st.session_state["carrito"] = []
            st.rerun()

    # Volver a productos
    with col2:
        if st.button("🏠 Seguir comprando"):
            st.session_state["page"] = "productos"
            st.rerun()

    # Ir a pago
    with col3:
        if st.button("💳 Ir a pagar"):
            st.session_state["total"] = total
            st.session_state["page"] = "pago"
            st.rerun()