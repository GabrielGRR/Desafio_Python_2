from pypdf import PdfReader
import pyttsx3
from gtts import gTTS
import tkinter as tk
import pygame
import os
import time
import threading

## Transformar PDF em TXT
reader = PdfReader("O Programador Pragmatico.pdf") # Caminho relativo
number_of_pages = len(reader.pages) # não obrigatório
n = 6
page = reader.pages[n] # seleciona a página que você quer que seja transcrito
text = page.extract_text()

# TODO: ?adicionar buffer da proxima pagina?

## Text to Speech (TTS) e 
tts = pyttsx3.init()
tts.save_to_file(text, 'sound/current.wav')
#tts.say(text) # não salva o MP3, reproduz diretamente
tts.runAndWait()

# ALTERNATIVA: google text to speech \/
# tts = gTTS(text, lang='pt')
# tts.save('audio2.mp3')

## Criando interface gráfica (GUI) com o tkinter

# Criando a janela principal
root = tk.Tk()
root.title("mPD player | PD_f player")

# Definindo o tamanho inicial da janela
root.geometry("") # fit to content

sound_prev = 'sound/prev.mp3'
sound_current = 'sound/current.wav'
sound_next = 'sound/next.mp3'

# Inicializando o pygame
pygame.mixer.init()

pygame.mixer.music.load(os.path.join("sound", "current.wav"))
# Variável para armazenar a posição onde o áudio foi pausado

paused_pos = 0.0

def paused_position_updater():
    global paused_pos
    while True:  # Enquanto a música estiver tocando
        paused_pos = pygame.mixer.music.get_pos() / 1000  # Pega a posição atual (em milissegundos) e converte para segundos
        time.sleep(0.2)  # Atualiza a cada 1 segundo
        print(paused_pos)

def is_playing():
    return pygame.mixer.music.get_busy()


music_loaded = False

## funções para os botões da interface
def play_pause():
    global paused_pos, thread_created, music_loaded
    
    try:
        if not music_loaded: #start music
            pygame.mixer.music.play(loops=0, start=0)  # Tocar do ponto onde foi pausado
            btn_play_pause.config(text="Pause")  # Atualiza o texto entre "Play" e "Pause"
            threading.Thread(target=paused_position_updater, daemon=True).start()
            checar_threads()
            music_loaded = True

        if not is_playing():
            #file_path = tk.filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
            pygame.mixer.music.unpause()  # Tocar do ponto onde foi pausado
            audio_slider.set(paused_pos)
            btn_play_pause.config(text="Pause")  # Atualiza o texto entre "Play" e "Pause"
            checar_threads()

        else:
            paused_pos = pygame.mixer.music.get_pos() / 1000
            pygame.mixer.music.pause()  # Pausa o áudio
            
            btn_play_pause.config(text="Play")  # Atualiza o texto entre "Play" e "Pause"

            print(paused_pos)
            checar_threads()

    except Exception as e:
        print(f"play music failed: {e}")


# Função para verificar quantas threads estão ativas
def checar_threads():
    threads_ativas = threading.enumerate()  # Retorna uma lista de threads ativas
    print(f"Total de threads ativas: {len(threads_ativas)}")
    print("Lista de threads:")
    for thread in threads_ativas:
        print(f"- {thread.name} (daemon: {thread.daemon})")

def prev_sound():
    try:
        pygame.mixer.music.unload()
        pygame.mixer.music.load(sound_prev)
    except:
        print("prev sound failed")

def next_sound():
    try:
        pygame.mixer.music.unload()
        pygame.mixer.music.load(sound_next)
    except:
        print("next sound failed")


## Botões
lines = text.split() 
palavras_linha = 10  # Quantidade de palavras por linha
count = 0  # Contador para limitar a criação de frames
max_words_per_frame = 15  # Quantidade de palavras por frame

# Variável para armazenar o frame atual
text_frame = None

for index, line in enumerate(lines):
    if count == 0:  # Quando o count for 0, cria um novo frame
        text_frame = tk.Frame(root)
        text_frame.pack(side=tk.TOP, pady=0)  # Cria um novo frame e empilha

    # Cria um botão com o texto
    text_container = tk.Button(text_frame, text=line, bd=0, highlightthickness=0, pady=0, width=len(line))
    text_container.pack(side=tk.LEFT, padx=0, pady=0)  # Adiciona o botão ao frame atual

    count += 1

    # Quando atinge o limite de palavras por frame, reinicia o contador
    if count == max_words_per_frame:
        count = 0  # Reseta o contador para criar um novo frame no próximo loop

# TODO: apagar dps?
text_content = " ".join(lines)
print(text_content)


#### TODO: slider volume?

# Criar um slider para a posição do áudio
audio_lenght = pygame.mixer.Sound("sound/current.wav").get_length()
print(audio_lenght)
audio_slider = tk.Scale(root, from_=0, to=audio_lenght, orient='horizontal',length=500,  showvalue=0) #command=atualizar_pos_slider,
audio_slider.pack(pady=10)

# Frame para alinhar os botões na mesma linha
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM)

btn_prev = tk.Button(button_frame, text="Prev", command=prev_sound)
btn_prev.pack(side=tk.LEFT, padx=3)

# Play_pause toggle button
btn_play_pause = tk.Button(button_frame, text="Play", command=play_pause)
btn_play_pause.pack(side=tk.LEFT, padx=3)

btn_next = tk.Button(button_frame, text="Next", command=next_sound)
btn_next.pack(side=tk.LEFT, padx=3)

# Executando a janela
root.mainloop()