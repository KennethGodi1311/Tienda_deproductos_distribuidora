import streamlit as st

def productos():

    st.title("🛍️ Productos")

    # -------------------------
    # SESSION
    # -------------------------
    if "carrito" not in st.session_state:
        st.session_state["carrito"] = []

    # -------------------------
    # BUSCADOR
    # -------------------------
    busqueda = st.text_input("🔍 Buscar producto")

    # -------------------------
    # CATEGORÍAS
    # -------------------------
    categoria = st.selectbox(
        "Filtrar por categoría",
        ["Todos", "Abarrotes", "Lácteos", "Panadería"]
    )

    # -------------------------
    # LISTA DE PRODUCTOS
    # -------------------------
    lista = [
        {"nombre": "Arroz", "precio": 1000, "cat": "Abarrotes"},
        {"nombre": "Frijoles", "precio": 1200, "cat": "Abarrotes"},
        {"nombre": "Azúcar", "precio": 900, "cat": "Abarrotes"},
        {"nombre": "Leche", "precio": 800, "cat": "Lácteos"},
        {"nombre": "Queso", "precio": 1800, "cat": "Lácteos"},
        {"nombre": "Pan", "precio": 500, "cat": "Panadería"},
        {"nombre": "Galletas", "precio": 600, "cat": "Panadería"},
    ]

    st.divider()

    # -------------------------
    # GRID
    # -------------------------
    cols = st.columns(3)
    index = 0

    for p in lista:

        # FILTRO POR CATEGORÍA
        if categoria != "Todos" and p["cat"] != categoria:
            continue

        # FILTRO POR BÚSQUEDA
        if busqueda and busqueda.lower() not in p["nombre"].lower():
            continue

        with cols[index % 3]:

            st.markdown(f"""
            <div style="
                background:#1e293b;
                padding:15px;
                border-radius:12px;
                border:1px solid #334155;
                margin-bottom:15px;
            ">
                <h4>{p["nombre"]}</h4>
                <p>💰 ₡{p["precio"]}</p>
                <small>{p["cat"]}</small>
            </div>
            """, unsafe_allow_html=True)

            # -------------------------
            # CANTIDAD
            # -------------------------
            cantidad = st.number_input(
                f"Cantidad {p['nombre']}",
                min_value=1,
                max_value=20,
                value=1,
                key=f"prod_{p['nombre']}"
            )

            # -------------------------
            # BOTÓN
            # -------------------------
            if st.button(f"🛒 Agregar", key=f"btn_{p['nombre']}"):

                st.session_state["carrito"].append({
                    "producto": p["nombre"],
                    "precio": p["precio"],
                    "cantidad": cantidad
                })

                st.success(f"{p['nombre']} agregado ✔️")

        index += 1

    # -------------------------
    # RESUMEN CARRITO
    # -------------------------
    st.divider()
    st.subheader("🛒 Resumen")

    total = sum(item["precio"] * item["cantidad"] for item in st.session_state["carrito"])

    col1, col2 = st.columns(2)

    col1.info(f"Productos: {len(st.session_state['carrito'])}")
    col2.success(f"Total: ₡{total}")

    # -------------------------
    # BOTONES
    # -------------------------
    col1, col2 = st.columns(2)

    if col1.button("🧹 Vaciar carrito"):
        st.session_state["carrito"] = []
        st.success("Carrito limpio")

    if col2.button("➡️ Ir al carrito"):
        st.session_state["page"] = "carrito"
        st.rerun()