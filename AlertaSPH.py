import pyaudio
import numpy as np
import time
import threading
import pygame
import logging

# Configuração do logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

audio_playing = False
threshold = 10

def audio_callback(in_data, frame_count, time_info, status):
    global audio_playing
    try:
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        volume_norm = np.linalg.norm(audio_data) * 10
        logging.debug(f"Volume atual: {volume_norm}")

        if volume_norm > threshold and not audio_playing:
            threading.Thread(target=play_alert_sound).start()
    except Exception as e:
        logging.error(f"Erro no callback de áudio: {e}")

    return (in_data, pyaudio.paContinue)

def play_alert_sound():
    global audio_playing
    logging.debug("Iniciando reprodução de alerta")
    audio_playing = True

    try:
        pygame.mixer.init()
        pygame.mixer.music.load("Alerta.wav")
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        logging.error(f"Erro ao reproduzir o áudio: {e}")
    finally:
        audio_playing = False
        logging.debug("Reprodução de alerta concluída")

def main():
    logging.info("Iniciando monitoramento de áudio...")
    logging.info("Pressione Ctrl+C para interromper o programa.")
    
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=44100,
                        input=True,
                        stream_callback=audio_callback)

        stream.start_stream()

        while stream.is_active():
            time.sleep(1)

    except KeyboardInterrupt:
        logging.info("Programa interrompido pelo usuário.")
    except Exception as e:
        logging.error(f"Erro no fluxo de entrada de áudio: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        logging.info("Monitoramento de áudio encerrado.")

if __name__ == "__main__":
    main()
