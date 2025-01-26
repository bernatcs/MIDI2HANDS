# MIDI2HANDS

![Logo](MIDI2HANDS.png)

**MIDI2HANDS** is a Python application that uses machine learning to separate left and right hand notes in MIDI files. With custom models, you can process your own MIDI files to isolate the right and left hand parts of a performance.

---

## Features

- **Hand Separation**: Automatically separates left and right hand notes in MIDI files.
- **Custom Models**: Try out custom models with your own MIDI files to see the results.
- **Simple Interface**: User-friendly GUI built with Tkinter.
- **Background Processing**: Runs in the background, so you can continue using the app without interruption.

---

## Installation

To get started with **MIDI2HANDS**, you need Python installed on your machine.

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/MIDI2HANDS.git
cd MIDI2HANDS
```

### Step 2: Install Dependencies


Before you run the application, install the required dependencies using pip:

```
pip install -r requirements.txt
```

This will install all the necessary libraries for the app to function.


### Step 3: Run the Application

Once dependencies are installed, you can start the app with:

```
python midi2hands.py
```

This will open the graphical user interface (GUI), where you can load your MIDI files and begin processing them.

## How It Works

### 1. Load a MIDI File

Click the "Load MIDI File" button and select a MIDI file you want to process. The file will be loaded into the application.

### 2. Processing the MIDI File

Once a MIDI file is loaded, the app will automatically analyze the file and begin separating the left and right hand notes. The separation is done using a pre-trained machine learning model. 

### 3. Open the Processed File

After the processing is completed, you can open the .midi file. You will find channel 0 for right hand and channel 1 for left hand.

## How to Train a Custom Model

Go to this link a follow the instructions: [Google Colab](https://colab.research.google.com/drive/1fwKNPdfAtdn9GAy4U58LrE_mK9aaYFe8?usp=sharing)
