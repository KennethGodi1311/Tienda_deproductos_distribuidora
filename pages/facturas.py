import streamlit as st
import pandas as pd
from database.db import conectar


def facturas():
    """
    Vista de historial de facturas.
    Muestra todas las compras realizadas por el usuario.
    """

    st.title("🧾 Historial de Facturas")

    # -------------------------
    # CARGAR DATOS
    # -------------------------
    conexion = conectar()

    try:
        df = pd.read_sql("SELECT * FROM ventas ORDER BY fecha DESC", conexion)
    except:
        st.error("Error cargando las facturas")
        return
    finally:
        conexion.close()

    # -------------------------
    # VALIDACIÓN
    # -------------------------
    if df.empty:
        st.warning("No hay facturas registradas")
        return

    # -------------------------
    # FILTROS
    # -------------------------
    st.subheader("🔎 Filtros")

    fecha_min = df["fecha"].min()
    fecha_max = df["fecha"].max()

    col1, col2 = st.columns(2)

    with col1:
        desde = st.date_input("Desde", pd.to_datetime(fecha_min))

    with col2:
        hasta = st.date_input("Hasta", pd.to_datetime(fecha_max))

    df["fecha"] = pd.to_datetime(df["fecha"])

    df_filtrado = df[
        (df["fecha"] >= pd.to_datetime(desde)) &
        (df["fecha"] <= pd.to_datetime(hasta))
    ]

    # -------------------------
    # TABLA
    # -------------------------
    st.subheader("📊 Facturas registradas")

    st.dataframe(df_filtrado, use_container_width=True)

    # -------------------------
    # RESUMEN
    # -------------------------
    total_general = df_filtrado["total"].sum()
    cantidad_ventas = len(df_filtrado)

    col1, col2 = st.columns(2)
    col1.metric("💰 Total vendido", f"₡{round(total_general,2)}")
    col2.metric("🧾 Cantidad de ventas", cantidad_ventas)

    st.divider()

    # -------------------------
    # DETALLE POR PRODUCTO
    # -------------------------
    st.subheader("📦 Ventas por producto")

    resumen = df_filtrado.groupby("producto")["total"].sum()

    st.bar_chart(resumen)

    # -------------------------
    # DESCARGA GLOBAL (CSV)
    # -------------------------
    st.download_button(
        label="📥 Descargar reporte CSV",
        data=df_filtrado.to_csv(index=False),
        file_name="reporte_ventas.csv",
        mime="text/csv"
    )