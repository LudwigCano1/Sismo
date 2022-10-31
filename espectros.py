from numpy import array,linspace,zeros,arange
from math import pi
import pandas as pd
import streamlit as st
import plotly_express as px

st.set_page_config(page_title="Espectros E030")

def espectros(Z,U,S,R,Tp,Tl):
    T=arange(0,5.1,0.1)
    n=len(T)
    C,Sd,Sv=zeros((n)),zeros((n)),zeros((n))
    for i in range(n):
        if (T[i]<=Tp):
            C[i] = 2.50
        elif (T[i] <= Tl):
            C[i] = 2.5*Tp/T[i]
        else:
            C[i] = 2.5*((Tp*Tl)/(T[i]**2))
    Sa=Z*U*C*S*9.81/R
    for i in range(n):
        Sd[i]=((T[i]**2)/(4*pi**2))*Sa[i]
        Sv[i]=((T[i])/(2*pi))*Sa[i]
    return Sa,Sd,Sv,T,C



# Definición de valores de la norma

zonas = {"Z4":0.45,"Z3":0.35,"Z2":0.25,"Z1":0.1}

suelo = pd.DataFrame(columns=["Z","S0","S1","S2","S3"])
suelo["Z"] = ["Z4","Z3","Z2","Z1"]
suelo["S0"] = 0.80
suelo["S1"] = 1.00
suelo["S2"] = [1.05,1.15,1.20,1.60]
suelo["S3"] = [1.10,1.20,1.40,2.00]

periodos = {"S0":[0.3,3.0],"S1":[0.4,2.5],"S2":[0.6,2.0],"S3":[1.0,1.6]}

uso = {"A":1.5,"B":1.3,"C":1.0}
st.title("Espectros según la norma E030 Diseño Sismorresistente")

c1,c2,c3,c4,c5 = st.columns([2.5,2.5,2.5,1,2])

with c1:
    Zt = st.selectbox("Zona:",zonas.keys())
    Z = zonas[Zt]
    st.write("Z = ",Z)
with c2:
    U = st.selectbox("Categoría:",uso.keys())
    U = uso[U]
    st.write("U = ",U)
with c3:
    St = st.selectbox("Suelo:",["S0","S1","S2","S3"])
    S = float(suelo.loc[suelo["Z"] == Zt][St])
    Tp = periodos[St][0]
    Tl = periodos[St][1]
    st.write("S = ",S)
    st.write("Tp = ",Tp)
    st.write("Tl = ",Tl)
with c4:
    st.write("Ro:")
    ""
    st.write("Ia:")
    ""
    st.write("Ip:")
with c5:
    R0 = st.number_input("Ro:",3,8,step=1,label_visibility="collapsed")
    Ia = st.selectbox("Ia:",[0.50,0.60,0.75,0.80,0.90],label_visibility="collapsed")
    Ip = st.selectbox("Ip:",[0.60,0.75,0.85,0.90],label_visibility="collapsed")
    R = R0*Ia*Ip

Sa,Sd,Sv,T,C = espectros(Z,U,S,R,Tp,Tl)
esp = pd.DataFrame(columns=["T","C","Sa","Sv","Sd"])
esp["T"] = T
esp["C"] = C
esp["Sa"] = Sa
esp["Sv"] = Sv
esp["Sd"] = Sd

st.latex(r"""\begin{split}
\frac{Z.U.S}{R}g = \frac{(%.2f)(%.2f)(%.2f)}{(%.2f)}9.81=%.2f\ m/s^2
\end{split}"""%(Z,U,S,R,Z*U*S*9.81/R))

T1,T2,T3,T4,T5 = st.tabs(["[ C ]","[ Sa ]","[ Sv ]","[ Sd ]","[ Sd vs Sa ]"])

with T1:
    plot_C = px.line(x=[0],y=[0],labels={"x":"T (s)","y":"C"})
    plot_C.data = []
    plot_C.update_layout(showlegend=False)
    plot_C.add_scatter(x=T,y=C,mode="lines",name="C")
    plot_C.add_scatter(x=[Tp,Tp],y=[0,1.1*max(C)],mode="lines",line={"dash":"dash"},name="Tp")
    plot_C.add_scatter(x=[Tl,Tl],y=[0,1.1*max(C)],mode="lines",line={"dash":"dash"},name="Tl")
    st.plotly_chart(plot_C,use_container_width=True)

with T2:
    plot_Sa = px.line(x=[0],y=[0],labels={"x":"T (s)","y":"Sa"})
    plot_Sa.data = []
    plot_Sa.update_layout(showlegend=False)
    plot_Sa.add_scatter(x=T,y=Sa,mode="lines",name="Sa")
    plot_Sa.add_scatter(x=[Tp,Tp],y=[0,1.1*max(Sa)],mode="lines",line={"dash":"dash"},name="Tp")
    plot_Sa.add_scatter(x=[Tl,Tl],y=[0,1.1*max(Sa)],mode="lines",line={"dash":"dash"},name="Tl")
    st.plotly_chart(plot_Sa,use_container_width=True)

with T3:
    plot_Sv = px.line(x=[0],y=[0],labels={"x":"T (s)","y":"Sv"})
    plot_Sv.data = []
    plot_Sv.update_layout(showlegend=False)
    plot_Sv.add_scatter(x=T,y=Sv,mode="lines",name="Sv")
    plot_Sv.add_scatter(x=[Tp,Tp],y=[0,1.1*max(Sv)],mode="lines",line={"dash":"dash"},name="Tp")
    plot_Sv.add_scatter(x=[Tl,Tl],y=[0,1.1*max(Sv)],mode="lines",line={"dash":"dash"},name="Tl")
    st.plotly_chart(plot_Sv,use_container_width=True)

with T4:
    plot_Sd = px.line(x=[0],y=[0],labels={"x":"T (s)","y":"Sd"})
    plot_Sd.data = []
    plot_Sd.update_layout(showlegend=False)
    plot_Sd.add_scatter(x=T,y=Sd,mode="lines",name="Sd")
    plot_Sd.add_scatter(x=[Tp,Tp],y=[0,1.1*max(Sd)],mode="lines",line={"dash":"dash"},name="Tp")
    plot_Sd.add_scatter(x=[Tl,Tl],y=[0,1.1*max(Sd)],mode="lines",line={"dash":"dash"},name="Tl")
    st.plotly_chart(plot_Sd,use_container_width=True)

with T5:
    plot_Sd_Sa = px.line(x=[0],y=[0],labels={"x":"Sd","y":"Sa"})
    plot_Sd_Sa.data = []
    plot_Sd_Sa.update_layout(showlegend=False)
    plot_Sd_Sa.add_scatter(x=Sd,y=Sa,mode="lines",name="Sd vs Sa")
    v_Sa_1 = Z*U*2.5*S*9.81/R
    v_Sd_1 = ((Tp**2)/(4*pi**2))*v_Sa_1
    v_Sa_2 = Z*U*(2.5*Tp/Tl)*S*9.81/R
    v_Sd_2 = ((Tl**2)/(4*pi**2))*v_Sa_2
    plot_Sd_Sa.add_scatter(x=[0,1.1*v_Sd_1],y=[0,1.1*v_Sa_1],mode="lines",line={"dash":"dash"},name="Tp")
    plot_Sd_Sa.add_scatter(x=[0,1.1*v_Sd_2],y=[0,1.1*v_Sa_2],mode="lines",line={"dash":"dash"},name="Tl")
    st.plotly_chart(plot_Sd_Sa,use_container_width=True)
