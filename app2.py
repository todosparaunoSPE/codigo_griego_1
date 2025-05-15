# -*- coding: utf-8 -*-
"""
Created on Mon May 12 18:24:05 2025

@author: jahop
"""

import streamlit as st
import urllib.parse

# Mapeo de letras griegas a español
griego_a_espanol = {
    'α': 'a', 'β': 'b', 'γ': 'g', 'δ': 'd', 'ε': 'e',
    'ζ': 'z', 'η': 'h', 'θ': 'th', 'ι': 'i', 'κ': 'k',
    'λ': 'l', 'μ': 'm', 'ν': 'n', 'ξ': 'x', 'ο': 'o',
    'π': 'p', 'ρ': 'r', 'σ': 's', 'ς': 's', 'τ': 't',
    'υ': 'y', 'φ': 'ph', 'χ': 'ch', 'ψ': 'ps', 'ω': 'w',
    'Α': 'A', 'Β': 'B', 'Γ': 'G', 'Δ': 'D', 'Ε': 'E',
    'Ζ': 'Z', 'Η': 'H', 'Θ': 'Th', 'Ι': 'I', 'Κ': 'K',
    'Λ': 'L', 'Μ': 'M', 'Ν': 'N', 'Ξ': 'X', 'Ο': 'O',
    'Π': 'P', 'Ρ': 'R', 'Σ': 'S', 'Τ': 'T', 'Υ': 'Y',
    'Φ': 'Ph', 'Χ': 'Ch', 'Ψ': 'Ps', 'Ω': 'W'
}

# Mapeo inverso (español a griego)
espanol_a_griego = {v: k for k, v in griego_a_espanol.items()}

def traducir_griego_a_espanol(texto):
    resultado = []
    i = 0
    n = len(texto)
    while i < n:
        for length in [2, 1]:
            if i + length <= n:
                substring = texto[i:i+length]
                if substring in griego_a_espanol:
                    resultado.append(griego_a_espanol[substring])
                    i += length
                    break
        else:
            resultado.append(texto[i])
            i += 1
    return ''.join(resultado)

def traducir_espanol_a_griego(texto):
    resultado = []
    i = 0
    n = len(texto)
    while i < n:
        for length in [2, 1]:
            if i + length <= n:
                substring = texto[i:i+length].lower()
                if substring in espanol_a_griego:
                    if texto[i:i+length].istitle():
                        traducido = espanol_a_griego[substring].title()
                    elif texto[i:i+length].isupper():
                        traducido = espanol_a_griego[substring].upper()
                    else:
                        traducido = espanol_a_griego[substring]
                    resultado.append(traducido)
                    i += length
                    break
        else:
            resultado.append(texto[i])
            i += 1
    return ''.join(resultado)

def crear_enlace_whatsapp(mensaje):
    texto_codificado = urllib.parse.quote(mensaje)
    return f"https://wa.me/?text={texto_codificado}"

# Configuración del sidebar
with st.sidebar:
    st.title("Información")
    st.markdown("---")
    st.markdown("### Creado por:")
    st.markdown("**Javier Horacio Pérez Ricárdez**")
    st.markdown("---")
    st.markdown("### Alfabeto Griego:")
    st.write("""
    - **Minúsculas**: α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ/ς τ υ φ χ ψ ω  
    - **Mayúsculas**: Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω
    """)
    st.markdown("---")
    st.markdown("### Instrucciones:")
    st.write("""
    1. Selecciona la operación deseada  
    2. Introduce tu texto  
    3. Haz clic en el botón correspondiente  
    4. Copia el texto generado  
    5. Comparte por WhatsApp  
    """)

# Configuración de la app principal
st.title("🔠 Generador y Traductor de Código Griego")

opcion = st.radio("Selecciona una opción:", 
                 ("Generar código griego", "Traducir código griego a español"),
                 horizontal=True)

if opcion == "Generar código griego":
    texto_original = st.text_area("Introduce el texto en español para convertir a griego:", 
                                  height=150, 
                                  placeholder="Escribe aquí tu texto en español...")

    if st.button("Generar Código Griego", type="primary"):
        if texto_original:
            texto_griego = traducir_espanol_a_griego(texto_original)
            st.subheader("Resultado:")
            st.code(texto_griego, language=None)
            st.text_area("Copia el código manualmente:", texto_griego, height=100)
            
            # Guardar en session_state para WhatsApp
            st.session_state.texto_griego = texto_griego
        else:
            st.warning("Por favor introduce un texto para generar el código griego.")
else:
    texto_griego = st.text_area("Introduce el código en griego para traducir a español:", 
                                height=150, 
                                placeholder="Escribe aquí tu texto en griego...")

    if st.button("Traducir a Español", type="primary"):
        if texto_griego:
            texto_traducido = traducir_griego_a_espanol(texto_griego)
            st.subheader("Resultado:")
            st.code(texto_traducido, language=None)
            st.text_area("Copia la traducción manualmente:", texto_traducido, height=100)
            
            # Guardar en session_state para WhatsApp
            st.session_state.texto_traducido = texto_traducido
            st.session_state.texto_griego_original = texto_griego
        else:
            st.warning("Por favor introduce un código en griego para traducir.")

# Mostrar botones de WhatsApp si hay contenido generado
if 'texto_griego' in st.session_state:
    mensaje1 = f"\n{st.session_state.texto_griego}"
    mensaje2 = "¿Quieres traducir el código que te ha llegado? Ve a:\nhttps://codigo-griego.streamlit.app"
    enlace1 = crear_enlace_whatsapp(mensaje1)
    enlace2 = crear_enlace_whatsapp(mensaje2)

    st.markdown("---")
    st.subheader("Compartir por WhatsApp:")
    st.markdown(f'<a href="{enlace1}" target="_blank"><button style="background-color:#25D366;color:white;border:none;border-radius:5px;padding:10px;width:100%;">📤 Enviar Código</button></a>', unsafe_allow_html=True)
    st.markdown(f'<a href="{enlace2}" target="_blank"><button style="background-color:#128C7E;color:white;border:none;border-radius:5px;padding:10px;width:100%;">🔗 Enlace para traducir</button></a>', unsafe_allow_html=True)

if 'texto_traducido' in st.session_state:
    mensaje1 = f"Traducción del código:\nOriginal: {st.session_state.texto_griego_original}\nTraducción: {st.session_state.texto_traducido}"
    mensaje2 = "¿Quieres generar o traducir código griego?\nhttps://codigo-griego.streamlit.app"
    enlace1 = crear_enlace_whatsapp(mensaje1)
    enlace2 = crear_enlace_whatsapp(mensaje2)

    st.markdown("---")
    st.subheader("Compartir por WhatsApp:")
    st.markdown(f'<a href="{enlace1}" target="_blank"><button style="background-color:#25D366;color:white;border:none;border-radius:5px;padding:10px;width:100%;">📤 Enviar Traducción</button></a>', unsafe_allow_html=True)
    st.markdown(f'<a href="{enlace2}" target="_blank"><button style="background-color:#128C7E;color:white;border:none;border-radius:5px;padding:10px;width:100%;">🔗 Enlace para generar/traducir</button></a>', unsafe_allow_html=True)

# Pie de página
st.markdown("---")
st.caption("Aplicación creada por Javier Horacio Pérez Ricárdez - Generador y traductor de código griego")
