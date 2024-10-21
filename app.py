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
n = 215
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

# Variável para armazenar a posição onde o áudio foi pausado
paused_position = 0
is_paused = False  # Variável para verificar se o áudio está pausado

# Função para atualizar a posição do slider enquanto a música toca
def atualizar_slider_posicao():
    while pygame.mixer.music.get_busy():  # Enquanto a música estiver tocando
        pos = pygame.mixer.music.get_pos() / 1000  # Pega a posição atual (em milissegundos) e converte para segundos
        audio_slider.set(pos)  # Atualiza o slider de posição
        time.sleep(1)  # Atualiza a cada 1 segundo

# Função para ajustar a posição do áudio
def ajustar_posicao(val):
    pos = int(val)  # Pega a posição do slider (em segundos)
    pygame.mixer.music.play(loops=0, start=pos)  # Reproduz a partir da nova posição


## funções para os botões da interface
def play_sound():
    global is_paused, paused_position
    
    try:
        if not pygame.mixer.music.get_busy():
            #file_path = tk.filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
            pygame.mixer.music.load(os.path.join("sound", "current.wav"))
            pygame.mixer.music.play(loops=0, start=paused_position)  # Tocar do ponto onde foi pausado
            btn_play_pause.config(text="Pause")  # Atualiza o texto entre "Play" e "Pause"
            is_paused = False
            # Iniciar a atualização do slider de posição em uma nova thread
        elif is_paused:  # Se o áudio estava pausado, continua de onde parou
            pygame.mixer.music.unpause()
            btn_play_pause.config(text="Pause")  # Atualiza o texto entre "Play" e "Pause"
            is_paused = False
        else:
            pause_sound()

    except Exception as e:
        print(f"play music failed: {e}")

def pause_sound():
    try:
        global is_paused, paused_position

        if pygame.mixer.music.get_busy():  # Se o áudio está tocando
            pygame.mixer.music.pause()  # Pausa o áudio
            btn_play_pause.config(text="Play")  # Atualiza o texto entre "Play" e "Pause"
            paused_position = pygame.mixer.music.get_pos() / 1000.0  # Salva a posição atual (em segundos)
            is_paused = True
    except:
        print("pause music failed")

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
audio_slider = tk.Scale(root, from_=0, to=audio_lenght, orient='horizontal',length=500, command=ajustar_posicao, showvalue=0)
audio_slider.pack(pady=10)

# Frame para alinhar os botões na mesma linha
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM)

# fazer este botão virar toggle
btn_prev = tk.Button(button_frame, text="Prev", command=prev_sound)
btn_prev.pack(side=tk.LEFT, padx=3)

# TODO: transformar esse botão em toggle e remover o pause
btn_play_pause = tk.Button(button_frame, text="Play", command=play_sound)
btn_play_pause.pack(side=tk.LEFT, padx=3)

btn_next = tk.Button(button_frame, text="Next", command=next_sound)
btn_next.pack(side=tk.LEFT, padx=3)

# Executando a janela
root.mainloop()