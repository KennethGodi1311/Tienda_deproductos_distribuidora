import streamlit as st
from datetime import datetime
from utils.factura import generar_factura
from database.db import guardar_venta


def pago():

    st.title("💳 Pago seguro")

    # -------------------------
    # VALIDACIÓN: CARRITO VACÍO
    # -------------------------
    if not st.session_state.get("carrito"):
        st.warning("🛒 No hay productos en el carrito")

        if st.button("Ir a productos"):
            st.session_state["page"] = "productos"
            st.rerun()
        return

    carrito = st.session_state["carrito"]

    # -------------------------
    # CÁLCULO
    # -------------------------
    subtotal = sum(item["precio"] * item["cantidad"] for item in carrito)
    iva = subtotal * 0.13
    total = subtotal + iva

    # -------------------------
    # RESUMEN
    # -------------------------
    st.subheader("🧾 Resumen de compra")

    for item in carrito:
        st.write(
            f"• {item['producto']} x{item['cantidad']} → ₡{item['precio'] * item['cantidad']}"
        )

    col1, col2, col3 = st.columns(3)
    col1.info(f"Subtotal: ₡{round(subtotal, 2)}")
    col2.info(f"IVA (13%): ₡{round(iva, 2)}")
    col3.success(f"Total: ₡{round(total, 2)}")

    # 🔥 AVISO LEGAL
    st.caption("⚖️ El total incluye IVA conforme a la normativa tributaria vigente en Costa Rica.")

    st.divider()

    # -------------------------
    # MÉTODO DE PAGO
    # -------------------------
    st.subheader("💳 Método de pago")

    metodo = st.selectbox(
        "Selecciona cómo pagar",
        ["Tarjeta", "SINPE", "Efectivo"]
    )

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
        telefono = st.text_input("Número de teléfono")
        st.info("Se enviará una solicitud de pago al número")

    elif metodo == "Efectivo":
        st.markdown("### 💵 Pago en efectivo")
        st.info("Pagarás al recibir el pedido")

    st.divider()

    # -------------------------
    # 📜 TÉRMINOS Y CONSENTIMIENTO (🔥 CLAVE)
    # -------------------------
    with st.expander("📜 Términos y condiciones"):
        st.write("""
- La compra genera un comprobante digital.
- Los precios incluyen impuestos aplicables.
- No se realizan devoluciones sin factura.
- Este sistema es una simulación académica.
""")

    acepta = st.checkbox("Acepto los términos y condiciones")

    st.caption("🔒 Tus datos están protegidos y no serán compartidos con terceros.")

    # -------------------------
    # BOTÓN DE PAGO
    # -------------------------
    if st.button("✅ Confirmar pago", use_container_width=True):

        # 🔥 VALIDACIÓN LEGAL
        if not acepta:
            st.error("Debes aceptar los términos y condiciones")
            return

        # VALIDACIONES
        if metodo == "Tarjeta":
            if not all([nombre, tarjeta, fecha, cvv]):
                st.error("Completa todos los datos de la tarjeta")
                return

        elif metodo == "SINPE":
            if not telefono:
                st.error("Ingresa el número SINPE")
                return

        # -------------------------
        # PROCESO
        # -------------------------
        with st.spinner("Procesando pago..."):

            try:
                guardar_venta(carrito)
                generar_factura(carrito, total, metodo)

                # MENSAJES
                if metodo == "Tarjeta":
                    st.success("💳 Pago aprobado correctamente")

                elif metodo == "SINPE":
                    st.success(f"📱 Solicitud enviada al {telefono}")

                elif metodo == "Efectivo":
                    st.success("💵 Pedido registrado para pago contra entrega")

                st.balloons()

                st.session_state["ultima_compra"] = datetime.now()
                st.session_state["carrito"] = []

                # DESCARGA
                try:
                    with open("factura.pdf", "rb") as file:
                        st.download_button(
                            label="📄 Descargar factura",
                            data=file,
                            file_name="factura.pdf",
                            mime="application/pdf"
                        )
                except:
                    st.warning("Factura generada pero no se pudo descargar")

            except Exception as e:
                st.error(f"Error en el proceso: {e}")

    # -------------------------
    # VOLVER
    # -------------------------
    if st.button("⬅ Volver al carrito"):
        st.session_state["page"] = "carrito"
        st.rerun()