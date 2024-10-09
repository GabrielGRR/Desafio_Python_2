from pypdf import PdfReader
import pyttsx3
from gtts import gTTS
import tkinter as tk

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
root.title("mPD player | PDf player")

# Definindo o tamanho inicial da janela
root.geometry("400x300")

# Criando a caixa branca (Canvas)
canvas = tk.Canvas(root, width=150, height=100, bg='white')
canvas.pack(side="top", padx=10, pady=10)

# Executando a janela
root.mainloop()
