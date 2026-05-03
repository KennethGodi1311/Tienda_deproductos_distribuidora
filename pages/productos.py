import streamlit as st
import os
from PIL import Image

def productos():

    st.title("🛍️ Productos")

    # -------------------------
    # SESSION
    # -------------------------
    if "carrito" not in st.session_state:
        st.session_state["carrito"] = []

    # -------------------------
    # 🔥 FUNCIÓN IMAGEN UNIFORME
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
    # 🔐 AVISO LEGAL
    # -------------------------
    with st.expander("⚖️ Información legal y condiciones de compra"):
        st.markdown("""
        **Protección al consumidor (Costa Rica)**  

        - Todos los precios incluyen impuestos según la normativa vigente (IVA 13%).
        - Los productos están sujetos a disponibilidad.
        - El cliente tiene derecho a recibir factura por su compra.
        - No se aceptan devoluciones en productos perecederos.
        - Al comprar, usted acepta nuestros términos y condiciones.

        📌 *Cumplimiento de la Ley 7472.*
        """)

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
    # PRODUCTOS CON IMAGEN
    # -------------------------
    lista = [
        {"nombre": "Arroz", "precio": 1000, "cat": "Abarrotes", "img": "arroz.jpg"},
        {"nombre": "Frijoles", "precio": 1200, "cat": "Abarrotes", "img": "frijoles.jpg"},
        {"nombre": "Azúcar", "precio": 900, "cat": "Abarrotes", "img": "azucar.jpg"},
        {"nombre": "Leche", "precio": 800, "cat": "Lácteos", "img": "leche.jpg"},
        {"nombre": "Queso", "precio": 1800, "cat": "Lácteos", "img": "queso.jpg"},
        {"nombre": "Pan", "precio": 500, "cat": "Panadería", "img": "pan.jpg"},
        {"nombre": "Galletas", "precio": 600, "cat": "Panadería", "img": "galletas.jpg"},
    ]

    st.divider()

    # -------------------------
    # GRID
    # -------------------------
    cols = st.columns(3)
    index = 0

    for p in lista:

        if categoria != "Todos" and p["cat"] != categoria:
            continue

        if busqueda and busqueda.lower() not in p["nombre"].lower():
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
                background:#0f172a;
                padding:12px;
                border-radius:12px;
                border:1px solid #334155;
                margin-bottom:10px;
                text-align:center;
                height:140px;
            ">
                <h4>{p["nombre"]}</h4>
                <p style="font-size:18px;color:#22c55e;">₡{p["precio"]}</p>
                <small style="color:#94a3b8;">{p["cat"]}</small>
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

                st.toast(f"{p['nombre']} agregado al carrito 🛒")

        index += 1

    # -------------------------
    # RESUMEN CARRITO
    # -------------------------
    st.divider()
    st.subheader("🛒 Resumen")

    total = sum(item["precio"] * item["cantidad"] for item in st.session_state["carrito"])

    col1, col2 = st.columns(2)
    col1.metric("Productos", len(st.session_state["carrito"]))
    col2.metric("Total", f"₡{total}")

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

    # -------------------------
    # 📜 DISCLAIMER FINAL
    # -------------------------
    st.markdown("---")
    st.caption("""
    ⚖️ Los precios pueden variar sin previo aviso.  
    📄 Factura disponible al finalizar la compra.  
    🛡️ Sitio protegido para transacciones seguras.
    """)