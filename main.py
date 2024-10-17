import interface
import detector
import sono_analyzer
from tkinter import filedialog
from captura_tela import listar_janelas, capturar_janela_por_nome, capturar_janela_especifica

video_source = None

# Callback para selecionar vídeo de análise de pessoas
def selecionar_video_pessoas():
    global video_source
    video_source = filedialog.askopenfilename(
        title="Selecionar vídeo",
        filetypes=[("Arquivos de Vídeo", "*.mp4 *.avi *.mov *.mkv")]
    )
    if video_source:
        detector.iniciar_video(video_source)

# Callback para selecionar vídeo de análise de sono
def selecionar_video_sono():
    global video_source
    video_source = filedialog.askopenfilename(
        title="Selecionar vídeo",
        filetypes=[("Arquivos de Vídeo", "*.mp4 *.avi *.mov *.mkv")]
    )
    if video_source:
        sono_analyzer.analisar_sono(video_source)

def abrir_captura_de_janela():
    """Função para listar janelas e capturar a janela selecionada"""
    # Listar as janelas disponíveis
    janelas = listar_janelas()
    indice = int(input("Selecione o índice da janela para capturar: ")) - 1
    nome_janela = janelas[indice]

    # Capturar a área da janela selecionada
    monitor_area = capturar_janela_por_nome(nome_janela)
    if monitor_area:
        capturar_janela_especifica(monitor_area)  # Aqui chamamos a função correta

if __name__ == "__main__":
    interface.criar_interface(selecionar_video_pessoas, selecionar_video_sono)
