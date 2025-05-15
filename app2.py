# -*- coding: utf-8 -*-
"""
Created on Mon May 12 18:24:05 2025

@author: jahop
"""

import streamlit as st
import urllib.parse
import pyperclip

# Mapeos de caracteres
griego_a_espanol = {
    'α': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'ζ': 'z', 'η': 'h',
    'θ': 'th', 'ι': 'i', 'κ': 'k', 'λ': 'l', 'μ': 'm', 'ν': 'n', 'ξ': 'x',
    'ο': 'o', 'π': 'p', 'ρ': 'r', 'σ': 's', 'ς': 's', 'τ': 't', 'υ': 'y',
    'φ': 'ph', 'χ': 'ch', 'ψ': 'ps', 'ω': 'w',
    'Α': 'A', 'Β': 'B', 'Γ': 'G', 'Δ': 'D', 'Ε': 'E', 'Ζ': 'Z', 'Η': 'H',
    'Θ': 'Th', 'Ι': 'I', 'Κ': 'K', 'Λ': 'L', 'Μ': 'M', 'Ν': 'N', 'Ξ': 'X',
    'Ο': 'O', 'Π': 'P', 'Ρ': 'R', 'Σ': 'S', 'Τ': 'T', 'Υ': 'Y', 'Φ': 'Ph',
    'Χ': 'Ch', 'Ψ': 'Ps', 'Ω': 'W'
}
espanol_a_griego = {v: k for k, v in griego_a_espanol.items()}

def traducir_griego_a_espanol(texto):
    resultado = []
    i = 0
    while i < len(texto):
        for l in [2, 1]:
            if i + l <= len(texto) and texto[i:i+l] in griego_a_espanol:
                resultado.append(griego_a_espanol[texto[i:i+l]])
                i += l
                break
        else:
            resultado.append(texto[i])
            i += 1
    return ''.join(resultado)

def traducir_espanol_a_griego(texto):
    resultado = []
    i = 0
    while i < len(texto):
        for l in [2, 1]:
            substring = texto[i:i+l].lower()
            if substring in espanol_a_griego:
                traducido = espanol_a_griego[substring]
                if texto[i:i+l].istitle():
                    traducido = traducido.title()
                elif texto[i:i+l].isupper():
                    traducido = traducido.upper()
                resultado.append(traducido)
                i += l
                break
        else:
            resultado.append(texto[i])
            i += 1
    return ''.join(resultado)

def crear_enlaces_whatsapp(mensaje_1, mensaje_2):
    mensaje_1_url = urllib.parse.quote(mensaje_1)
    mensaje_2_url = urllib.parse.quote(mensaje_2)
    enlace1 = f"https://wa.me/?text={mensaje_1_url}"
    enlace2 = f"https://wa.me/?text={mensaje_2_url}"
    return enlace1, enlace2

# Sidebar
with st.sidebar:
    st.title("Información")
    st.markdown("---")
    st.markdown("### Creado por:")
    st.markdown("**Javier Horacio Pérez Ricárdez**")
    st.markdown("### Alfabeto Griego:")
    st.write("Minúsculas: α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ/ς τ υ φ χ ψ ω")
    st.write("Mayúsculas: Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω")
    st.markdown("### Instrucciones:")
    st.write("1. Selecciona una opción\n2. Escribe tu texto\n3. Genera o traduce\n4. Copia y comparte por WhatsApp")

# Estado inicial
if 'copied' not in st.session_state:
    st.session_state.copied = False

st.title("🔠 Generador y Traductor de Código Griego")

opcion = st.radio("Selecciona una opción:", 
                 ("Generar código griego", "Traducir código griego a español"),
                 horizontal=True)

if opcion == "Generar código griego":
    texto_original = st.text_area("Texto en español:", height=150, placeholder="Escribe tu texto...")
    if st.button("Generar Código Griego", type="primary"):
        if texto_original:
            texto_griego = traducir_espanol_a_griego(texto_original)
            st.subheader("Resultado:")
            st.code(texto_griego, language=None)
            
            st.session_state.texto_a_copiar = texto_griego
            st.session_state.mensaje_whatsapp1 = f"\n{texto_griego}"
            st.session_state.mensaje_whatsapp2 = "Traduce este código en: https://tuapp.streamlit.app"
            st.session_state.copied = False
        else:
            st.warning("Introduce texto para generar el código.")
else:
    texto_griego = st.text_area("Texto en griego:", height=150, placeholder="Escribe tu texto griego...")
    if st.button("Traducir a Español", type="primary"):
        if texto_griego:
            texto_traducido = traducir_griego_a_espanol(texto_griego)
            st.subheader("Resultado:")
            st.code(texto_traducido, language=None)
            
            st.session_state.texto_a_copiar = texto_traducido
            st.session_state.mensaje_whatsapp1 = f"Texto traducido:\n{texto_traducido}"
            st.session_state.mensaje_whatsapp2 = "¿Quieres traducir más? Visita: https://tuapp.streamlit.app"
            st.session_state.copied = False
        else:
            st.warning("Introduce texto en griego para traducir.")

# Mostrar botón para copiar y compartir
if 'texto_a_copiar' in st.session_state:
    if st.button("📋 Copiar al Portapapeles"):
        pyperclip.copy(st.session_state.texto_a_copiar)
        st.session_state.copied = True
        st.success("¡Texto copiado!")

    if st.session_state.copied:
        enlace1, enlace2 = crear_enlaces_whatsapp(
            st.session_state.mensaje_whatsapp1,
            st.session_state.mensaje_whatsapp2
        )

        st.markdown("### Compartir en WhatsApp:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<a href="{enlace1}" target="_blank"><button style="background-color:#25D366;color:white;border-radius:5px;padding:10px;width:100%">1️⃣ Código</button></a>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<a href="{enlace2}" target="_blank"><button style="background-color:#128C7E;color:white;border-radius:5px;padding:10px;width:100%">2️⃣ Enlace</button></a>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Aplicación creada por Javier Horacio Pérez Ricárdez - Generador y traductor de código griego")
