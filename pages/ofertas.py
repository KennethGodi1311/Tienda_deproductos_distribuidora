import streamlit as st

def ofertas():

    st.title("🔥 Ofertas especiales")

    # -------------------------
    # ESTADO
    # -------------------------
    if "carrito" not in st.session_state:
        st.session_state["carrito"] = []

    # -------------------------
    # FILTRO
    # -------------------------
    filtro = st.selectbox("Filtrar por descuento", ["Todos", "10%", "20%"])

    # -------------------------
    # LISTA
    # -------------------------
    lista = [
        {"nombre": "Leche", "precio": 800, "desc": 10},
        {"nombre": "Pan", "precio": 500, "desc": 20},
        {"nombre": "Queso", "precio": 1800, "desc": 15},
        {"nombre": "Arroz", "precio": 1500, "desc": 5},
    ]

    st.divider()

    # -------------------------
    # GRID
    # -------------------------
    cols = st.columns(2)
    index = 0

    for o in lista:

        # FILTRO
        if filtro != "Todos" and f"{o['desc']}%" != filtro:
            continue

        precio_original = o["precio"]
        descuento = o["desc"]
        final = int(precio_original - (precio_original * descuento / 100))

        with cols[index % 2]:

            st.markdown(f"""
            <div style="
                background:#1e293b;
                padding:15px;
                border-radius:12px;
                border:1px solid #334155;
                margin-bottom:15px;
            ">
                <h4>{o["nombre"]}</h4>
                <p style="text-decoration:line-through;color:#94a3b8;">
                    ₡{precio_original}
                </p>
                <h3 style="color:#22c55e;">₡{final}</h3>
                <p>🔥 {descuento}% descuento</p>
            </div>
            """, unsafe_allow_html=True)

            # -------------------------
            # CANTIDAD
            # -------------------------
            cantidad = st.number_input(
                f"Cantidad {o['nombre']}",
                min_value=1,
                max_value=20,
                value=1,
                key=f"cant_{o['nombre']}"
            )

            # -------------------------
            # BOTÓN
            # -------------------------
            if st.button(f"🛒 Agregar {o['nombre']}", key=o["nombre"]):

                st.session_state["carrito"].append({
                    "producto": o["nombre"],
                    "precio": final,
                    "cantidad": cantidad
                })

                st.success(f"{o['nombre']} agregado al carrito ✔️")

        index += 1

    # -------------------------
    # RESUMEN CARRITO
    # -------------------------
    st.divider()
    st.subheader("🛒 Resumen rápido")

    total = sum(item["precio"] * item["cantidad"] for item in st.session_state["carrito"])

    col1, col2 = st.columns(2)

    col1.info(f"Productos: {len(st.session_state['carrito'])}")
    col2.success(f"Total: ₡{total}")

    # -------------------------
    # BOTÓN LIMPIAR
    # -------------------------
    if st.button("🧹 Vaciar carrito"):
        st.session_state["carrito"] = []
        st.success("Carrito limpio")