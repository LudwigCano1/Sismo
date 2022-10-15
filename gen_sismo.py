import streamlit as st
import numpy as np
import math as m
import plotly_express as px

st.set_page_config(layout="wide")


plot = px.line(x=[0],y=[0],labels={"x":"t (s)","y":"u (cm)"})

t_i = 0; dt = 0.01; t_f = 20
t_set = np.arange(t_i,t_f,dt,float)
u = np.zeros(int((t_f-t_i)/dt))

def GenerarDesplazamiento(omega,A,phi,set_t):
    desp = []
    for t in set_t:
        desp.append(A*m.sin(omega*t+phi))
    return np.array(desp)

def AgregarOnda(lab,Tlabel,Alabel,philabel,t_Set):
    c2,c3,c4,c1 = st.columns([3,3,3,1])
    with c1: a = st.checkbox(label=lab)
    with c2: T = st.number_input(Tlabel,min_value=0.0,max_value=10.0,value=2.0,step=0.1)
    with c3: A = st.number_input(Alabel,min_value=0.0,max_value=15.0,value=2.0,step=0.1)
    with c4: phi = st.number_input(philabel,min_value=0,max_value=180,step=1)/180 * m.pi
    vDesp = GenerarDesplazamiento(2*m.pi/T,A,phi,t_Set)
    nnn = np.zeros(int((t_f-t_i)/dt))
    if a:
        lab += " "
        Tlabel += " "
        Alabel += " "
        philabel += " "
        nnn = AgregarOnda(lab,Tlabel,Alabel,philabel,t_set)
    return vDesp + nnn
    
with st.sidebar:
    st.title("Overlap Waves")
    st.write("**Developed by:** Ludwig Cano")
    st.write("---")
    Y = AgregarOnda(" ","T (s):","A (cm):","ϕ (deg):",t_set)

plot.add_scatter(x=t_set,y=Y,mode="lines",name=f"sismo")
st.plotly_chart(plot,use_container_width=True)
