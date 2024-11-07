import tkinter as tk
from tkinter import filedialog

class PDFPlayerGUI:
    def __init__(self, root, player):
        self.player = player
        self.palavras_linha = 13
        self.filename = ""
        self.current_page = 1
        self.number_of_pages = 1
        self.is_dragging_slider = False

        self.root = root
        self.root.title("mPD player | PD_f player")
        self.root.geometry("")  # fit to content
        self.root.minsize(400, 400)
        self.root.maxsize(700, 700)
        self.root.iconbitmap(default='docs/images/OrangePD_icon2.ico')

        self.page_text, self.number_of_pages = self.player.pdf_conversion(self.current_page, self.filename)

        # Crie um Frame para encapsular o Text
        self.text_frame = tk.Frame(self.root, width=600, height=400)
        self.text_frame.pack_propagate(False)  # Impede que o Frame redimensione para caber no conteúdo
        self.text_frame.pack(side=tk.TOP, padx=10, pady=10, expand=True, fill="both")

        # Crie o Text dentro do Frame com barras de rolagem
        self.text_scrollbar = tk.Scrollbar(self.text_frame)
        self.text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_label = tk.Text(self.text_frame, font=("Arial", 10), relief="sunken", wrap=tk.WORD, yscrollcommand=self.text_scrollbar.set)
        self.text_label.pack(expand=True, fill="both")

        self.text_scrollbar.config(command=self.text_label.yview)

        # Adicione uma tag para centralizar o texto
        self.text_label.tag_configure("center", justify='center')

        self.update_text_label(self.page_text, self.palavras_linha)

        self.audio_slider = tk.Scale(self.root, from_=0, to=self.player.audio_lenght(), orient='horizontal', length=500, sliderlength=20, showvalue=0)
        self.audio_slider.pack(pady=5)
        self.audio_slider.bind("<ButtonPress-1>", self.slider_click)
        self.audio_slider.bind("<ButtonRelease-1>", self.slider_release)

        lower_frame = tk.Frame(self.root)
        lower_frame.pack(side=tk.LEFT, expand=True, fill="x", pady=(0, 10))

        self.page_input = tk.Entry(lower_frame, width=4)
        self.page_input.pack(side=tk.LEFT, anchor="w", padx=(10, 0))
        self.page_input.bind("<Return>", self.process_input)
        self.page_input.insert(0, f"{self.current_page}")

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
        self.text_label.config(state=tk.NORMAL)
        self.text_label.delete("1.0", tk.END)
        self.text_label.insert(tk.END, text_content)
        self.text_label.tag_add("center", "1.0", "end")
        self.text_label.config(state=tk.DISABLED)

    def process_input(self, event=None):
        new_page = int(self.page_input.get())
        if 1 <= new_page <= self.number_of_pages:
            self.new_page_conversion(new_page, 'results/sound/current.wav', self.filename)
            self.current_page = new_page
        else:
            print("Invalid page number")

    def new_page_conversion(self, current_page, sound_current, filename):
        self.player.unload_music()
        new_text, _ = self.player.pdf_conversion(current_page, filename)
        self.player.load_music(sound_current)
        self.update_text_label(new_text, self.palavras_linha)
        self.audio_slider.set(0)
        self.player.play_music()
        self.btn_play_pause.config(text="Pause")
        self.page_input.delete(0, tk.END)
        self.page_input.insert(0, f"{current_page}")
        self.audio_slider.configure(to=self.player.audio_lenght())

    def slider_click(self, event=None):
        self.is_dragging_slider = True
        self.player.stop_music()

    def slider_release(self, event=None):
        if self.is_dragging_slider:
            self.player.play_music(start=self.paused_pos())
            self.is_dragging_slider = False

    def paused_pos(self):
        current_pos = self.audio_slider.get()
        return current_pos

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

    def play_pause(self):
        try:
            if not self.music_loaded:
                self.player.play_music(start=0)
                self.btn_play_pause.config(text="Pause")
                self.music_loaded = True
            elif not self.player.is_playing():
                self.audio_slider.set(self.paused_pos())
                self.player.unpause_music()
                self.btn_play_pause.config(text="Pause")
            else:
                self.player.pause_music()
                self.btn_play_pause.config(text="Play")
        except Exception as e:
            print(f"play music failed: {e}")

    def browse_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("PDF files", "*.pdf*"), ("all files", "*.*")))

        if filename != "":
            self.current_page = 1
            self.new_page_conversion(self.current_page, 'results/sound/current.wav', filename)
            self.page_label.config(text=f"/{self.number_of_pages}")
            self.filename = filename