from pypdf import PdfReader
import pyttsx3
# from gtts import gTTS
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
#tts.say(text) # não salva o wav, reproduz diretamente
tts.runAndWait()

# ALTERNATIVA: google text to speech \/
# tts = gTTS(text, lang='pt')
# tts.save('audio2.wav')

## Criando interface gráfica (GUI) com o tkinter

# Criando a janela principal
root = tk.Tk()
root.title("mPD player | PD_f player")

# Definindo o tamanho inicial da janela
root.geometry("") # fit to content

sound_prev = 'sound/prev.wav'
sound_current = 'sound/current.wav'
sound_next = 'sound/next.wav'

# Inicializando o pygame
pygame.mixer.init()

pygame.mixer.music.load(os.path.join("sound", "current.wav"))
# Variável para armazenar a posição onde o áudio foi pausado

is_dragging_slider = False

def paused_pos():
    current_pos = audio_slider.get()
    # pygame.mixer.music.play(loops=0, start=current_pos)
    return current_pos

def position_updater(val=None): 
    while True:  # Enquanto a música estiver tocando
        time.sleep(1)  # Atualiza a cada 1 segundo
        if is_playing() and not is_dragging_slider:
            pos = audio_slider.get()+1  # Pega a posição atual (em milissegundos) e converte para segundos
            audio_slider.set(pos)
            print()
            checar_threads()

threading.Thread(target=position_updater, daemon=True).start()

# Função chamada quando o slider é clicado (começa o arrasto)
def slider_click(event=None):
    global is_dragging_slider
    is_dragging_slider = True  # O slider está sendo arrastado
    pygame.mixer.music.stop()

# Função chamada quando o slider é solto (termina o arrasto)
def slider_release(event=None):
    global is_dragging_slider
    if is_dragging_slider:
        pygame.mixer.music.play(loops=0, start=paused_pos())  # Tocar do ponto onde foi pausado
        pygame.mixer.music.set_pos(paused_pos())
        is_dragging_slider = False  # O slider não está mais sendo arrastado

def is_playing():
    return pygame.mixer.music.get_busy()

music_loaded = False

## funções para os botões da interface
def play_pause():
    global thread_created, music_loaded
    
    try:
        if not music_loaded: #start music
            pygame.mixer.music.play(loops=0, start=0)  # Tocar do ponto onde foi pausado
            btn_play_pause.config(text="Pause")  # Atualiza o texto entre "Play" e "Pause"
            music_loaded = True

        elif not is_playing():
            #file_path = tk.filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
            audio_slider.set(paused_pos())
            pygame.mixer.music.unpause()  # Tocar do ponto onde foi pausado
            btn_play_pause.config(text="Pause")  # Atualiza o texto entre "Play" e "Pause"

        else:
            pygame.mixer.music.pause()  # Pausa o áudio   
            btn_play_pause.config(text="Play")  # Atualiza o texto entre "Play" e "Pause"

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


## texto
lines = text.split() 
palavras_linha = 13  # Quantidade de palavras por linha

# Variável para armazenar o texto completo
full_text = ""

total_count = 0
word_counter = 0
for word in lines:
    word_counter+=1
    if word_counter == palavras_linha:
        lines.insert(total_count,"\n")
        word_counter=0
    total_count+=1

text_content = " ".join(lines)
print(text_content)

# Cria um Label com o texto completo
text_label = tk.Label(root, text=text_content, font=("Arial",10), relief="sunken") ####mudar fonte?
text_label.pack(side=tk.TOP, padx=10, pady=10)  # Adiciona o Label à janela principal


# Criar um slider para a posição do áudio
audio_lenght = pygame.mixer.Sound("sound/current.wav").get_length()
print(audio_lenght)


#como já tem thread ativa, irá dar conflitor se add o command=position_updater
audio_slider = tk.Scale(root, from_=0, to=audio_lenght, orient='horizontal',length=500, sliderlength=20, showvalue=0) 
audio_slider.pack(pady=10)

# Vincular os eventos de clique e soltura no slider
audio_slider.bind("<ButtonPress-1>", slider_click)  # Quando o slider é clicado
audio_slider.bind("<ButtonRelease-1>", slider_release)  # Quando o slider é solto


# Frame para alinhar os botões na mesma linha
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM)

btn_prev = tk.Button(button_frame, text="Prev", command=prev_sound)
btn_prev.pack(side=tk.LEFT, padx=3)

# Play_pause twavle button
btn_play_pause = tk.Button(button_frame, text="Play", command=play_pause)
btn_play_pause.pack(side=tk.LEFT, padx=3)

btn_next = tk.Button(button_frame, text="Next", command=next_sound)
btn_next.pack(side=tk.LEFT, padx=3)

# Executando a janela
root.mainloop()