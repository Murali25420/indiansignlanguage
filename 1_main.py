
import subprocess
import numpy as np
import cv2
import os
import PIL
from PIL import ImageTk
import PIL.Image
from PIL import Image
import speech_recognition as sr
import pyttsx3
from itertools import count
import string
from tkinter import *
import time
import tkinter as tk
from tkinter import ttk
import numpy as np
image_x, image_y = 64,64
#from keras.models import load_model
from tensorflow.keras.models import load_model
import speech_recognition as sr

classifier = load_model('model.h5')


def give_char():
       import numpy as np
       from keras.preprocessing import image
       test_image = image.load_img('tmp1.png', target_size=(64, 64))
       test_image = image.img_to_array(test_image)
       test_image = np.expand_dims(test_image, axis = 0)
       result = classifier.predict(test_image)
       print(result)
       chars="ABCDEFGHIJKMNOPQRSTUVWXYZ"
       indx=  np.argmax(result[0])
       print(indx)
       return(chars[indx])

def check_sim(i,file_map):
       for item in file_map:
              for word in file_map[item]:
                     if(i==word):
                            return 1,item
       return -1,""

op_dest="filtered_data/"
alpha_dest="alphabet/"
dirListing = os.listdir(op_dest)
editFiles = []
for item in dirListing:
       if ".webp" in item:
              editFiles.append(item)

file_map={}
for i in editFiles:
       tmp=i.replace(".webp","")
       #print(tmp)
       tmp=tmp.split()
       file_map[i]=tmp

def func(a):
       all_frames=[]
       final= PIL.Image.new('RGB', (380, 260))
       words=a.split()
       for i in words:
              flag,sim=check_sim(i,file_map)
              if(flag==-1):
                     for j in i:
                            print(j)
                            im = PIL.Image.open(alpha_dest+str(j).lower()+"_small.gif")
                            frameCnt = im.n_frames
                            for frame_cnt in range(frameCnt):
                                   im.seek(frame_cnt)
                                   im.save("tmp.png")
                                   img = cv2.imread("tmp.png")
                                   img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                   img = cv2.resize(img, (380,260))
                                   im_arr = PIL.Image.fromarray(img)
                                   for itr in range(15):
                                          all_frames.append(im_arr)
              else:
                     print(sim)
                     im = PIL.Image.open(op_dest+sim)
                     im.info.pop('background', None)
                     im.save('tmp.gif', 'gif', save_all=True)
                     im = PIL.Image.open("tmp.gif")
                     frameCnt = im.n_frames
                     for frame_cnt in range(frameCnt):
                            im.seek(frame_cnt)
                            im.save("tmp.png")
                            img = cv2.imread("tmp.png")
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            img = cv2.resize(img, (380,260))
                            im_arr = PIL.Image.fromarray(img)
                            all_frames.append(im_arr)
       final.save("out.gif", save_all=True, append_images=all_frames, duration=100, loop=0)
       return all_frames      

img_counter = 0
img_text=''
class Tk_Manage(tk.Tk):
       def __init__(self, *args, **kwargs):     
              tk.Tk.__init__(self, *args, **kwargs)
              container = tk.Frame(self)
              container.pack(side="top", fill="both", expand = True)
              container.grid_rowconfigure(0, weight=1)
              container.grid_columnconfigure(0, weight=1)
              self.frames = {}
              for F in (StartPage, VtoS):
                     frame = F(container, self)
                     self.frames[F] = frame
                     frame.grid(row=0, column=0, sticky="nsew")
              self.show_frame(StartPage)

       def show_frame(self, cont):
              frame = self.frames[cont]
              frame.tkraise()

      

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Setting a dark futuristic background color
        self.config(bg='#2C2F33')  # Dark charcoal gray

        # Title label with lighter text for contrast
        label = tk.Label(self, text="Sign Sense", font=("Helvetica", 24, "bold"), bg='#2C2F33', fg='#FFFFFF')
        label.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky="ew")

        # Button styles
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 16, 'bold'), foreground='grey')

        # Define a set of vibrant, futuristic colors for each button
        button_colors = {
            "Sign Translation": "#4CAF50",  # Green
            "Voice to Sign": "#2196F3",     # Blue
        
        }

        # Create button styles with specified colors
        for text, color in button_colors.items():
            style.configure(f'{text}.TButton', background=color)

        # Sign Translation Button
        btn_sign_translation = ttk.Button(self, text="Sign Translation", style='Sign Translation.TButton', width=20,command=self.Sign_Translator)
        btn_sign_translation.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Voice to Sign Button
        btn_voice_to_sign = ttk.Button(self, text="Text to Sign", style='Voice to Sign.TButton', width=20, command=lambda: controller.show_frame(VtoS))
        btn_voice_to_sign.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

     

        # Proper alignment
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Set uniform padding
        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=10, sticky="nsew")

 
    def Sign_Translator(self):
          subprocess.Popen(['python','Sign_Translator.py'])






class VtoS(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#e3f2fd")  # Set background color to a light blue shade

        # Header
        header_label = tk.Label(self, text="Sign Transcriber", font=("Helvetica", 24, "bold"), fg="#333", bg="#e3f2fd")  # Set text and background color
        header_label.pack(pady=(20, 30))

        # Input Section
        input_frame = tk.Frame(self, bg="#e3f2fd")  # Set background color
        input_frame.pack(pady=20)

        text_label = tk.Label(input_frame, text="Enter Text :", font=("Helvetica", 14), bg="#e3f2fd")  # Set background color
        text_label.grid(row=0, column=0, padx=10)

        # Modern and elegant text field
        self.inputtxt = tk.Text(input_frame, height=1, width=30, font=("Helvetica", 12), bg="#fff", fg="#333", relief="solid", borderwidth=1, padx=5, pady=5)  # Set background and text color
        self.inputtxt.grid(row=0, column=1, padx=5)

        # Convert Button
        convert_button = tk.Button(self, text="Convert", font=("Helvetica", 14, "bold"), bg="#007bff", fg="#fff", command=self.take_input)  # Set background and text color
        convert_button.pack(pady=20)

        speech_button = tk.Button(self, text="Use Voice", font=("Helvetica", 14, "bold"), bg="#28a745", fg="#fff", command=self.speech_to_text)
        speech_button.pack(pady=10)

        # GIF Display
        self.gif_box = tk.Label(self, bg="#fff")  # Set background color
        self.gif_box.pack(pady=20)

        # Back to Home Button
        back_button = tk.Button(self, text="Back to Home", font=("Helvetica", 12), bg="#dc3545", fg="#fff", command=lambda: controller.show_frame(StartPage))  # Set background and text color
        back_button.pack(pady=20)

        # Variables
        self.gif_frames = []
        self.cnt = 0
    
    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.inputtxt.delete("1.0", "end")
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                self.inputtxt.insert("1.0", text)
            except sr.UnknownValueError:
                self.inputtxt.insert("1.0", "Could not understand audio")

    def gif_stream(self):
        if self.cnt == len(self.gif_frames):
            return
        img = self.gif_frames[self.cnt]
        self.cnt += 1
        imgtk = ImageTk.PhotoImage(image=img)
        self.gif_box.imgtk = imgtk
        self.gif_box.configure(image=imgtk)
        self.gif_box.after(50, self.gif_stream)

    def take_input(self):
        input_text = self.inputtxt.get("1.0", "end-1c")
        print("Input Text:", input_text)

        # Assuming func is defined elsewhere
        self.gif_frames = func(input_text)
        self.cnt = 0
        self.gif_stream()

app = Tk_Manage()
app.geometry("800x750")
app.mainloop()