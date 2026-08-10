import base64
from io import BytesIO
import os
from PIL import Image
import streamlit as st


def inicio():
    st.title("🐉 Pulpería El Dragón Dorado")
    st.caption("Ofertas todos los días 🛒 | Rápido, cerca y confiable")

    # -------------------------
    # CSS PARAS TARJETAS E IMÁGENES COMPACTAS
    # -------------------------
    st.markdown(
        """
    <style>
        .product-card {
            background: #1e293b;
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 12px;
            padding: 10px;
            text-align: center;
            margin-bottom: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .product-img {
            width: 100%;
            height: 120px !important;  /* Altura fija compacta */
            object-fit: contain !important;
            border-radius: 8px;
            background-color: #0f172a;
            margin-bottom: 8px;
            padding: 4px;
        }

        .product-title {
            color: #f8fafc;
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 2px;
        }

        .product-price {
            color: #38bdf8;
            font-size: 1.1rem;
            font-weight: 800;
            margin-bottom: 2px;
        }

        .product-cat {
            color: #94a3b8;
            font-size: 0.75rem;
            text-transform: uppercase;
        }

        /* Botón estilizado al ancho de la columna */
        div[data-testid="stColumn"] .stButton > button {
            width: 100% !important;
            border-radius: 8px !important;
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            border: none !important;
        }
        div[data-testid="stColumn"] .stButton > button:hover {
            background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.divider()

    # -------------------------
    # SESSION
    # -------------------------
    if "categoria" not in st.session_state:
        st.session_state["categoria"] = "Todos"

    if "carrito" not in st.session_state:
        st.session_state["carrito"] = []

    # -------------------------
    # FUNCIÓN PARA CONVERTIR IMAGEN A BASE64
    # -------------------------
    def obtener_img_base64(ruta):
        try:
            if os.path.exists(ruta):
                img = Image.open(ruta).convert("RGB")
                buffered = BytesIO()
                img.save(buffered, format="JPEG", quality=85)
                return base64.b64encode(buffered.getvalue()).decode()
        except:
            pass
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
        {
            "nombre": "Arroz",
            "precio": 1500,
            "cat": "Abarrotes",
            "img": "arroz.jpg",
        },
        {
            "nombre": "Frijoles",
            "precio": 1200,
            "cat": "Abarrotes",
            "img": "frijoles.jpg",
        },
        {
            "nombre": "Azúcar",
            "precio": 900,
            "cat": "Abarrotes",
            "img": "azucar.jpg",
        },
        {"nombre": "Sal", "precio": 500, "cat": "Abarrotes", "img": "sal.jpg"},
        {"nombre": "Leche", "precio": 900, "cat": "Lacteos", "img": "leche.jpg"},
        {"nombre": "Queso", "precio": 1800, "cat": "Lacteos", "img": "queso.jpg"},
        {"nombre": "Yogurt", "precio": 700, "cat": "Lacteos", "img": "yogurt.jpg"},
        {
            "nombre": "Mantequilla",
            "precio": 1200,
            "cat": "Lacteos",
            "img": "mantequilla.jpg",
        },
        {"nombre": "Pan", "precio": 800, "cat": "Panaderia", "img": "pan.jpg"},
        {
            "nombre": "Queque",
            "precio": 1500,
            "cat": "Panaderia",
            "img": "queque.jpg",
        },
        {
            "nombre": "Galletas",
            "precio": 600,
            "cat": "Panaderia",
            "img": "galletas.jpg",
        },
        {
            "nombre": "Empanadas",
            "precio": 1000,
            "cat": "Panaderia",
            "img": "empanadas.jpg",
        },
        {
            "nombre": "Huevos",
            "precio": 2500,
            "cat": "Basicos",
            "img": "huevos.jpg",
        },
        {
            "nombre": "Aceite",
            "precio": 2200,
            "cat": "Basicos",
            "img": "aceite.jpg",
        },
        {"nombre": "Café", "precio": 3000, "cat": "Basicos", "img": "cafe.jpg"},
        {"nombre": "Atún", "precio": 1300, "cat": "Basicos", "img": "atun.jpg"},
    ]

    st.subheader("🛒 Productos")

    # 4 Columnas para aprovechar bien la pantalla en Desktop
    cols = st.columns(4)
    index = 0

    for p in productos:
        if (
            st.session_state["categoria"] != "Todos"
            and p["cat"] != st.session_state["categoria"]
        ):
            continue

        with cols[index % 4]:
            ruta = f"assets/productos/{p['img']}"
            img_b64 = obtener_img_base64(ruta)

            # HTML de la imagen integrada en la tarjeta
            if img_b64:
                img_html = f'<img src="data:image/jpeg;base64,{img_b64}" class="product-img">'
            else:
                img_html = '<div class="product-img" style="display:flex; align-items:center; justify-content:center; color:#64748b;">📷 Sin Foto</div>'

            # TARJETA COMPLETA
            st.markdown(
                f"""
            <div class="product-card">
                {img_html}
                <div class="product-title">{p["nombre"]}</div>
                <div class="product-price">₡{p["precio"]}</div>
                <div class="product-cat">{p["cat"]}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Botón inmediatamente abajo
            if st.button("🛒 Agregar", key=f"btn_{p['nombre']}"):
                st.session_state["carrito"].append(
                    {
                        "producto": p["nombre"],
                        "precio": p["precio"],
                        "cantidad": 1,
                    }
                )
                st.toast(f"✔️ {p['nombre']} agregado", icon="🛒")

        index += 1

    # -------------------------
    # OFERTAS E INFO
    # -------------------------
    st.divider()
    st.subheader("🔥 Ofertas del día")

    col1, col2 = st.columns(2)
    col1.success("🍚 Arroz ₡1200")
    col2.warning("🥖 Pan ₡600")

    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.info("📍 Barrio Chino, San José")
    col2.info("☎ 2230-5698")
    col3.info("🕒 7:00 AM - 9:00 PM")

    st.markdown("---")
    st.caption("""
    ⚖️ Las imágenes mostradas son de carácter ilustrativo.
    Este sistema es una simulación académica y no constituye una plataforma de comercio electrónico oficial conforme a la normativa del Ministerio de Hacienda de Costa Rica.
    """)