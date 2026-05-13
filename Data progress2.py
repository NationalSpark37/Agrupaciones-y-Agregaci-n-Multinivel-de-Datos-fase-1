#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import datetime
import os

print("PASO 1: CARGANDO EL DATASET")

df = None
metodo_usado = None

try:
    df = pd.read_csv('pipol_dataset__1_.csv')
    metodo_usado = "archivo local"
except FileNotFoundError:
    try:
        df = pd.read_csv('pipol_dataset (1).csv')
        metodo_usado = "archivo local"
    except FileNotFoundError:
        print("Descargando desde GitHub...")
        try:
            url_github = "https://github.com/NationalSpark37/Agrupaciones-y-Agregaci-n-Multinivel-de-Datos-fase-1/raw/main/pipol_dataset%20(1).csv"
            df = pd.read_csv(url_github)
            metodo_usado = "GitHub"
        except Exception as e:
            print(f"Error: {e}")
            exit()

print(f"\n Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
print("\nPrimeras 5 filas:")
print(df.head())

print("PASO 2: CONVERSIÓN DE BIRTHDAY A DATETIME")

df['birthday'] = pd.to_datetime(df['birthday'], format='%d/%m/%Y')
print(f"\nTipo de dato: {df['birthday'].dtype}")
print(df.head())

print("PASO 3: CÁLCULO DE EDAD")

df['age'] = datetime.datetime.now().year - df['birthday'].dt.year

print("\nEdadísticas:")
print(f"Mínima: {df['age'].min()}, Máxima: {df['age'].max()}, Promedio: {df['age'].mean():.2f}")
print("\nPrimeras 10 filas con edad:")
print(df[['name', 'birthday', 'age']].head(10))

print("PASO 4: AGRUPACIÓN POR PAÍS")

group_by_country = df.groupby('country')
print("\nPaíses encontrados:")
print(group_by_country.groups.keys())
print("\nPersonas por país:")
print(group_by_country.size())

print("\n" + "=" * 70)
print("PASO 5: EDAD PROMEDIO POR PAÍS")
print("=" * 70)

age_avg = df.groupby('country')['age'].agg(['mean', 'count', 'min', 'max'])
age_avg.columns = ['Promedio', 'Total', 'Mín', 'Máx']
print("\n")
print(age_avg)

age_simple = df.groupby('country')['age'].mean()
print("\nPromedio simple por país:")
print(age_simple)

print("PASO 6: ACCESO A GRUPOS CON get_group()")

print("\nMexico:")
mexico = group_by_country.get_group('Mexico')
print(mexico[['name', 'city', 'age']])

print("\nSpain:")
spain = group_by_country.get_group('Spain')
print(spain[['name', 'city', 'age']])

print("PASO 7: AGREGACIÓN MULTINIVEL (PAÍS + CIUDAD)")

multilevel = df.groupby(['country', 'city'])['age'].agg(['mean', 'count'])
multilevel.columns = ['Promedio', 'Total']
print("\n")
print(multilevel)

print("RESUMEN FINAL")

print(f"\nTotal registros: {len(df)}")
print(f"Países: {df['country'].nunique()}")
print(f"Ciudades: {df['city'].nunique()}")
print(f"\nMayor edad promedio: {age_simple.idxmax()} ({age_simple.max():.2f} años)")
print(f"Menor edad promedio: {age_simple.idxmin()} ({age_simple.min():.2f} años)")

print("SCRIPT COMPLETADO")


# In[ ]:




