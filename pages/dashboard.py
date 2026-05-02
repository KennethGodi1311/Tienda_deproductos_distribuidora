import streamlit as st
import pandas as pd
from database.db import conectar
import matplotlib.pyplot as plt

def dashboard():

    st.title("📊 Dashboard de ventas")

    conexion = conectar()
    df = pd.read_sql("SELECT * FROM ventas", conexion)
    conexion.close()

    if df.empty:
        st.warning("No hay ventas aún")
        return

    st.dataframe(df)

    # -------------------------
    # TOTAL POR PRODUCTO
    # -------------------------
    resumen = df.groupby("producto")["total"].sum()

    fig, ax = plt.subplots()
    resumen.plot(kind="bar", ax=ax)
    ax.set_title("Ventas por producto")

    st.pyplot(fig)