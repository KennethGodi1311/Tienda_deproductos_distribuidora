import streamlit as st
from database.db import (
    obtener_productos,
    agregar_producto,
    actualizar_producto,
    eliminar_producto
)

def inventario():

    st.title("📦 Gestión de Inventario")
    st.caption("Administra los productos de la tienda")

    # -------------------------
    # CARGAR PRODUCTOS
    # -------------------------
    productos = obtener_productos()

    if productos:
        st.subheader("📋 Productos actuales")

        for nombre, precio, stock in productos:

            with st.expander(f"{nombre} | ₡{precio} | Stock: {stock}"):

                col1, col2 = st.columns(2)

                with col1:
                    nuevo_precio = st.number_input(
                        "Precio",
                        min_value=0.0,
                        value=float(precio),
                        key=f"precio_{nombre}"
                    )

                    nuevo_stock = st.number_input(
                        "Stock",
                        min_value=0,
                        value=int(stock),
                        key=f"stock_{nombre}"
                    )

                with col2:

                    if st.button("💾 Actualizar", key=f"upd_{nombre}"):
                        actualizar_producto(nombre, nuevo_precio, nuevo_stock)
                        st.success("Producto actualizado")
                        st.rerun()

                    if st.button("🗑 Eliminar", key=f"del_{nombre}"):
                        eliminar_producto(nombre)
                        st.warning("Producto eliminado")
                        st.rerun()

    else:
        st.info("No hay productos registrados")

    st.divider()

    # -------------------------
    # AGREGAR PRODUCTO
    # -------------------------
    st.subheader("➕ Agregar nuevo producto")

    nombre = st.text_input("Nombre del producto")
    precio = st.number_input("Precio", min_value=0.0)
    stock = st.number_input("Stock inicial", min_value=0)

    if st.button("➕ Guardar producto"):

        if not nombre:
            st.error("El nombre es obligatorio")
            return

        ok = agregar_producto(nombre, precio, stock)

        if ok:
            st.success("Producto agregado correctamente")
            st.rerun()
        else:
            st.error("Ese producto ya existe")