import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import subprocess
import threading
import os
import sys
import traceback
import mido
import numpy as np
from tensorflow.keras.models import load_model

class MidiProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MIDI2HANDS")
        self.root.geometry("600x500")
        self.root.config(bg="#333333")

        # Variables
        self.input_midi = ""
        self.output_path = ""
        self.model_path = ""
        self.model = None

        # Crear widgets
        self.create_widgets()

    def create_widgets(self):
        # Título y subtítulo
        self.title_label = tk.Label(self.root, text="MIDI2HANDS", font=("Arial", 28, "bold"), bg="#333333", fg="#FFA500")
        self.title_label.pack(pady=20)

        self.subtitle_label = tk.Label(self.root, text="by Bernat Cucarella (www.bernatcucarella.com)", font=("Arial", 14, "italic"), bg="#333333", fg="#A1A1A1")
        self.subtitle_label.pack(pady=5)

        # Frame para organizar los widgets
        frame = tk.Frame(self.root, bg="#333333")
        frame.pack(pady=30)

        # Input MIDI File
        self.input_midi_label = tk.Label(frame, text="Selecciona el archivo MIDI de entrada:", font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.input_midi_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.input_midi_button = self.create_button(frame, "Seleccionar archivo MIDI", self.select_midi_file)
        self.input_midi_button.grid(row=0, column=1, padx=10, pady=10)

        # Output File
        self.output_label = tk.Label(frame, text="Selecciona el archivo de salida:", font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.output_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.output_button = self.create_button(frame, "Seleccionar archivo de salida", self.select_output_file)
        self.output_button.grid(row=1, column=1, padx=10, pady=10)

        # Model Selection
        self.model_label = tk.Label(frame, text="Selecciona el modelo:", font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.model_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.model_button = self.create_button(frame, "Seleccionar modelo", self.select_model_file)
        self.model_button.grid(row=2, column=1, padx=10, pady=10)

        # Start Process Button
        self.start_button = self.create_button(self.root, "Iniciar proceso", self.start_process, width=20, font_size=14)
        self.start_button.pack(pady=20)

        # Progress bar
        self.progress_bar = Progressbar(self.root, length=300, mode='indeterminate')
        self.progress_bar.pack(pady=10)
        self.progress_bar.stop()

        # Loading label
        self.loading_label = tk.Label(self.root, text="Procesando...", font=("Arial", 12, "italic"), bg="#333333", fg="#FFFFFF")
        self.loading_label.pack(pady=10)
        self.loading_label.pack_forget()

        # Exported file label
        self.exported_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#333333", fg="#FFFFFF")
        self.exported_label.pack(pady=10)

    def create_button(self, parent, text, command, width=20, font_size=12):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            font=("Arial", font_size),
            bg="#4CAF50",
            fg="black",
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=5
        )
        button.bind("<Enter>", lambda e: button.config(bg="#45A049"))
        button.bind("<Leave>", lambda e: button.config(bg="#4CAF50"))
        return button

    def select_midi_file(self):
        self.input_midi = filedialog.askopenfilename(filetypes=[("MIDI Files", "*.mid")])
        if self.input_midi:
            if not self.input_midi.lower().endswith(".mid"):
                messagebox.showerror("Error", "El archivo seleccionado no es un archivo MIDI válido.")
                return
            midi_name = os.path.basename(self.input_midi)
            self.input_midi_button.config(text=midi_name)

    def select_output_file(self):
        self.output_path = filedialog.asksaveasfilename(defaultextension=".mid", filetypes=[("MIDI Files", "*.mid")])
        if self.output_path:
            output_name = os.path.basename(self.output_path)
            self.output_button.config(text=output_name)

    def select_model_file(self):
        self.model_path = filedialog.askopenfilename(filetypes=[("Keras Model Files", "*.keras *.h5")])
        if self.model_path:
            model_name = os.path.basename(self.model_path)
            self.model_button.config(text=model_name)
            self.model = self.load_user_model(self.model_path)

    def start_process(self):
        if not self.input_midi or not self.output_path or not self.model:
            messagebox.showerror("Error", "Por favor, selecciona todos los archivos necesarios.")
            return

        # Check if process is already running
        if hasattr(self, 'process_running') and self.process_running:
            messagebox.showwarning("Proceso en curso", "Ya hay un proceso en ejecución.")
            return

        # Disable start button to prevent multiple clicks
        self.start_button.config(state=tk.DISABLED)
        self.process_running = True

        # Reset labels
        self.exported_label.config(text="")
        self.loading_label.pack_forget()

        # Start progress bar
        self.progress_bar.start()
        self.loading_label.pack()

        # Start processing in a separate thread
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        try:
            self.separate_hands(self.input_midi, self.output_path, self.model)
            self.root.after(0, self.show_success_message, self.output_path)
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}\n{traceback.format_exc()}"
            self.root.after(0, self.show_error_message, error_msg)
        finally:
            self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
            self.process_running = False

    def show_success_message(self, output_path):
        self.progress_bar.stop()
        self.loading_label.pack_forget()
        self.exported_label.config(text=f"Archivo exportado a: {output_path}", fg="green")
        self.exported_label.pack()

    def show_error_message(self, message):
        self.progress_bar.stop()
        self.loading_label.pack_forget()
        self.exported_label.config(text=message, fg="red")
        self.exported_label.pack()
        messagebox.showerror("Error", message)

    def load_user_model(self, model_path):
        try:
            model = load_model(model_path)
            print(f"Modelo cargado exitosamente desde: {model_path}")
            return model
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
            print(traceback.format_exc())
            sys.exit(1)

    def load_midi(self, midi_file):
        try:
            return mido.MidiFile(midi_file)
        except Exception as e:
            print(f"Error al cargar el archivo MIDI: {e}")
            print(traceback.format_exc())
            return None

    def predict_hand(self, note_features, model):
        try:
            note_features = np.reshape(note_features, (1, 1, note_features.shape[0]))  # Reshape para 3 dimensiones
            prediction = model.predict(note_features)
            return prediction[0][0]  # Retorna la predicción como un valor continuo
        except Exception as e:
            print(f"Error en predicción de mano: {e}")
            print(traceback.format_exc())
            sys.exit(1)

    def separate_hands(self, input_midi, output_midi, model):
        try:
            midi_data = self.load_midi(input_midi)
            if midi_data is None:
                sys.exit(1)

            new_tracks = []
            right_hand_notes = 0
            left_hand_notes = 0

            active_notes = {"right": set(), "left": set()}

            for track in midi_data.tracks:
                new_track = mido.MidiTrack()
                new_tracks.append(new_track)

                for msg in track:
                    if not msg.is_meta:
                        if msg.type == 'note_on' and msg.velocity > 0:
                            note_features = np.array([msg.time, msg.note, msg.velocity])
                            prediction = self.predict_hand(note_features, model)

                            if prediction < 0.5:
                                msg.channel = 0
                                right_hand_notes += 1
                                active_notes["right"].add(msg.note)
                            else:
                                msg.channel = 1
                                left_hand_notes += 1
                                active_notes["left"].add(msg.note)

                        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                            if msg.note in active_notes["right"]:
                                msg.channel = 0
                                active_notes["right"].remove(msg.note)
                            elif msg.note in active_notes["left"]:
                                msg.channel = 1
                                active_notes["left"].remove(msg.note)

                    new_track.append(msg)

            new_midi = mido.MidiFile()
            for track in new_tracks:
                new_midi.tracks.append(track)

            new_midi.save(output_midi)
            print(f"Archivo MIDI procesado guardado como: {output_midi}")
            print(f"Total notas mano derecha: {right_hand_notes}")
            print(f"Total notas mano izquierda: {left_hand_notes}")
        except Exception as e:
            print(f"Error en el procesamiento del MIDI: {e}")
            print(traceback.format_exc())
            sys.exit(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = MidiProcessingApp(root)
    root.mainloop()