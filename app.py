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
lines = text.split()

palavras_linha = 10
count = 0 

for line in lines:
    if count == 15:
        lines.insert(palavras_linha,'\n')
        count = -1
    count +=1
    palavras_linha+=1

text_content = " ".join(lines)

print(text_content)

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

# Função para tocar o arquivo MP3
# def play_sound():
#     file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
#     if file_path:
#         pygame.mixer.music.load(file_path)
#         pygame.mixer.music.play()

sound_prev = 'sound/prev.mp3'
sound_current = 'sound/current.wav'
sound_next = 'sound/next.mp3'

# Inicializando o pygame
pygame.mixer.init()

# Variável para armazenar a posição onde o áudio foi pausado
paused_position = 0
is_paused = False  # Variável para verificar se o áudio está pausado

## funções para os botões da interface
def play_sound():
    global is_paused, paused_position
    
    try:
        if is_paused:  # Se o áudio estava pausado, continua de onde parou
            pygame.mixer.music.unpause()
            is_paused = False
        elif not pygame.mixer.music.get_busy():
            #file_path = tk.filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
            pygame.mixer.music.load(os.path.join("sound", "current.wav"))
            pygame.mixer.music.play(loops=0, start=paused_position)  # Tocar do ponto onde foi pausado
            is_paused = False

    except Exception as e:
        print(f"play music failed: {e}")

def pause_sound():
    try:
        global is_paused, paused_position

        if pygame.mixer.music.get_busy():  # Se o áudio está tocando
            pygame.mixer.music.pause()  # Pausa o áudio
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
tk_text = tk.Label(root, text=text_content).grid(row=0,column=1)
#tk_text = tk.Label(root, text=text).grid(row=0,column=1)


# Executando a janela
root.mainloop()
