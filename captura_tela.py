import cv2
import numpy as np
import mss
import pygetwindow as gw
from ultralytics import YOLO
from deepface import DeepFace  # Importar o DeepFace para predição de gênero

# Carregar o modelo YOLOv8n pré-treinado
model = YOLO('yolov8n.pt')

# Carregar o classificador Haar Cascade para rostos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def listar_janelas():
    """Lista todas as janelas disponíveis no sistema."""
    janelas = gw.getAllTitles()
    janelas_validas = [janela for janela in janelas if janela.strip()]
    return janelas_validas

def capturar_janela_por_nome(nome_janela):
    """Captura a janela com o nome fornecido."""
    janelas = gw.getWindowsWithTitle(nome_janela)
    
    if janelas:
        janela = janelas[0]
        return {
            'top': janela.top,
            'left': janela.left,
            'width': janela.width,
            'height': janela.height
        }
    else:
        print("Janela não encontrada.")
        return None

def classificar_genero(face):
    """Classifica o gênero com base na imagem da face usando DeepFace."""
    # Usar o DeepFace para prever o gênero
    preds = DeepFace.analyze(face, actions=['gender'], enforce_detection=False)
    
    # Como DeepFace retorna uma lista, acessamos o primeiro item da lista
    genero = preds[0]['gender']
    
    return genero

def capturar_janela_especifica(monitor_area):
    """Captura a área especificada da tela e exibe em tempo real com detecção de pessoas e classificação de gênero."""
    with mss.mss() as sct:
        while True:
            screenshot = sct.grab(monitor_area)
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # Redimensionar para no máximo 1200x1200
            h, w = frame.shape[:2]
            max_dim = 1200
            if h > max_dim > max_dim:
                scale = min(max_dim / h, max_dim / w)
                frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

            # Usar YOLOv8 para detectar pessoas no frame capturado
            results = model(frame)  # Realiza a detecção

            # Processar resultados da detecção
            for result in results[0].boxes:
                if result.cls == 0:  # A classe '0' representa 'pessoa'
                    x1, y1, x2, y2 = map(int, result.xyxy[0])  # Coordenadas da caixa delimitadora

                    # Recortar a área do rosto para classificar o gênero
                    face_region = frame[y1:y2, x1:x2]
                    face_gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(face_gray, 1.1, 4)

                    # Classificar gênero usando a face detectada
                    for (fx, fy, fw, fh) in faces:
                        face = frame[fy:fy+fh, fx:fx+fw]
                        if face is not None:
                            genero = classificar_genero(face)
                            # Desenhar a caixa verde para homens e rosa para mulheres
                            if genero == "Man":
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Caixa verde para homem
                            else:
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)  # Caixa rosa para mulher

            # Exibir a captura de tela com os quadrados
            cv2.imshow("Detecção de Pessoas com YOLOv8 e Gênero", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
