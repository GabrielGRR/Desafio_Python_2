# Bibliotecas padrão
import os
import time
import threading

# Bibliotecas Externas
from pypdf import PdfReader
import pyttsx3
import pygame
import tkinter as tk
from tkinter import filedialog

class PDFPlayer:
    """
    Uma classe para criar um audio player de PDF usando Tkinter.

    Uso esperado:
        root = tk.Tk()
        app = PDFPlayer(root)
        root.mainloop()
    """    

    def __init__(self, root: object):
        
        # Definição dos parâmetros da instância da classe (Equivalente a variáveis globais, mas dentro de uma classe).
        self.max_palavras_linha = 13
        self.pdf_file_path = ""
        self.current_page = 1
        self.number_of_pages = 1
        self.is_dragging_slider = False
        self.music_loaded = False
        self.current_sound = 'results/sound/current.wav'                
        self.page_text, self.number_of_pages = self.convert_pdf_to_text(self.current_page, self.pdf_file_path)

        self.root = root

        self._InitMixer()
        self._InitGUI()

        threading.Thread(target=self.position_updater, daemon=True).start()

    # Funções de uso interno
    def _InitMixer(self):
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join("results/sound", "pdf.wav"))
        self.convert_text_to_audio(self.page_text)

    def _InitGUI(self):
        """
        Initializes the graphical user interface (GUI) for the application.

        This method sets up the main window, frames, text areas, scrollbars, sliders, 
        and buttons used in the application. It also configures the window properties 
        and necessary widgets.
        """

        # Parâmetros da interface gráfica
        self.root.title("mPD player | PD_f player")
        self.root.geometry("")  # fit to content
        self.root.minsize(400, 400)
        self.root.maxsize(700, 700)
        self.root.iconbitmap(default='docs/images/OrangePD_icon2.ico')        

        # Frame para encapsular o Text
        self.text_frame = tk.Frame(self.root, width=600, height=400)
        self.text_frame.pack_propagate(False)  # Impede que o Frame redimensione para caber no conteúdo
        self.text_frame.pack(side=tk.TOP, 
                             padx=10, 
                             pady=10, 
                             expand=True, 
                             fill="both")

        # Barras de rolagem para textos longos
        self.text_scrollbar = tk.Scrollbar(self.text_frame)
        self.text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Parâmetros do texto
        self.text_widget = tk.Text(self.text_frame, 
                                  font=("Arial", 10), 
                                  relief="sunken", 
                                  wrap=tk.WORD, 
                                  yscrollcommand=self.text_scrollbar.set)
        self.text_widget.pack(expand=True, fill="both")
        self.text_scrollbar.config(command=self.text_widget.yview)
        self.text_widget.tag_configure("center", justify='center')
        self.set_screen_text("Select a PDF file.")

        # Parâmetros do 'slider' de áudio
        self.audio_slider = tk.Scale(self.root, 
                                     from_=0, 
                                     to=self.get_audio_length(), 
                                     orient='horizontal', 
                                     length=500, 
                                     sliderlength=20, 
                                     showvalue=0)
        self.audio_slider.pack(pady=5)
        self.audio_slider.bind("<ButtonPress-1>", self.slider_click)
        self.audio_slider.bind("<ButtonRelease-1>", self.slider_release)

        # Frame para encapsular input da página
        lower_frame = tk.Frame(self.root)
        lower_frame.pack(side=tk.LEFT, expand=True, fill="x", pady=(0, 10))

        # Caixa de input de página
        self.page_input = tk.Entry(lower_frame, width=4)
        self.page_input.pack(side=tk.LEFT, anchor="w", padx=(10, 0))
        self.page_input.bind("<Return>", self.navigate_to_page)
        self.page_input.insert(0, f"{self.current_page}")

        # Complemento da caixa de input de pagina, mostrando o total de páginas daquele PDF
        self.page_label = tk.Label(lower_frame, text=f"/{self.number_of_pages}", font=("Arial", 10))
        self.page_label.pack(side=tk.LEFT, anchor="w")

        # Frame para encapsular os botões, está dentro da frame anterior (lower_frame)
        button_frame = tk.Frame(lower_frame)
        button_frame.pack(side=tk.LEFT, anchor="center", expand=True)

        # Botão de voltar página
        button_prev = tk.Button(button_frame, text="Prev", command=self.prev_page)
        button_prev.pack(side=tk.LEFT, padx=3)

        # Botão de toggle de pausar e tocar áudio
        self.button_play_pause = tk.Button(button_frame, text="Play", command=self.play_pause)
        self.button_play_pause.pack(side=tk.LEFT, padx=3)

        # Botão de avançar página
        button_next = tk.Button(button_frame, text="Next", command=self.next_page)
        button_next.pack(side=tk.LEFT, padx=3)

        # Botão de selecionar arquivo PDF
        select_file = tk.Button(lower_frame, text="Select PDF", command=self.browse_file)
        select_file.pack(side=tk.BOTTOM, anchor="e", padx=10)


    # Métodos 'getter'
    def get_is_playing(self):
        return pygame.mixer.music.get_busy()

    def get_paused_pos(self):
        return self.audio_slider.get()

    def get_audio_length(self):
        return pygame.mixer.Sound(self.current_sound).get_length()
    
    def thread_check(self):
        threads_ativas = threading.enumerate()
        print(f"Total de threads ativas: {len(threads_ativas)}")
        print("Lista de threads:")
        for thread in threads_ativas:
            print(f"- {thread.name} (daemon: {thread.daemon})")


    # Métodos 'Setter'
    def browse_file(self):
        pdf_file_path = filedialog.askopenfilename(initialdir="/", 
                                              title="Select a File", 
                                              filetypes=(("PDF files", "*.pdf*"), ("all files", "*.*")))

        if pdf_file_path != "":
            self.current_page = 1
            self.set_new_page(self.current_page, 'results/sound/current.wav', pdf_file_path)
            self.page_label.config(text=f"/{self.number_of_pages}")
            self.pdf_file_path = pdf_file_path

    def convert_pdf_to_text(self, num_page: int, pdf_file_path: str) -> tuple[str, int]:
        """
        Converts a specified page of a PDF file to text and saves it as an audio file.

        Args:
            num_page (int): The page of the PDF to be converted.
            pdf_file_path (str): The path to the PDF file.

        Returns:
            tuple: A tuple containing the extracted text (str) and the total number of pages (int).
        """

        try:
            reader = PdfReader(pdf_file_path)
            self.number_of_pages = len(reader.pages)
            page = reader.pages[num_page-1]
            text = page.extract_text()
        except:
            text = "Selecione um arquivo PDF"
            self.number_of_pages = 1

        return text, self.number_of_pages
    
    def convert_text_to_audio(self, text: str):
        tts = pyttsx3.init()
        tts.save_to_file(text, 'results/sound/current.wav')
        tts.runAndWait()

    def play_pause(self):
        """Toggles the audio and button between play and pause."""

        try:
            if not self.music_loaded:
                pygame.mixer.music.play(loops=0, start=0)
                self.button_play_pause.config(text="Pause")
                self.music_loaded = True

            elif not self.get_is_playing():
                self.audio_slider.set(self.get_paused_pos())
                pygame.mixer.music.unpause()
                self.button_play_pause.config(text="Pause")

            else:
                pygame.mixer.music.pause()
                self.button_play_pause.config(text="Play")

        except Exception as e:
            print(f"play music failed: {e}")

    def prev_page(self):
        try:
            if self.current_page != 1:
                self.current_page -= 1
                self.set_new_page(self.current_page, 'results/sound/current.wav', self.pdf_file_path)
            else:
                print("current page is already 1")
        except:
            print("prev sound failed")

    def next_page(self):
        try:
            if self.current_page != self.number_of_pages:
                self.current_page += 1
                self.set_new_page(self.current_page, 'results/sound/current.wav', self.pdf_file_path)
            else:
                print("current page is already last")
        except:
            print("next sound failed")

    def navigate_to_page(self, event=None):
        try:
            new_page = int(self.page_input.get())
            if 1 <= new_page <= self.number_of_pages:
                self.set_new_page(new_page, 'results/sound/current.wav', self.pdf_file_path)
                self.current_page = new_page
            else:
                print("Invalid page number")
        except ValueError:
            print("Invalid input")

    def position_updater(self, val=None):
        """Continuously updates the position of the audio slider."""

        while True:
            time.sleep(1)
            if self.get_is_playing() and not self.is_dragging_slider:
                pos = self.audio_slider.get() + 1
                self.audio_slider.set(pos)
                self.thread_check()

    # Slider mouse events binded to MB1
    def slider_click(self, event=None):
        self.is_dragging_slider = True
        pygame.mixer.music.stop()
    def slider_release(self, event=None):
        if self.is_dragging_slider:
            pygame.mixer.music.play(loops=0, start=self.get_paused_pos())
            pygame.mixer.music.set_pos(self.get_paused_pos())
            self.is_dragging_slider = False

    def set_screen_text(self, new_text: list):
        total_count = 0
        word_counter = 0
        lines = new_text.split()
        for _ in lines:
            word_counter += 1
            if word_counter == self.max_palavras_linha:
                lines.insert(total_count, "\n")
                word_counter = 0
            total_count += 1
        text_content = " ".join(lines)

        # Apaga o texto anterior e adiciona o atual
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, text_content)
        self.text_widget.tag_add("center", "1.0", "end")
        self.text_widget.config(state=tk.DISABLED)
        
    def set_new_page(self, current_page: int, sound_file_path: str, pdf_file_path: str):

        pygame.mixer.music.unload()

        new_text, _ = self.convert_pdf_to_text(current_page, pdf_file_path)
        self.convert_text_to_audio(new_text)
        pygame.mixer.music.load(sound_file_path)
        self.set_screen_text(new_text)
        
        self.audio_slider.set(0)
        self.audio_slider.configure(to=self.get_audio_length())
        self.page_input.delete(0, tk.END)
        self.page_input.insert(0, f"{current_page}")

        pygame.mixer.music.play(loops=0, start=0)
        self.button_play_pause.config(text="Pause")


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFPlayer(root)
    root.mainloop()