import streamlit as st
from openpyxl import Workbook

wb = Workbook()

wb.create_sheet("Hoja_A",0)

direc = st.text_input("Dirección:")
filename = st.text_input("Nombre de archivo:")
n = direc+"\\"+filename+".xlsx"
print(n)

if st.button("Descargar"):
    wb.save("Hola.xlsx")
