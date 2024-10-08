from pypdf import PdfReader
import pyttsx3
from gtts import gTTS

reader = PdfReader("O Programador Pragmatico.pdf") # Caminho relativo
number_of_pages = len(reader.pages) # não obrigatório
n = 8
page = reader.pages[n] # seleciona a página que você quer que seja transcrito
text = page.extract_text()

# if n+1 <= number_of_pages:
#     buffer = reader.pages[n+1] # seleciona a página que você quer que seja transcrito
# else:
#     page = reader.pages[n] # seleciona a página que você quer que seja transcrito
#     text = page.extract_text()

print(text)

tts = pyttsx3.init()
tts.save_to_file(text, 'audio.mp3')
#tts.say(text)
tts.runAndWait()

# tts = gTTS(text, lang='pt')
# tts.save('audio2.mp3')
