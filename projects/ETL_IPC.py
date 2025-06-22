# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 07:24:08 2025

@author: MARCELO
"""
# %reset -f

# Setting of directory of work
import os
os.chdir("D:/DATA_SCIENCE_ENDI/NOTEBOOKS_R/MULTIVARIANTE/MARCELO_WEBSITE/projects/")

# Reading of DataSet at Datsource: IPC - INEC
import pandas as pd

df_ipc = pd.read_excel("IPC/SERIE HISTORICA IPC_05_2025.xls",
                        sheet_name="1. ÍNDICE",
                        skiprows=4,
                        engine="xlrd")

# Find the first row where all cells are empty (NaN)
fila_vacia = df_ipc[df_ipc.isnull().all(axis=1)].index

# If an empty row is found, trim the DataFrame up to that row
if not fila_vacia.empty:
    df_ipc = df_ipc.iloc[:fila_vacia[0]]

# List with the correct names of the columns
nuevos_nombres = ["AÑO",
                  "ENERO", 
                  "FEBRERO",
                  "MARZO",
                  "ABRIL",
                  "MAYO",
                  "JUNIO",
                  "JULIO",
                  "AGOSTO", 
                  "SEPTIEMBRE", 
                  "OCTUBRE",
                  "NOVIEMBRE",
                  "DICIEMBRE"]

# Assign the new names to the DataFrame
df_ipc.columns = nuevos_nombres

# Basic DataFrame features:

# display(df_ipc.dtypes)
# display(df_ipc.shape)
# display(df_ipc.describe(include="all"))

# =============================================================================
# Calculation of IPC
# =============================================================================

# Filter of DataFrame IPC desde el año base 2014=100
df_ipc = df_ipc.loc[df_ipc['AÑO'] >= 2014].reset_index(drop=True)

# Ordered list of months
meses = ["ENERO", 
         "FEBRERO",
         "MARZO",
         "ABRIL", 
         "MAYO", 
         "JUNIO",
         "JULIO", 
         "AGOSTO", 
         "SEPTIEMBRE",
         "OCTUBRE",
         "NOVIEMBRE",
         "DICIEMBRE"]

# Create new DataFrame for monthly inflation
df_inflacion = df_ipc[["AÑO"]].copy()

# Base year (2014) equal to 100
df_inflacion.loc[0, meses] = 1

# Calculate monthly inflation for the following years
for i in range(1, len(df_ipc)):
    for j, mes in enumerate(meses):
        valor_actual = df_ipc.loc[i, mes]

        # Skip if None or NaN (case of 2025 from June)
        if pd.isna(valor_actual):
            continue

        if j == 0:
            # JANUARY: use DECEMBER of the preceding year
            valor_anterior = df_ipc.loc[i-1, "DICIEMBRE"]
        else:
            # Rest of months: use the previous month of the same year.
            valor_anterior = df_ipc.loc[i, meses[j-1]]

        # Avoid calculation if previous value is None or NaN
        if pd.isna(valor_anterior):
            continue

        inflacion = ((valor_actual - valor_anterior) / valor_actual) * 100
        df_inflacion.loc[i, mes] = round(inflacion, 2)

# =============================================================================
# Graphic of IPC
# =============================================================================

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import pandas as pd

# Asegurar tipos correctos
df_inflacion["AÑO"] = df_inflacion["AÑO"].astype(int)
df_inflacion["ENERO"] = pd.to_numeric(df_inflacion["ENERO"], errors='coerce')  # Convierte a float

# Estilo profesional
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("notebook")

# Crear figura y ajustar resolución
fig, ax = plt.subplots(figsize=(10, 5), dpi=150)

# Graficar línea fina y puntos pequeños
ax.plot(df_inflacion["AÑO"], df_inflacion["ENERO"],
        marker="o", markersize=4, linewidth=1.5, color="#004e98", label="Inflación Enero")

# Título y etiquetas
ax.set_title("Inflación mensual - Enero", fontsize=14, fontweight='bold')
ax.set_xlabel("Año", fontsize=12)
ax.set_ylabel("Inflación (%)", fontsize=12)

# Mostrar todos los años
ax.set_xticks(df_inflacion["AÑO"])

# Formato porcentaje
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
ax.tick_params(axis='x', labelrotation=45)
ax.tick_params(axis='both', labelsize=10)

# Leyenda y cuadrícula
ax.legend(loc="upper left", fontsize=10)
ax.grid(True, linestyle='--', alpha=0.4)

# Ajustar layout
plt.tight_layout()
plt.show()
