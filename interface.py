import customtkinter as ctk
import mss
import numpy as np
import cv2
from captura_tela import listar_janelas, capturar_janela_por_nome, capturar_janela_especifica
from PIL import Image
from customtkinter import CTkImage
from tkinter import filedialog
from sono_analyzer import analisar_sono  # Importando a função para análise de sono

def criar_interface(selecionar_video_pessoas_callback, selecionar_video_sono_callback):
    # Configurações principais da janela
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Seleção de Análise")
    root.geometry("1000x800")  # Ajustei o tamanho da janela para suportar mais colunas

    # Título
    title_label = ctk.CTkLabel(root, text="Escolha uma análise", font=("Helvetica", 18))
    title_label.pack(pady=20)

    # Botão para analisar pessoas em vídeo
    btn_analisar_pessoas = ctk.CTkButton(root, text="Analisar Pessoas em Vídeo (Desativado)", 
                                         command=selecionar_video_sono_callback, width=300, height=100)
    btn_analisar_pessoas.pack(pady=10)

    # Botão para analisar sono
    btn_analisar_sono = ctk.CTkButton(root, text="Analisar Sono", 
                                      command=selecionar_video_sono_callback, width=300, height=100)
    btn_analisar_sono.pack(pady=10)

    # Botão para selecionar janelas específicas
    btn_selecionar_janela = ctk.CTkButton(root, text="Selecionar janela específica (Desativado)", 
                                          command=selecionar_video_sono_callback, width=300, height=100)
    btn_selecionar_janela.pack(pady=10)


    # Iniciar a interface gráfica principal
    root.mainloop()
