from pypdf import PdfReader
import pyttsx3

reader = PdfReader("desafio_python_2/O Programador Pragmatico.pdf") #Caminho relativo
number_of_pages = len(reader.pages) # não obrigatório
page = reader.pages[8] # seleciona a página que você quer que seja transcrito
text = page.extract_text()

print(text)

tts = pyttsx3.init()
tts.save_to_file(text, 'desafio_python_2/audio.mp3')
tts.runAndWait()
#tts.say(text)

# engine.save_to_file('Hello World' , 'test.mp3')
# engine.runAndWait()