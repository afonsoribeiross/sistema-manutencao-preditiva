import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import sqlite3

def init_db():
    conn = sqlite3.connect("historico.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leituras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperatura REAL,
            vibracao REAL,
            pressao REAL,
            status_temp TEXT,
            status_vibr TEXT,
            status_press TEXT,
            data_hora TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

if "historico" not in st.session_state:
    st.session_state.historico = []

def classificar(valor, limite):
    if valor <= limite * 0.7:
        return "Normal", "🟢"
    elif valor <= limite * 0.9:
        return "Alerta", "🟡"
    else:
        return "Crítico", "🔴"

st.title("Sistema de Manutenção Preditiva")
st.sidebar.title("Parâmetros da Máquina")

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
    
    st.session_state.historico.append({
    "Temperatura (°C)": temperatura,
    "Vibração (mm/s)": vibracao,
    "Pressão (bar)": pressao,
    "Status Temp": status_temp,
    "Status Vibr": status_vibr,
    "Status Press": status_press,
    "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    })
    conn = sqlite3.connect("historico.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO leituras VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)
    """, (temperatura, vibracao, pressao, status_temp, status_vibr, status_press, datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    conn.commit()
    conn.close()
    st.markdown("---")
    alertas_criticos = []
    alertas_alerta = []

    if status_temp == "Crítico":
        alertas_criticos.append("Temperatura")
    if status_vibr == "Crítico":
        alertas_criticos.append("Vibração")
    if status_press == "Crítico":
        alertas_criticos.append("Pressão")

    if status_temp == "Alerta":
        alertas_alerta.append("Temperatura")
    if status_vibr == "Alerta":
        alertas_alerta.append("Vibração")
    if status_press == "Alerta":
        alertas_alerta.append("Pressão")

    if alertas_criticos:
        st.error(f"⚠️ Estado Crítico: {', '.join(alertas_criticos)}")
        requests.post("https://afonsoribeiross.app.n8n.cloud/webhook/32b2dd6b-5678-452e-8006-3612d420d4ee", json={"parametros": alertas_criticos})
        
    elif alertas_alerta:
        st.warning(f"⚠️ Estado de Alerta: {', '.join(alertas_alerta)}")
    else:
        st.success("✅ Todos os parâmetros normais!")   
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
        st.markdown("---")

conn = sqlite3.connect("historico.db")
df = pd.read_sql("SELECT * FROM leituras", conn)
conn.close()

if not df.empty:
    st.header("Histórico de Leituras")
    st.dataframe(df)

    fig, ax = plt.subplots(figsize=(10, 4)) 
    ax.plot(df["temperatura"] / temp_max * 100, label="Temperatura")
    ax.plot(df["vibracao"] / vibr_max * 100, label="Vibração")
    ax.plot(df["pressao"] / press_max * 100, label="Pressão")
    ax.axhline(y=100, color="red", linestyle="--", linewidth=1.5, label="Limite crítico") 
    ax.legend()
    ax.set_title("Evolução de Parâmetros")
    ax.set_xlabel("Leitura")
    ax.set_ylabel("% do limite máximo")
    st.pyplot(fig)
    plt.close(fig)

if  st.button("Limpar Histórico"):
    st.session_state.historico = []    
