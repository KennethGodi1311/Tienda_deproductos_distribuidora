import streamlit as st

def inicio():

    st.title("🐉 Pulpería El Dragón Dorado")
    st.caption("Ofertas todos los días 🛒 | Rápido, cerca y confiable")

    st.divider()

    # Estado categoría
    if "categoria" not in st.session_state:
        st.session_state["categoria"] = "Todos"

    # -------------------------
    # CATEGORÍAS
    # -------------------------
    st.subheader("🧭 Categorías")

    col1, col2, col3, col4, col5 = st.columns(5)

    if col1.button("🥫 Abarrotes"):
        st.session_state["categoria"] = "Abarrotes"

    if col2.button("🥛 Lácteos"):
        st.session_state["categoria"] = "Lacteos"

    if col3.button("🥖 Panadería"):
        st.session_state["categoria"] = "Panaderia"

    if col4.button("🍳 Básicos"):
        st.session_state["categoria"] = "Basicos"

    if col5.button("🔄 Todos"):
        st.session_state["categoria"] = "Todos"

    st.info(f"Mostrando: {st.session_state['categoria']}")

    st.divider()

    # -------------------------
    # PRODUCTOS
    # -------------------------
    productos = [
        {"nombre": "Arroz", "precio": 1500, "cat": "Abarrotes"},
        {"nombre": "Frijoles", "precio": 1200, "cat": "Abarrotes"},
        {"nombre": "Azúcar", "precio": 900, "cat": "Abarrotes"},
        {"nombre": "Sal", "precio": 500, "cat": "Abarrotes"},

        {"nombre": "Leche", "precio": 900, "cat": "Lacteos"},
        {"nombre": "Queso", "precio": 1800, "cat": "Lacteos"},
        {"nombre": "Yogurt", "precio": 700, "cat": "Lacteos"},
        {"nombre": "Mantequilla", "precio": 1200, "cat": "Lacteos"},

        {"nombre": "Pan", "precio": 800, "cat": "Panaderia"},
        {"nombre": "Queque", "precio": 1500, "cat": "Panaderia"},
        {"nombre": "Galletas", "precio": 600, "cat": "Panaderia"},
        {"nombre": "Empanadas", "precio": 1000, "cat": "Panaderia"},

        {"nombre": "Huevos", "precio": 2500, "cat": "Basicos"},
        {"nombre": "Aceite", "precio": 2200, "cat": "Basicos"},
        {"nombre": "Café", "precio": 3000, "cat": "Basicos"},
        {"nombre": "Atún", "precio": 1300, "cat": "Basicos"},
    ]

    st.subheader("🛒 Productos")

    cols = st.columns(3)
    index = 0

    for p in productos:

        if st.session_state["categoria"] != "Todos" and p["cat"] != st.session_state["categoria"]:
            continue

        with cols[index % 3]:
            st.markdown(f"""
            <div class="card">
                <h4>{p["nombre"]}</h4>
                <p>💰 ₡{p["precio"]}</p>
                <small>{p["cat"]}</small>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Comprar", key=p["nombre"]):
                st.success(f"{p['nombre']} agregado ✔️")

        index += 1

    # -------------------------
    # OFERTAS
    # -------------------------
    st.divider()
    st.subheader("🔥 Ofertas del día")

    col1, col2 = st.columns(2)
    col1.success("🍚 Arroz ₡1200")
    col2.warning("🥖 Pan ₡600")

    # -------------------------
    # INFO
    # -------------------------
    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.info("📍 Barrio Chino, San José")
    col2.info("☎ 2230-5698")
    col3.info("🕒 7:00 AM - 9:00 PM")