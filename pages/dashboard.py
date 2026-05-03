import streamlit as st
import pandas as pd
from database.db import conectar
import matplotlib.pyplot as plt

def dashboard():

    st.title("📊 Dashboard de ventas")
    st.caption("Análisis general de ingresos y productos")

    # -------------------------
    # CARGAR DATOS
    # -------------------------
    conexion = conectar()

    try:
        df = pd.read_sql("SELECT * FROM ventas", conexion)
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return
    finally:
        conexion.close()

    if df.empty:
        st.warning("📭 No hay ventas aún")
        return

    # -------------------------
    # LIMPIEZA DATOS
    # -------------------------
    try:
        df["fecha"] = pd.to_datetime(df["fecha"])
    except:
        st.error("Error procesando fechas")
        return

    df = df.dropna()

    # -------------------------
    # FILTRO FECHA
    # -------------------------
    st.subheader("📅 Filtro por fecha")

    fecha_min = df["fecha"].min()
    fecha_max = df["fecha"].max()

    rango = st.date_input(
        "Selecciona rango",
        [fecha_min, fecha_max]
    )

    if len(rango) == 2:
        df = df[
            (df["fecha"] >= pd.to_datetime(rango[0])) &
            (df["fecha"] <= pd.to_datetime(rango[1]))
        ]

    # 🔥 VALIDACIÓN CLAVE
    if df.empty:
        st.warning("⚠️ No hay ventas en ese rango de fechas")
        return

    # -------------------------
    # MÉTRICAS
    # -------------------------
    total_ventas = len(df)
    ingresos = df["total"].sum()
    ticket_promedio = ingresos / total_ventas if total_ventas > 0 else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("🧾 Ventas", total_ventas)
    col2.metric("💰 Ingresos", f"₡{round(ingresos,2)}")
    col3.metric("📊 Ticket Promedio", f"₡{round(ticket_promedio,2)}")

    st.divider()

    # -------------------------
    # TABLA
    # -------------------------
    st.subheader("📋 Detalle de ventas")
    st.dataframe(df, use_container_width=True)

    # -------------------------
    # GRÁFICA POR PRODUCTO
    # -------------------------
    st.subheader("📦 Ventas por producto")

    resumen = df.groupby("producto")["total"].sum().sort_values(ascending=False)

    if resumen.empty:
        st.info("No hay datos para graficar productos")
    else:
        fig, ax = plt.subplots()
        resumen.plot(kind="bar", ax=ax)

        ax.set_title("Ventas por producto")
        ax.set_xlabel("Producto")
        ax.set_ylabel("Ingresos")

        # 🔥 EXTRA PRO
        ax.bar_label(ax.containers[0])

        st.pyplot(fig)

    # -------------------------
    # GRÁFICA POR DÍA
    # -------------------------
    st.subheader("📈 Ventas por día")

    ventas_dia = df.groupby(df["fecha"].dt.date)["total"].sum()

    if ventas_dia.empty:
        st.info("No hay datos para gráfica diaria")
    else:
        fig2, ax2 = plt.subplots()
        ventas_dia.plot(kind="line", ax=ax2)

        ax2.set_title("Ingresos diarios")
        ax2.set_xlabel("Fecha")
        ax2.set_ylabel("₡")

        st.pyplot(fig2)