import cv2
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from weather import obter_dados_clima


# Função para classificar os estágios do sono com base nos movimentos detectados
def classificar_estagio_sono(movimentos):
    if movimentos > 10:
        return 'Sono Leve'
    elif movimentos > 2:
        return 'REM'
    else:
        return 'Sono Profundo'

def monitorar_estagios_sono(dados_movimento):
    estagios = []
    timestamps = []
    for timestamp, movimentos in dados_movimento.items():
        estagio = classificar_estagio_sono(movimentos)
        estagios.append(estagio)
        timestamps.append(timestamp)

    return estagios, timestamps

# Exemplo de dados fictícios de movimentação por período (podem ser gerados a partir do YOLOv8n)
dados_movimento = {
    '22:00': 12,  # Muitos movimentos (sono leve)
    '23:00': 5,   # REM
    '00:00': 1,   # Sono profundo
    '01:00': 3,   # REM
    '02:00': 0,   # Sono profundo
}

# Classifica os estágios de sono
estagios, timestamps = monitorar_estagios_sono(dados_movimento)

# Gera um gráfico dos estágios de sono
def plotar_estagios_sono(timestamps, estagios):
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, estagios, marker='o', linestyle='-', color='b')
    plt.title("Estágios do Sono de Noah")
    plt.xlabel("Horário")
    plt.ylabel("Estágio do Sono")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Exemplo de chave e cidade para teste
api_key = "3f8510aed353a2274b6a4f7a772e100e"
cidade = "Campinas"

# Função para monitorar o sono e armazenar dados climáticos
def monitorar_sono_com_clima(movimentos, despertares):
    # Obter os dados de clima
    temperatura, umidade, condicao = obter_dados_clima(api_key, cidade)
    
    # Armazenar os dados junto com os movimentos e despertares
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dados_sono = {
        "timestamp": timestamp,
        "movimentos": movimentos,
        "despertares": despertares,
        "temperatura": temperatura,
        "umidade": umidade,
        "condicao": condicao
    }

    print(f"Dados armazenados: {dados_sono}")

    return dados_sono

def gerar_grafico_sono(awake_periods, sleep_periods):
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plotar períodos acordados e de sono profundo
    awake_times = [p.time() for p in awake_periods]
    sleep_times = [p.time() for p in sleep_periods]

    ax.plot(awake_times, [1] * len(awake_times), 'ro', label="Acordado")
    ax.plot(sleep_times, [0] * len(sleep_times), 'bo', label="Sono profundo")

    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Sono profundo", "Acordado"])
    ax.set_xlabel("Horário")
    ax.set_title("Análise do Sono de Noah")
    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

modelo_bebe = ("C:/Users/sylvio.zanotti/Desktop/system_vigilancia/DataTest/data.yaml")
def detectar_bebe(frame):
    resultados = modelo_bebe(frame)
    
    for resultado in resultados:
        for classe, x, y, w, h in resultado.boxes.data:
            # Assumindo que a classe "0" representa o bebê
            if int(classe) == 0:  # Ajuste conforme o treinamento do seu modelo
                return (x, y, w, h)
    
    return None

def analisar_sono(video_source=None, duracao_minima_sono=30):
    if video_source is None:
        print("Nenhum vídeo selecionado.")
        return

    cap = cv2.VideoCapture(video_source)
    movements_detected = 0
    total_movement_time = 0
    awake_periods = []
    sleep_periods = []
    current_state = 'Dormindo'
    start_sleep_time = time.time()

    # Lista para armazenar os dados de sono com clima
    dados_sono = []

    # Loop de análise do vídeo
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detectar a presença do bebê no frame
        bbox_bebe = detectar_bebe(frame)
        if bbox_bebe is None:
            # Se o bebê não for detectado, não há movimento relevante a analisar
            continue

        (x, y, w, h) = bbox_bebe
        # Cortar a região do frame que contém o bebê
        frame_bebe = frame[int(y):int(y+h), int(x):int(x+w)]

        # Converter a região do frame do bebê para escala de cinza e aplicar suavização
        gray_frame = cv2.cvtColor(frame_bebe, cv2.COLOR_BGR2GRAY)
        blurred_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        # Inicializando o primeiro quadro como referência
        if 'first_frame' not in locals():
            first_frame = blurred_frame
            continue

        # Cálculo da diferença entre o primeiro quadro e o atual (apenas na área do bebê)
        frame_delta = cv2.absdiff(first_frame, blurred_frame)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Encontrar contornos de movimento dentro da área do bebê
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        movement_detected = False
        for contour in contours:
            if cv2.contourArea(contour) < 100:  # Limiar ajustável para pequenos movimentos
                continue
            movement_detected = True
            (cx, cy, cw, ch) = cv2.boundingRect(contour)
            cv2.rectangle(frame_bebe, (cx, cy), (cx + cw, cy + ch), (0, 255, 0), 2)

        # Atualizar o quadro de referência para a próxima iteração
        first_frame = blurred_frame

        # Verificar estado atual (Dormindo ou Acordado)
        if movement_detected:
            if current_state == 'Dormindo':
                awake_time = datetime.now()
                awake_periods.append(awake_time)
                current_state = 'Acordado'
            total_movement_time += 1
            movements_detected += 1
        else:
            if current_state == 'Acordado' and time.time() - start_sleep_time >= duracao_minima_sono:
                sleep_time = datetime.now()
                sleep_periods.append(sleep_time)
                current_state = 'Dormindo'
                start_sleep_time = time.time()

        # Coletar os dados de clima e armazenar com os dados de sono
        temperatura, umidade, condicao = obter_dados_clima(api_key, cidade)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dados_sono.append({
            "timestamp": timestamp,
            "movimentos": movements_detected,
            "despertares": len(awake_periods),
            "temperatura": temperatura,
            "umidade": umidade,
            "condicao": condicao
        })

        # Mostrar o vídeo com a análise em tempo real
        cv2.imshow("Análise de Sono", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Gerar relatório ao final da análise
    gerar_relatorio_com_clima(dados_sono)

# Função para gerar relatório com dados de sono e clima
def gerar_relatorio_com_clima(dados_sono):
    print("\nRelatório de Qualidade do Sono com Dados Climáticos:")
    
    # Gráfico que correlaciona temperatura e despertares
    temperaturas = [entrada['temperatura'] for entrada in dados_sono]
    despertares = [entrada['despertares'] for entrada in dados_sono]
    timestamps = [entrada['timestamp'] for entrada in dados_sono]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, temperaturas, label="Temperatura (°C)", marker='o', color='b')
    plt.plot(timestamps, despertares, label="Despertares", marker='x', color='r')
    plt.xlabel("Horário")
    plt.title("Relação entre Temperatura e Despertares")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
