import streamlit as st
import os
from PIL import Image

def inicio():

    st.title("🐉 Pulpería El Dragón Dorado")
    st.caption("Ofertas todos los días 🛒 | Rápido, cerca y confiable")

    st.divider()

    # -------------------------
    # SESSION
    # -------------------------
    if "categoria" not in st.session_state:
        st.session_state["categoria"] = "Todos"

    if "carrito" not in st.session_state:
        st.session_state["carrito"] = []

    # -------------------------
    # FUNCIÓN PARA NORMALIZAR IMÁGENES 🔥
    # -------------------------
    def cargar_imagen_uniforme(ruta, size=(300, 300)):
        try:
            img = Image.open(ruta).convert("RGB")
            img.thumbnail(size)

            fondo = Image.new("RGB", size, (255, 255, 255))
            offset = (
                (size[0] - img.size[0]) // 2,
                (size[1] - img.size[1]) // 2
            )
            fondo.paste(img, offset)
            return fondo
        except:
            return None

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
        {"nombre": "Arroz", "precio": 1500, "cat": "Abarrotes", "img": "arroz.jpg"},
        {"nombre": "Frijoles", "precio": 1200, "cat": "Abarrotes", "img": "frijoles.jpg"},
        {"nombre": "Azúcar", "precio": 900, "cat": "Abarrotes", "img": "azucar.jpg"},
        {"nombre": "Sal", "precio": 500, "cat": "Abarrotes", "img": "sal.jpg"},

        {"nombre": "Leche", "precio": 900, "cat": "Lacteos", "img": "leche.jpg"},
        {"nombre": "Queso", "precio": 1800, "cat": "Lacteos", "img": "queso.jpg"},
        {"nombre": "Yogurt", "precio": 700, "cat": "Lacteos", "img": "yogurt.jpg"},
        {"nombre": "Mantequilla", "precio": 1200, "cat": "Lacteos", "img": "mantequilla.jpg"},

        {"nombre": "Pan", "precio": 800, "cat": "Panaderia", "img": "pan.jpg"},
        {"nombre": "Queque", "precio": 1500, "cat": "Panaderia", "img": "queque.jpg"},
        {"nombre": "Galletas", "precio": 600, "cat": "Panaderia", "img": "galletas.jpg"},
        {"nombre": "Empanadas", "precio": 1000, "cat": "Panaderia", "img": "empanadas.jpg"},

        {"nombre": "Huevos", "precio": 2500, "cat": "Basicos", "img": "huevos.jpg"},
        {"nombre": "Aceite", "precio": 2200, "cat": "Basicos", "img": "aceite.jpg"},
        {"nombre": "Café", "precio": 3000, "cat": "Basicos", "img": "cafe.jpg"},
        {"nombre": "Atún", "precio": 1300, "cat": "Basicos", "img": "atun.jpg"},
    ]

    st.subheader("🛒 Productos")

    cols = st.columns(3)
    index = 0

    for p in productos:

        if st.session_state["categoria"] != "Todos" and p["cat"] != st.session_state["categoria"]:
            continue

        with cols[index % 3]:

            ruta = f"assets/productos/{p['img']}"

            if os.path.exists(ruta):
                img = cargar_imagen_uniforme(ruta)

                if img:
                    st.image(img, use_container_width=True)
                else:
                    st.warning("Error cargando imagen")
            else:
                st.warning(f"No existe {p['img']}")

            # CARD
            st.markdown(f"""
            <div style="
                background:#1e293b;
                padding:10px;
                border-radius:10px;
                text-align:center;
                margin-bottom:10px;
                height:140px;
            ">
                <h4>{p["nombre"]}</h4>
                <p style="font-size:18px;">💰 ₡{p["precio"]}</p>
                <small>{p["cat"]}</small>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🛒 Agregar", key=p["nombre"]):
                st.session_state["carrito"].append({
                    "producto": p["nombre"],
                    "precio": p["precio"],
                    "cantidad": 1
                })
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

    # -------------------------
    # ⚖️ AVISO LEGAL
    # -------------------------
    st.markdown("---")
    st.caption("""
    ⚖️ Las imágenes mostradas son de carácter ilustrativo.
    Este sistema es una simulación académica y no constituye una plataforma de comercio electrónico oficial conforme a la normativa del Ministerio de Hacienda de Costa Rica.
    """)