import streamlit as st
import matplotlib.pyplot as plt
# import pandas as pd
import numpy as np

def classificar(valor, limite):
    if valor <= limite * 0.7:
        return "Normal", "🟢"
    elif valor <= limite * 0.9:
        return "Alerta", "🟡"
    else:
        return "Crítico", "🔴"

st.title("Sistema de Manutenção Preditiva")
st.sidebar.title("Configurações")

st.sidebar.markdown("---")
st.sidebar.markdown("**Limites de operação:**")

temp_max  = st.sidebar.number_input("Temperatura máxima (°C):", value=80.0)
vibr_max  = st.sidebar.number_input("Vibração máxima (mm/s):", value=7.0)
press_max = st.sidebar.number_input("Pressão máxima (bar):", value=10.0)

st.header("Dados da Máquina")

col1, col2, col3 = st.columns(3)

with col1:
    temperatura = st.number_input("Temperatura (°C):", value=0.0)

with col2:
    vibracao = st.number_input("Vibração (mm/s):", value=0.0)

with col3:
    pressao = st.number_input("Pressão (bar):", value=0.0)

if st.button("Analisar"):

    status_temp,  icon_temp  = classificar(temperatura, temp_max)
    status_vibr,  icon_vibr  = classificar(vibracao,    vibr_max)
    status_press, icon_press = classificar(pressao,     press_max)

    st.markdown("---")
    st.header("Resultado da Análise")

    r1, r2, r3 = st.columns(3)

    with r1:
        st.metric("Temperatura", f"{temperatura}°C")
        st.markdown(f"**Status: {icon_temp} {status_temp}**")
        fig, ax = plt.subplots(figsize=(4, 2))

        theta1 = np.linspace(0, 1.047, 100) 
        theta2 = np.linspace( 1.047, 2.094, 100) 
        theta3 = np.linspace(2.094, 3.14 , 100)

        ax.plot(np.cos(theta1), np.sin(theta1), color="red", linewidth=10)
        ax.plot(np.cos(theta2), np.sin(theta2), color="yellow", linewidth=10)
        ax.plot(np.cos(theta3), np.sin(theta3), color="green", linewidth=10)
        
        porcentagem = min(temperatura / temp_max, 1.0)
        angulo = np.pi - porcentagem * np.pi
        ax.plot([0, np.cos(angulo)], [0, np.sin(angulo)], color="black", linewidth=3)
        ax.axis("off")

        st.pyplot(fig)
        plt.close(fig)
        
    with r2:
        st.metric("Vibração", f"{vibracao} mm/s")
        st.markdown(f"**Status: {icon_vibr} {status_vibr}**")
        fig, ax = plt.subplots(figsize=(4, 2))

        delta1 = np.linspace(0, 1.047, 100) 
        delta2 = np.linspace( 1.047, 2.094, 100) 
        delta3 = np.linspace(2.094, 3.14 , 100)

        ax.plot(np.cos(delta1), np.sin(delta1), color="red", linewidth=10)
        ax.plot(np.cos(delta2), np.sin(delta2), color="yellow", linewidth=10)
        ax.plot(np.cos(delta3), np.sin(delta3), color="green", linewidth=10)

        porcentagem = min(vibracao / vibr_max, 1.0)
        angulo = np.pi - porcentagem * np.pi
        ax.plot([0, np.cos(angulo)], [0, np.sin(angulo)], color="black", linewidth=3)
        ax.axis("off")

        st.pyplot(fig)
        plt.close(fig)

    with r3:
        st.metric("Pressão", f"{pressao} bar")
        st.markdown(f"**Status: {icon_press} {status_press}**")
        fig, ax = plt.subplots(figsize=(4, 2))

        beta1 = np.linspace(0, 1.047, 100) 
        beta2 = np.linspace( 1.047, 2.094, 100) 
        beta3 = np.linspace(2.094, 3.14 , 100)

        ax.plot(np.cos(beta1), np.sin(beta1), color="red", linewidth=10)
        ax.plot(np.cos(beta2), np.sin(beta2), color="yellow", linewidth=10)
        ax.plot(np.cos(beta3), np.sin(beta3), color="green", linewidth=10)

        porcentagem = min(pressao / press_max, 1.0)
        angulo = np.pi - porcentagem * np.pi
        ax.plot([0, np.cos(angulo)], [0, np.sin(angulo)], color="black", linewidth=3)
        ax.axis("off")

        st.pyplot(fig)
        plt.close(fig)


