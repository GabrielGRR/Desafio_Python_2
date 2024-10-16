from pypdf import PdfReader
import pyttsx3
from gtts import gTTS
import tkinter as tk
import pygame
import os

## Transformar PDF em TXT
reader = PdfReader("O Programador Pragmatico.pdf") # Caminho relativo
number_of_pages = len(reader.pages) # não obrigatório
n = 215
page = reader.pages[n] # seleciona a página que você quer que seja transcrito
text = page.extract_text()
print(text)
# TODO: ?adicionar buffer da proxima pagina?



## Text to Speech (TTS) e 
tts = pyttsx3.init()
tts.save_to_file(text, 'sound/current.mp3')
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
root.geometry("400x300")

# Função para tocar o arquivo MP3
# def play_sound():
#     file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
#     if file_path:
#         pygame.mixer.music.load(file_path)
#         pygame.mixer.music.play()

sound_prev = 'sound/prev.mp3'
sound_current = 'sound/current.mp3'
sound_next = 'sound/next.mp3'

# Inicializando o pygame
pygame.mixer.init()

# Variável para armazenar a posição onde o áudio foi pausado
paused_position = 0
is_paused = False  # Variável para verificar se o áudio está pausado

## funções para os botões da interface
def play_sound():
    try:
        sound = pygame.mixer.Sound(sound_current)
        sound.play()
    except:
        print("play music failed")

def pause_sound():
    try:
        pygame.mixer.pause() #não está pausando, está PARANDO
    except:
        print("pause music failed")

def prev_sound():
    try:
        pygame.mixer.music.load(sound_prev)
    except:
        print("prev sound failed")

def next_sound():
    try:
        pygame.mixer.music.load(sound_next)
    except:
        print("next sound failed")

# input box (escolher pagina)
# mute
# slider volume

## Botões
# fazer este botão virar toggle
btn_play = tk.Button(root, text="Play", command=play_sound)
btn_play.grid(row=1, column=1) #pady="20"

btn_pause = tk.Button(root, text="Pause", command=pause_sound)
btn_pause.grid(row=1, column=2)

btn_next = tk.Button(root, text="Next", command=next_sound)
btn_next.grid(row=1, column=3)

btn_prev = tk.Button(root, text="Prev", command=prev_sound)
btn_prev.grid(row=1, column=0)

# Texto
tk_text = tk.Label(root, text="hello world").grid(row=0,column=1)
#tk_text = tk.Label(root, text=text).grid(row=0,column=1)


# Executando a janela
root.mainloop()
