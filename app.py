from pypdf import PdfReader
import pyttsx3
import tkinter as tk
from tkinter import filedialog
import pygame
import os
import time
import threading

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
        self.filename = ""
        self.current_page = 1
        self.number_of_pages = 1
        self.is_dragging_slider = False
        self.music_loaded = False
        self.sound_current = 'results/sound/current.wav'                
        self.page_text, self.number_of_pages = self.pdf_conversion(self.current_page, self.filename)

        # Por conveção do tkinter, a janela principal é chamada de janela raiz, portanto, root
        self.root = root

        # Inicializadores/construtores do player de áudio e interface gráfica do usuário(GUI) 
        self._InitMixer()
        self._InitGUI()

        # TODO: estudar paralelismo e concorrencia
        threading.Thread(target=self.position_updater, daemon=True).start()

    # Funções de uso interno
    def _InitMixer(self):
        """Inicializa o mixer pygame e carrega um arquivo de música."""

        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join("results/sound", "pdf.wav"))

    def _InitGUI(self):
        """
        Inicializa a interface gráfica do usuário (GUI) para a aplicação.

        Este método configura a janela principal, frames, áreas de texto, barras de rolagem, sliders,
        e botões usados na aplicação. Também configura as propriedades da janela e widgets necessários.

        Widgets criados:
        - Janela principal com título, geometria, tamanho mínimo, tamanho máximo e ícone.
        - Frame para encapsular o widget Text.
        - Widget Text com barra de rolagem para exibir texto.
        - Slider de áudio para controlar a reprodução de áudio.
        - Widget Entry para entrada de página.
        - Widget Label para exibir o número total de páginas.
        - Botões para navegar no áudio (Anterior, Reproduzir/Pausar, Próximo) e selecionar um arquivo PDF.
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
        self.text_frame.pack(side=tk.TOP, padx=10, pady=10, expand=True, fill="both")

        # Barras de rolagem para textos longos
        self.text_scrollbar = tk.Scrollbar(self.text_frame)
        self.text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Parâmetros do texto
        self.text_label = tk.Text(self.text_frame, font=("Arial", 10), relief="sunken", wrap=tk.WORD, yscrollcommand=self.text_scrollbar.set)
        self.text_label.pack(expand=True, fill="both")
        self.text_scrollbar.config(command=self.text_label.yview)
        self.text_label.tag_configure("center", justify='center')
        self.update_text_label(self.page_text)

        # Parâmetros do 'slider' de áudio
        self.audio_slider = tk.Scale(self.root, from_=0, to=self.get_audio_lenght(), orient='horizontal', length=500, sliderlength=20, showvalue=0)
        self.audio_slider.pack(pady=5)
        self.audio_slider.bind("<ButtonPress-1>", self.slider_click)
        self.audio_slider.bind("<ButtonRelease-1>", self.slider_release)

        # Frame para encapsular input da página
        lower_frame = tk.Frame(self.root)
        lower_frame.pack(side=tk.LEFT, expand=True, fill="x", pady=(0, 10))

        # Caixa de input de página
        self.page_input = tk.Entry(lower_frame, width=4)
        self.page_input.pack(side=tk.LEFT, anchor="w", padx=(10, 0))
        self.page_input.bind("<Return>", self.page_user_input)
        self.page_input.insert(0, f"{self.current_page}")

        # Complemento da caixa de input de pagina, mostrando o total de páginas daquele PDF
        self.page_label = tk.Label(lower_frame, text=f"/{self.number_of_pages}", font=("Arial", 10))
        self.page_label.pack(side=tk.LEFT, anchor="w")

        # Frame para encapsular os botões, está dentro da frame anterior (lower_frame)
        button_frame = tk.Frame(lower_frame)
        button_frame.pack(side=tk.LEFT, anchor="center", expand=True)

        # Botão de voltar página
        btn_prev = tk.Button(button_frame, text="Prev", command=self.prev_sound)
        btn_prev.pack(side=tk.LEFT, padx=3)

        # Botão de toggle de pausar e tocar áudio
        self.btn_play_pause = tk.Button(button_frame, text="Play", command=self.play_pause)
        self.btn_play_pause.pack(side=tk.LEFT, padx=3)

        # Botão de avançar página
        btn_next = tk.Button(button_frame, text="Next", command=self.next_sound)
        btn_next.pack(side=tk.LEFT, padx=3)

        # Botão de selecionar arquivo PDF
        select_file = tk.Button(lower_frame, text="Select PDF", command=self.browse_file)
        select_file.pack(side=tk.BOTTOM, anchor="e", padx=10)


    # Métodos 'getter'
    def get_is_playing(self):
        return pygame.mixer.music.get_busy()

    def get_paused_pos(self):
        return self.audio_slider.get()

    def get_audio_lenght(self):
        return pygame.mixer.Sound(self.sound_current).get_length()
    
    def thread_check(self):
        """Checa se as threads foram corretamente inicializados."""

        threads_ativas = threading.enumerate()
        print(f"Total de threads ativas: {len(threads_ativas)}")
        print("Lista de threads:")
        for thread in threads_ativas:
            print(f"- {thread.name} (daemon: {thread.daemon})")


    # Métodos 'Setter'
    def pdf_conversion(self, num_page: int, filename: str):
        """
        Converte uma página especificada de um arquivo PDF para texto e salva como um arquivo de áudio.
            num_page (int): O número da página a ser convertida.
            filename (str): O caminho para o arquivo PDF.
            Try-Exception: Se houver um erro ao ler o arquivo PDF ou se a pessoa sair da caixa de diálogo 
            browse_file ao buscar um PDF.
        
        Args:
            num_page (int): A página do PDF a ser convertida.
            filename (str): O caminho do arquivo PDF.

        Returns:
            tupla: Uma tupla contendo o texto extraído(str) e o número total de páginas (int).
        """

        try:
            reader = PdfReader(filename)
            self.number_of_pages = len(reader.pages)
            page = reader.pages[num_page-1]
            text = page.extract_text()
        except:
            text = "Selecione um arquivo PDF"
            self.number_of_pages = 1
        tts = pyttsx3.init()
        tts.save_to_file(text, 'results/sound/current.wav')
        tts.runAndWait()
        return text, self.number_of_pages

    def position_updater(self, val=None):
        """Atualiza continuamente a posição do slider de áudio."""
        
        while True:
            time.sleep(1)
            if self.get_is_playing() and not self.is_dragging_slider:
                pos = self.audio_slider.get() + 1
                self.audio_slider.set(pos)
                self.thread_check()

    def slider_click(self, event=None):
        self.is_dragging_slider = True
        pygame.mixer.music.stop()

    def slider_release(self, event=None):
        if self.is_dragging_slider:
            pygame.mixer.music.play(loops=0, start=self.get_paused_pos())
            pygame.mixer.music.set_pos(self.get_paused_pos())
            self.is_dragging_slider = False

    def play_pause(self):
        """
        Alterna entre play/pause do aúdio.

        É uma única função devido ao botão compartilhado da GUI (Graphic User Interface).
        """

        try:
            if not self.music_loaded:
                pygame.mixer.music.play(loops=0, start=0)
                self.btn_play_pause.config(text="Pause")
                self.music_loaded = True

            elif not self.get_is_playing():
                self.audio_slider.set(self.get_paused_pos())
                pygame.mixer.music.unpause()
                self.btn_play_pause.config(text="Pause")

            else:
                pygame.mixer.music.pause()
                self.btn_play_pause.config(text="Play")

        except Exception as e:
            print(f"play music failed: {e}")

    def prev_sound(self):
        """Navega para a página anterior."""
        
        try:
            if self.current_page != 1:
                self.current_page -= 1
                self.new_page_conversion(self.current_page, 'results/sound/current.wav', self.filename)
            else:
                print("current page is already 1")
        except:
            print("prev sound failed")

    def next_sound(self):
        """Navega para a próxima página."""
        
        try:
            if self.current_page != self.number_of_pages:
                self.current_page += 1
                self.new_page_conversion(self.current_page, 'results/sound/current.wav', self.filename)
            else:
                print("current page is already last")
        except:
            print("next sound failed")

    def update_text_label(self, new_text: list):
        """
        Atualiza a caixa de texto com o novo texto da página atual do PDF.
        
        Args:
            new_text (list): O novo texto a ser exibido no rótulo de texto.
        """
        
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
        self.text_label.config(state=tk.NORMAL)
        self.text_label.delete("1.0", tk.END)
        self.text_label.insert(tk.END, text_content)
        self.text_label.tag_add("center", "1.0", "end")
        self.text_label.config(state=tk.DISABLED)

    def page_user_input(self, event=None):
        """Atualiza a pagina atual para a que o usuário digitou."""

        try:
            new_page = int(self.page_input.get())
            if 1 <= new_page <= self.number_of_pages:
                self.new_page_conversion(new_page, 'results/sound/current.wav', self.filename)
                self.current_page = new_page
            else:
                print("Invalid page number")
        except ValueError:
            print("Invalid input")

    def new_page_conversion(self, current_page: int, sound_current: str, filename: str):
        """
        Faz a conversão de um arquivo PDF em texto e áudio e reprodução de uma nova página no PDF.

        Args:
            current_page (int): A página do PDF a ser convertida.
            sound_current (str): O caminho do arquivo de aúdio.
            filename (str): O caminho do arquivo PDF.
        """
        pygame.mixer.music.unload()
        new_text, _ = self.pdf_conversion(current_page, filename)
        pygame.mixer.music.load(sound_current)
        self.update_text_label(new_text)
        self.audio_slider.set(0)
        pygame.mixer.music.play(loops=0, start=0)
        self.btn_play_pause.config(text="Pause")
        self.page_input.delete(0, tk.END)
        self.page_input.insert(0, f"{current_page}")
        self.audio_slider.configure(to=self.get_audio_lenght())

    def browse_file(self):
        """Opens a file dialog for the user to select a PDF file."""

        filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("PDF files", "*.pdf*"), ("all files", "*.*")))

        if filename != "":
            self.current_page = 1
            self.new_page_conversion(self.current_page, 'results/sound/current.wav', filename)
            self.page_label.config(text=f"/{self.number_of_pages}")
            self.filename = filename

#TODO: Explicar o pq se usa __name__ == __main__
if __name__ == "__main__":
    # Criação da janela 'raiz' pela biblioteca tkinter
    root = tk.Tk()
    
    # Inicialização do nosso objeto PDFPlayer, onde o argumento da nossa classe, é o objeto criado anteriormente
    app = PDFPlayer(root)
    
    # Função nativa do tkinter que permite a GUI ler e executar funções baseadas em nossos inputs
    root.mainloop()

    # /\ equivalente a um while True:
    # while enquanto_a_janela_existir():
    #   aguardar_eventos_e_inputs()
    #   event.executar()
    #   event = lista_eventos.pop()
