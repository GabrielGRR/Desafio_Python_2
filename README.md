# PDF_Player

## Overview

PDF_Player is a Python application that provides a user-friendly interface to read PDF files, convert them to audio, and play the audio. It utilizes Tkinter for the graphical user interface, pygame for audio playback, and pypdf for PDF parsing.

This tool is designed to assist users in listening to their PDF documents and navigating pages seamlessly through an intuitive GUI.

## ⚙ Starting the project

1. **Copy the files from this repository to your machine**: `git clone https://github.com/GabrielGRR/Desafio_Python_2.git`
2. **Navigate into the folder**: `cd Desafio_Python_2`
3. **Create your virtual environment**: `python -m venv venv`
4. **Activate your virtual environment**: `venv/Scripts/Activate`
5. **Install the required dependencies**: `pip install -r docs/requirements.txt`
6. **Run the program**: `python main.py`

## File Structure
```
PDFPlayer/
├── app.py          # Main application file
├── results/
│   └── sound/             # Directory for generated audio files 
│       └── current.wav    # Current page audio file 
│       └── pdf.wav        # Default audio file
├── docs/
│   └── images/            # Icons and additional resources
│       └── OrangePD_icon2.ico
└── requirements.txt       # List of dependencies
```

## Known Issues
[ ] Thread Safety: Some threading issues might occur with slider updates.
[ ] Audio garbage: The best practice is to create the .wav audio file in the OS temp folder.
[ ] GUI Responsiveness: Limited testing on different screen sizes.