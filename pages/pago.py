import streamlit as st
from datetime import datetime
from utils.factura import generar_factura
from database.db import guardar_venta

def pago():
    """
    Vista de pago del sistema.
    Permite confirmar la compra, guardar venta y generar factura PDF.
    """

    st.title("💳 Pago")

    # -------------------------
    # VALIDACIÓN: CARRITO VACÍO
    # -------------------------
    if "carrito" not in st.session_state or not st.session_state["carrito"]:
        st.warning("No hay productos en el carrito")

        if st.button("🛒 Ir a productos"):
            st.session_state["page"] = "productos"
            st.rerun()

        return

    # -------------------------
    # CALCULAR TOTAL REAL
    # -------------------------
    total = sum(
        item["precio"] * item["cantidad"]
        for item in st.session_state["carrito"]
    )

    # -------------------------
    # RESUMEN DE COMPRA
    # -------------------------
    st.subheader("🧾 Resumen de compra")

    for item in st.session_state["carrito"]:
        st.write(
            f"- {item['producto']} x{item['cantidad']} "
            f"→ ₡{item['precio'] * item['cantidad']}"
        )

    st.success(f"Total: ₡{total}")
    st.divider()

    # -------------------------
    # MÉTODO DE PAGO
    # -------------------------
    st.subheader("💳 Método de pago")

    metodo = st.selectbox("Selecciona cómo pagar", ["Tarjeta", "SINPE", "Efectivo"])

    # VARIABLES
    nombre = tarjeta = fecha = cvv = telefono = None

    # -------------------------
    # CAMPOS DINÁMICOS
    # -------------------------
    if metodo == "Tarjeta":

        st.markdown("### 💳 Pago con tarjeta")

        nombre = st.text_input("Nombre en la tarjeta")
        tarjeta = st.text_input("Número de tarjeta")
        fecha = st.text_input("Fecha expiración (MM/AA)")
        cvv = st.text_input("CVV", type="password")

    elif metodo == "SINPE":

        st.markdown("### 📱 Pago con SINPE")

        telefono = st.text_input("Número de teléfono SINPE")
        st.info("Se enviará una solicitud de pago al número indicado")

    elif metodo == "Efectivo":

        st.markdown("### 💵 Pago en efectivo")
        st.info("Pagarás al recibir el pedido")

    # -------------------------
    # CONFIRMAR PAGO
    # -------------------------
    if st.button("✅ Confirmar pago"):

        # VALIDACIONES SEGÚN MÉTODO
        if metodo == "Tarjeta":
            if not nombre or not tarjeta or not fecha or not cvv:
                st.error("Completa todos los datos de la tarjeta")
                return

        elif metodo == "SINPE":
            if not telefono:
                st.error("Ingresa el número SINPE")
                return

        with st.spinner("Procesando pago..."):

            # -------------------------
            # GUARDAR VENTA
            # -------------------------
            guardar_venta(st.session_state["carrito"])

            # -------------------------
            # GENERAR FACTURA
            # -------------------------
            generar_factura(st.session_state["carrito"], total)

            # -------------------------
            # MENSAJE SEGÚN MÉTODO
            # -------------------------
            if metodo == "Tarjeta":
                st.success("💳 Pago con tarjeta aprobado")

            elif metodo == "SINPE":
                st.success(f"📱 Solicitud SINPE enviada al {telefono}")

            elif metodo == "Efectivo":
                st.success("💵 Pedido registrado para pago en efectivo")

            st.balloons()

            # -------------------------
            # LIMPIAR CARRITO
            # -------------------------
            st.session_state["carrito"] = []
            st.session_state["ultima_compra"] = datetime.now()

            # -------------------------
            # DESCARGAR FACTURA
            # -------------------------
            with open("factura.pdf", "rb") as file:
                st.download_button(
                    label="📄 Descargar factura",
                    data=file,
                    file_name="factura.pdf",
                    mime="application/pdf"
                )

    # -------------------------
    # VOLVER
    # -------------------------
    if st.button("⬅ Volver al carrito"):
        st.session_state["page"] = "carrito"
        st.rerun()