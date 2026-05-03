import streamlit as st
import pandas as pd
from database.db import conectar

def ventas():
    """
    Vista de historial de ventas.
    Muestra todas las ventas registradas en la base de datos.
    """

    st.title("💰 Historial de Ventas")
    st.caption("Consulta todas las compras realizadas")

    # -------------------------
    # CARGAR DATOS
    # -------------------------
    conexion = conectar()
    df = pd.read_sql("SELECT * FROM ventas ORDER BY id DESC", conexion)
    conexion.close()

    if df.empty:
        st.warning("No hay ventas registradas")
        return

    # -------------------------
    # FORMATO FECHA
    # -------------------------
    if "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"])

    # -------------------------
    # MÉTRICAS
    # -------------------------
    total_ventas = len(df)
    ingresos = df["total"].sum()

    col1, col2 = st.columns(2)

    col1.metric("🧾 Total ventas", total_ventas)
    col2.metric("💰 Ingresos totales", f"₡{round(ingresos,2)}")

    st.divider()

    # -------------------------
    # FILTRO POR PRODUCTO
    # -------------------------
    productos = df["producto"].unique()
    filtro = st.selectbox("Filtrar por producto", ["Todos"] + list(productos))

    if filtro != "Todos":
        df = df[df["producto"] == filtro]

    # -------------------------
    # TABLA
    # -------------------------
    st.subheader("📋 Detalle de ventas")
    st.dataframe(df, use_container_width=True)

    # -------------------------
    # BOTÓN EXPORTAR
    # -------------------------
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Descargar CSV",
        data=csv,
        file_name="ventas.csv",
        mime="text/csv"
    )

    # -------------------------
    # VOLVER
    # -------------------------
    if st.button("⬅ Volver al inicio"):
        st.session_state["page"] = "inicio"
        st.rerun()