from pypdf import PdfReader
import pyttsx3
import pygame
import os
class PDFPlayer:
    def __init__(self, pygame_instance):
        self.sound_current = 'results/sound/current.wav'
        pygame.mixer.init()
        self.pygame_instance = pygame_instance
        self.pygame_instance.mixer.music.load(os.path.join("results/sound", "pdf.wav"))

    def pdf_conversion(self, num_page: int, filename: str):
        try:
            reader = PdfReader(filename)
            number_of_pages = len(reader.pages)
            page = reader.pages[num_page-1]
            text = page.extract_text()
        except:
            text = "Selecione um arquivo PDF"
            number_of_pages = 1
        tts = pyttsx3.init()
        tts.save_to_file(text, 'results/sound/current.wav')
        tts.runAndWait()
        print(text)
        return text, number_of_pages

    def load_music(self, sound_file):
        pygame.mixer.music.load(sound_file)

    def unload_music(self):
        pygame.mixer.music.unload()

    def play_music(self, start=0):
        pygame.mixer.music.play(loops=0, start=start)

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def unpause_music(self):
        pygame.mixer.music.unpause()

    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def audio_lenght(self):
        audio_file_lenght = pygame.mixer.Sound(self.sound_current).get_length()
        print(audio_file_lenght)
        return audio_file_lenght