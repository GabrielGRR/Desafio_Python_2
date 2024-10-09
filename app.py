from pypdf import PdfReader
import pyttsx3
from gtts import gTTS
import tkinter as tk
from tkinter import filedialog
import pygame

## Transformar PDF em TXT
reader = PdfReader("O Programador Pragmatico.pdf") # Caminho relativo
number_of_pages = len(reader.pages) # não obrigatório
n = 217
page = reader.pages[n] # seleciona a página que você quer que seja transcrito
text = page.extract_text()
print(text)
# TODO: ?adicionar buffer da proxima pagina?


## Text to Speech (TTS) e 
tts = pyttsx3.init()
tts.save_to_file(text, 'audio.mp3')
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

# Criando a caixa branca (Canvas)
canvas = tk.Canvas(root, width=150, height=100, bg='white')
canvas.pack(side="top", padx=10, pady=10)

# Função para tocar o arquivo MP3
def play_music():
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

# Botão para selecionar e tocar música
btn_play = tk.Button(root, text="Tocar MP3", command=play_music)
btn_play.pack(pady=20)

# Executando a janela
root.mainloop()
