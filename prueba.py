import streamlit as st
from openpyxl import Workbook
from tempfile import NamedTemporaryFile
from io import BytesIO

wb = Workbook()
wb.create_sheet("Hoja_A",0)

with NamedTemporaryFile() as tmp:
    wb.save(tmp.name)
    data = BytesIO(tmp.read())

st.download_button("Descargar",data=data,mime="xlsx",file_name="gato.xlsx")
