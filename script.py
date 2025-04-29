import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

df = pd.read_csv('salaries.csv')

#Filters


st.sidebar.header("Filters")
year = st.sidebar.selectbox("Year", sorted(df["work_year"].unique()))
experience = st.sidebar.multiselect("Experience level", df["experience_level"].unique(), default=df["experience_level"].unique())
company_size = st.sidebar.multiselect("Company size", df["company_size"].unique(), default=df["company_size"].unique())


#Data filtering


df_filtered = df[
    (df["work_year"] == year) &
    (df["experience_level"].isin(experience)) &
    (df["company_size"].isin(company_size))
]

st.title("Dashboard de Sueldos en Ciencia de Datos") #Title

#Graphics

fig1 = px.box(df_filtered, x="employment_type", y="salary_in_usd", color="employment_type",
              title="Distribución de sueldos por tipo de empleo")
st.plotly_chart(fig1)



st.subheader("Salario promedio por país")
avg_salary = df_filtered.groupby("company_location")["salary_in_usd"].mean().reset_index().sort_values("salary_in_usd", ascending=True)
fig2 = px.bar(avg_salary, x="company_location", y="salary_in_usd", title="Salario promedio por país")
st.plotly_chart(fig2)


st.subheader("Tendencias salariales de 2020 a 2022")
trend_data = df.groupby(["work_year", "employment_type"])["salary_in_usd"].mean().reset_index()
fig3 = px.line(trend_data, x="work_year", y="salary_in_usd", color="employment_type", markers=True)
st.plotly_chart(fig3)


st.subheader("Comparación de sueldos por modalidad (onsite / híbrido / remoto)")
remote_map = {0: "Onsite", 50: "Híbrido", 100: "Remoto"}
df_filtered["work_mode"] = df_filtered["work_models"]
fig4 = px.box(df_filtered, x="work_mode", y="salary_in_usd", color="work_mode")
st.plotly_chart(fig4)

st.markdown("### Resumen ejecutivo")
st.markdown(f"- Año seleccionado: **{year}**")
st.markdown(f"- Se observa que los trabajos **remotos** tienen sueldos distintos frente a los presenciales o híbridos.")
st.markdown(f"- Hay una tendencia de crecimiento salarial entre 2020 y 2022.")
st.markdown(f"- Puedes filtrar por experiencia y tamaño de empresa desde la barra lateral.")

