from pypdf import PdfReader
import pyttsx3
# from gtts import gTTS
import tkinter as tk
from tkinter import filedialog
import pygame
import os
import time
import threading

palavras_linha = 13

filename = ""

## Conversão PDF
def pdf_conversion(num_page: int):
    ## Transformar PDF em TXT
    global filename, number_of_pages
    try:
        reader = PdfReader(filename)
        number_of_pages = len(reader.pages) # não obrigatório
        page = reader.pages[num_page] # seleciona a página que você quer que seja transcrito
        text = page.extract_text()
    except:
        text = "Selecione um arquivo PDF"
        number_of_pages = 1
        print("deu ruim")

    ## Text to Speech (TTS)
    tts = pyttsx3.init()
    tts.save_to_file(text, 'sound/current.wav')
    tts.runAndWait()

    # ALTERNATIVA: google text to speech \/
    # tts = gTTS(text, lang='pt')
    # tts.save('audio2.wav')
    return text, number_of_pages

current_page = 1

page_text, number_of_pages = pdf_conversion(current_page)

## Criando interface gráfica (GUI) com o tkinter
# Criando a janela principal
root = tk.Tk()
root.title("mPD player | PD_f player")

# Definindo o tamanho inicial da janela
root.geometry("") # fit to content
root.minsize(400,400)

root.iconbitmap(default='OrangePD_icon2.ico')

sound_current = 'sound/current.wav'

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
            print('esteve aqui 1')

        elif not is_playing():
            #file_path = tk.filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
            audio_slider.set(paused_pos())
            pygame.mixer.music.unpause()  # Tocar do ponto onde foi pausado
            btn_play_pause.config(text="Pause")  # Atualiza o texto entre "Play" e "Pause"
            print('esteve aqui 2')

        else:
            pygame.mixer.music.pause()  # Pausa o áudio   
            btn_play_pause.config(text="Play")  # Atualiza o texto entre "Play" e "Pause"
            print('esteve aqui 3')

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
    global current_page
    try:
        if current_page != 1:
            current_page-=1
            pygame.mixer.music.unload()
            new_text, _ = pdf_conversion(current_page)
            pygame.mixer.music.load(sound_current)
            update_text_label(new_text)
            audio_slider.set(0)
            pygame.mixer.music.play(loops=0, start=0)
            btn_play_pause.config(text="Pause")
            page_input.delete("1.0","2.0")
            page_input.insert("1.0",f"{current_page}")
            audio_slider.configure(to=audio_lenght())
        else:
            print("current page is already 1")
    except:
        print("prev sound failed")

def next_sound():
    global current_page, number_of_pages
    try:
        if current_page != number_of_pages:
            current_page+=1
            pygame.mixer.music.unload()
            new_text, _ = pdf_conversion(current_page)
            pygame.mixer.music.load(sound_current)
            update_text_label(new_text)
            audio_slider.set(0)
            pygame.mixer.music.play(loops=0, start=0)
            btn_play_pause.config(text="Pause")
            page_input.delete("1.0","2.0")
            page_input.insert("1.0",f"{current_page}")
            audio_slider.configure(to=audio_lenght())
        else:
            print("current page is already last")
    except:
        print("next sound failed")


def update_text_label(new_text: list):
    global palavras_linha
    lines = new_text.split() 

    total_count = 0
    word_counter = 0
    for _ in lines:
        word_counter+=1
        if word_counter == palavras_linha:
            lines.insert(total_count,"\n")
            word_counter=0
        total_count+=1

    text_content = " ".join(lines)
    text_label.config(text=text_content)

def process_input(event=None):
    global current_page
    try:
        new_page = int(page_input.get("1.0", "end-1c"))
        if 1 <= new_page <= number_of_pages:
            current_page = new_page
            pygame.mixer.music.unload()
            new_text, _ = pdf_conversion(current_page)
            pygame.mixer.music.load(sound_current)
            update_text_label(new_text)
            audio_slider.set(0)
            pygame.mixer.music.play(loops=0, start=0)
            btn_play_pause.config(text="Pause")
            page_input.delete("1.0","2.0")
            page_input.insert("1.0",f"{current_page}")
            audio_slider.configure(to=audio_lenght())

        else:
            print("Invalid page number")
    except ValueError:
        print("Invalid input")

## texto

text_content = ""

# Cria um Label com o texto completo
text_label = tk.Label(root, text=text_content, font=("Arial",10), relief="sunken") ####mudar fonte?
text_label.pack(side=tk.TOP, padx=10, pady=10,expand=True,fill="both")  # Adiciona o Label à janela principal

update_text_label(page_text)


# Criar um slider para a posição do áudio
def audio_lenght():

    audio_file_lenght = pygame.mixer.Sound(sound_current).get_length()
    print(audio_file_lenght)
    return audio_file_lenght


#como já tem thread ativa, irá dar conflitor se add o command=position_updater
audio_slider = tk.Scale(root, from_=0, to=audio_lenght(), orient='horizontal',length=500, sliderlength=20, showvalue=0) 
audio_slider.pack(pady=5)

# Vincular os eventos de clique e soltura no slider
audio_slider.bind("<ButtonPress-1>", slider_click)  # Quando o slider é clicado
audio_slider.bind("<ButtonRelease-1>", slider_release)  # Quando o slider é solto

lower_frame = tk.Frame(root)
lower_frame.pack(side=tk.LEFT, expand=True, fill="x",pady=(0,10))

page_input = tk.Text(lower_frame, height=1, width=4)
page_input.pack(side=tk.LEFT, anchor="w", padx=(10,0))
page_input.bind("<Return>", process_input)

page_input.delete("1.0","2.0")
page_input.insert("1.0",f"{current_page}")

page_label = tk.Label(lower_frame, text=f"/{number_of_pages}", font=("Arial",10)) ####mudar fonte?
page_label.pack(side=tk.LEFT, anchor="w")

# Frame para alinhar os botões na mesma linha
button_frame = tk.Frame(lower_frame)
button_frame.pack(side=tk.LEFT, anchor="center", expand=True)


btn_prev = tk.Button(button_frame, text="Prev", command=prev_sound)
btn_prev.pack(side=tk.LEFT, padx=3)

# Play_pause twavle button
btn_play_pause = tk.Button(button_frame, text="Play", command=play_pause)
btn_play_pause.pack(side=tk.LEFT, padx=3)

btn_next = tk.Button(button_frame, text="Next", command=next_sound)
btn_next.pack(side=tk.LEFT, padx=3)


def browse_file():
    global filename
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("PDF files","*.pdf*"),("all files","*.*")))
    print(filename)
    
    if filename != "":
        current_page=1
        pygame.mixer.music.unload()
        new_text, number_of_pages = pdf_conversion(current_page)
        pygame.mixer.music.load(sound_current)
        update_text_label(new_text)
        audio_slider.set(0)
        pygame.mixer.music.play(loops=0, start=0)
        btn_play_pause.config(text="Pause")
        page_input.delete("1.0","2.0")
        page_input.insert("1.0",f"{current_page}")
        page_label.config(text=f"/{number_of_pages}")
        audio_slider.configure(to=audio_lenght())


select_file = tk.Button(lower_frame, text="Select PDF",command=browse_file)
select_file.pack(side=tk.BOTTOM,anchor="e", padx=10)


# Executando a janela
root.mainloop()