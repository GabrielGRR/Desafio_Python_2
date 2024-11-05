from pypdf import PdfReader
import pyttsx3
import tkinter as tk
from tkinter import filedialog
import pygame
import os
import time
import threading

class PDFPlayer:
    def __init__(self, root):
        self.palavras_linha = 13
        self.filename = ""
        self.current_page = 1
        self.number_of_pages = 1
        self.is_dragging_slider = False
        self.music_loaded = False

        self.root = root
        self.root.title("mPD player | PD_f player")
        self.root.geometry("")  # fit to content
        self.root.minsize(400, 400)
        self.root.maxsize(700,700)
        self.root.iconbitmap(default='docs/images/OrangePD_icon2.ico')

        self.sound_current = 'results/sound/current.wav'

        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join("results/sound", "pdf.wav"))

        self.page_text, self.number_of_pages = self.pdf_conversion(self.current_page, self.filename)

        # Crie um Frame para encapsular o Label
        self.text_frame = tk.Frame(self.root, width=600, height=400)
        self.text_frame.pack_propagate(False)  # Impede que o Frame redimensione para caber no conteúdo
        self.text_frame.pack(side=tk.TOP, padx=10, pady=10, expand=True, fill="both")

        # Crie o Label dentro do Frame
        self.text_label = tk.Label(self.text_frame, text="", font=("Arial", 10), relief="sunken")
        self.text_label.pack(expand=True, fill="both")


        self.update_text_label(self.page_text, self.palavras_linha)

        self.audio_slider = tk.Scale(self.root, from_=0, to=self.audio_lenght(), orient='horizontal', length=500, sliderlength=20, showvalue=0)
        self.audio_slider.pack(pady=5)
        self.audio_slider.bind("<ButtonPress-1>", self.slider_click)
        self.audio_slider.bind("<ButtonRelease-1>", self.slider_release)

        lower_frame = tk.Frame(self.root)
        lower_frame.pack(side=tk.LEFT, expand=True, fill="x", pady=(0, 10))

        self.page_input = tk.Text(lower_frame, height=1, width=4)
        self.page_input.pack(side=tk.LEFT, anchor="w", padx=(10, 0))
        self.page_input.bind("<Return>", self.process_input)
        self.page_input.delete("1.0", "2.0")
        self.page_input.insert("1.0", f"{self.current_page}")

        self.page_label = tk.Label(lower_frame, text=f"/{self.number_of_pages}", font=("Arial", 10))
        self.page_label.pack(side=tk.LEFT, anchor="w")

        button_frame = tk.Frame(lower_frame)
        button_frame.pack(side=tk.LEFT, anchor="center", expand=True)

        btn_prev = tk.Button(button_frame, text="Prev", command=self.prev_sound)
        btn_prev.pack(side=tk.LEFT, padx=3)

        self.btn_play_pause = tk.Button(button_frame, text="Play", command=self.play_pause)
        self.btn_play_pause.pack(side=tk.LEFT, padx=3)

        btn_next = tk.Button(button_frame, text="Next", command=self.next_sound)
        btn_next.pack(side=tk.LEFT, padx=3)

        select_file = tk.Button(lower_frame, text="Select PDF", command=self.browse_file)
        select_file.pack(side=tk.BOTTOM, anchor="e", padx=10)

        threading.Thread(target=self.position_updater, daemon=True).start()

    def pdf_conversion(self, num_page: int, filename: str):
        try:
            reader = PdfReader(filename)
            self.number_of_pages = len(reader.pages)
            page = reader.pages[num_page]
            text = page.extract_text()
        except:
            text = "Selecione um arquivo PDF"
            self.number_of_pages = 1
        tts = pyttsx3.init()
        tts.save_to_file(text, 'results/sound/current.wav')
        tts.runAndWait()
        print(text)
        return text, self.number_of_pages

    def paused_pos(self):
        current_pos = self.audio_slider.get()
        return current_pos

    def position_updater(self, val=None):
        while True:
            time.sleep(1)
            if self.is_playing() and not self.is_dragging_slider:
                pos = self.audio_slider.get() + 1
                self.audio_slider.set(pos)
                self.checar_threads()

    def slider_click(self, event=None):
        self.is_dragging_slider = True
        pygame.mixer.music.stop()

    def slider_release(self, event=None):
        if self.is_dragging_slider:
            pygame.mixer.music.play(loops=0, start=self.paused_pos())
            pygame.mixer.music.set_pos(self.paused_pos())
            self.is_dragging_slider = False

    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def play_pause(self):
        try:
            if not self.music_loaded:
                pygame.mixer.music.play(loops=0, start=0)
                self.btn_play_pause.config(text="Pause")
                self.music_loaded = True
                print('esteve aqui 1')

            elif not self.is_playing():
                self.audio_slider.set(self.paused_pos())
                pygame.mixer.music.unpause()
                self.btn_play_pause.config(text="Pause")
                print('esteve aqui 2')

            else:
                pygame.mixer.music.pause()
                self.btn_play_pause.config(text="Play")
                print('esteve aqui 3')

        except Exception as e:
            print(f"play music failed: {e}")

    def checar_threads(self):
        threads_ativas = threading.enumerate()
        print(f"Total de threads ativas: {len(threads_ativas)}")
        print("Lista de threads:")
        for thread in threads_ativas:
            print(f"- {thread.name} (daemon: {thread.daemon})")

    def prev_sound(self):
        try:
            if self.current_page != 1:
                self.current_page -= 1
                self.new_page_conversion(self.current_page, 'results/sound/current.wav', self.filename)
            else:
                print("current page is already 1")
        except:
            print("prev sound failed")

    def next_sound(self):
        try:
            if self.current_page != self.number_of_pages:
                self.current_page += 1
                self.new_page_conversion(self.current_page, 'results/sound/current.wav', self.filename)
            else:
                print("current page is already last")
        except:
            print("next sound failed")

    def update_text_label(self, new_text: list, palavras_linha):
        lines = new_text.split()

        total_count = 0
        word_counter = 0
        for _ in lines:
            word_counter += 1
            if word_counter == palavras_linha:
                lines.insert(total_count, "\n")
                word_counter = 0
            total_count += 1

        text_content = " ".join(lines)
        self.text_label.config(text=text_content)

    def process_input(self, event=None):
        new_page = int(self.page_input.get("1.0", "end-1c"))
        if 1 <= new_page <= self.number_of_pages:
            self.new_page_conversion(new_page, 'results/sound/current.wav', self.filename)
            self.current_page = new_page
        else:
            print("Invalid page number")

    def new_page_conversion(self, current_page, sound_current, filename):
        pygame.mixer.music.unload()
        new_text, _ = self.pdf_conversion(current_page, filename)
        pygame.mixer.music.load(sound_current)
        self.update_text_label(new_text, self.palavras_linha)
        self.audio_slider.set(0)
        pygame.mixer.music.play(loops=0, start=0)
        self.btn_play_pause.config(text="Pause")
        self.page_input.delete("1.0", "2.0")
        self.page_input.insert("1.0", f"{current_page}")
        self.audio_slider.configure(to=self.audio_lenght())

    def audio_lenght(self):
        audio_file_lenght = pygame.mixer.Sound(self.sound_current).get_length()
        print(audio_file_lenght)
        return audio_file_lenght

    def browse_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("PDF files", "*.pdf*"), ("all files", "*.*")))

        if filename != "":
            self.current_page = 1
            self.new_page_conversion(self.current_page, 'results/sound/current.wav', filename)
            self.page_label.config(text=f"/{self.number_of_pages}")
            self.filename = filename

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFPlayer(root)
    root.mainloop()