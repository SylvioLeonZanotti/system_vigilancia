import cv2
from ultralytics import YOLO

def iniciar_video(video_source):
    # Carregar o modelo YOLOv8
    model = YOLO('yolov8n.pt')

    # Captura de vídeo
    cap = cv2.VideoCapture(video_source)

    paused = False
    frame_count = 0

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break

            # PELO AMOR DE DEUS NÃO MEXE MAIS NISSO AQUI PORQUE POR ALGUM MOTIVO OBSCURO O FPS VAI EMBORA QUANDO REDIMENSIONO A IMAGEM
            # PS: lembrar de procurar formas de otimizar o processamento de análise de imagens sem gpus dedicadas atuais
            h, w = frame.shape[:2]
            max_dim = 1200
            if h > max_dim or w > max_dim:
                scale = min(max_dim / h, max_dim / w)
                frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

            results = model(frame)

            # processo de detecções
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    if box.cls == 0:  # classe 0 é pessoa por padrão
                        x1, y1, x2, y2 = box.xyxy[0].numpy()
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                        label = "Pessoa"
                        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                        cv2.rectangle(frame, (int(x1), int(y1) - 20), (int(x1) + w, int(y1)), (0, 255, 0), -1)
                        cv2.putText(frame, label, (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

            # Instruções na tela
            instructions = "'p' para pausar/retomar | 's' para salvar frame | 'q' para sair"
            cv2.putText(frame, instructions, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

            # Mostrar o frame com as detecções e instruções
            cv2.imshow('Detecção de Pessoas', frame)

        # Controles de interface
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):  # Sair
            break
        elif key == ord('p'):  # Pausar/retomar o vídeo
            paused = not paused
        elif key == ord('s') and not paused:  # Salvar o quadro atual como imagem
            frame_count += 1
            cv2.imwrite(f'frame_salvo_{frame_count}.jpg', frame)
            print(f"Quadro salvo como frame_salvo_{frame_count}.jpg")

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()
