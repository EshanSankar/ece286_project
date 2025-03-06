# TODO:
# -centering the buttons and text properly
# -adding a tutorial gif
# -building the annotation infrastructure

import tkinter as tk
from PIL import Image

class annotator:
    def __init__(self, master):
        self.master = master
        self.master.attributes('-fullscreen', True)
        self.HEADER_FONT = "Arial 32 bold"
        self.BODY_FONT = "Arial 14"
        self.home()
    
    def home(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame_home = tk.Frame(self.master, width=1920, height=1080)
        self.frame_home.columnconfigure(0, weight=1)
        self.frame_home.rowconfigure([0, 1, 2, 3], minsize=300)
        self.frame_home.pack(expand=True, fill="both")
        self.text_home = tk.Label(self.frame_home, text="Welcome to the data annotator!", font=self.HEADER_FONT)
        self.text_home.grid(row=0,column=0)
        self.text_body = tk.Label(self.frame_home,
                                  text="Thank you for participating in our experiment! \n Here, you will perform bounding-box data annotation on images of stop signs. \n When you click \'Continue\', you will be given a brief tutorial.",
                                  font=self.BODY_FONT)
        self.text_body.grid(row=1, column=0, sticky="n")
        self.button_begin = tk.Button(self.frame_home, text="Continue", width=25, height=5, command=self.guide)
        self.button_begin.grid(row=2, column=0)
    
    def guide(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame_guide = tk.Frame(self.master, width=1920, height=1080)
        self.frame_guide.columnconfigure(0, minsize=350)
        self.frame_guide.rowconfigure([0, 1, 2, 3], minsize=200)
        self.frame_guide.pack(expand=True, fill="both")
        self.text1_guide = tk.Label(self.frame_guide,
                                   text="A bounding box is a box drawn around an object of interest in an image, that contains the object as precisely as possible. \n You must draw precise bounding boxes that encapsulate only the stop signs, as perfectly as possible. \n Some images will have slanted or off-centered stop signs which cannot be perfectly bound, but a few pixels worth of leeway is okay. Just try to be as precise as you can.",
                                   font=self.BODY_FONT)
        self.text1_guide.grid(row=0, column=0, sticky="s")
        self.text2_guide = tk.Label(self.frame_guide,
                                   text="For each image, you will be given a small default box, the corners of which you can freely drag such that the box captures the stop sign. \n Here is an example of a good bounding box being drawn:",
                                   font=self.BODY_FONT)
        self.text2_guide.grid(row=1, column=0, sticky="s")
        # gif configuration -- NEED TO ADD ANNOTATION GIF
        # file = "annotation.gif" # NEED TO ADD THIS
        # gif = Image.open(file)
        # self.frames = gif.n_frames
        # self.photoimage_objects = []
        # for i in range(self.frames):
        #     obj = tk.PhotoImage(file = file, format = f"gif -index {i}")
        #     self.photoimage_objects.append(obj)
        # self.gif_guide = tk.Label(self.frame_guide)
        # self.gif_guide.grid(row=2, column=0)
        # self.current_frame = 0
        # self.animation()
        # end gif configuration
        self.button_trial = tk.Button(self.frame_guide, text="Do an Example Annotation", width=25, height=5, command=self.trial)
        self.button_trial.grid(row=3, column=0)

    def trial(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame_trial = tk.Frame(self.master, width=1920, height=1080)
        self.frame_trial.columnconfigure(0, minsize=350)
        self.frame_trial.rowconfigure([0, 1, 2], minsize=200)
        self.frame_trial.pack(expand=True, fill="both")
        self.button_begin = tk.Button(self.frame_trial, text="Continue", width=25, height=5, command=self.begin_screen)
        self.button_begin.grid(row=0, column=0)

    def begin_screen(self):
        for i in self.master.winfo_children():
            i.destroy()
        self.frame_begin_screen = tk.Frame(self.master, width=1920, height=1080)
        self.frame_begin_screen.columnconfigure(0, minsize=350)
        self.frame_begin_screen.rowconfigure([0, 1, 2], minsize=200)
        self.frame_begin_screen.pack(expand=True, fill="both")
        self.text_begin = tk.Label(self.frame_begin_screen,
                                   text="You are about to begin the actual data annotation experiment. \n \'Begin Experiment\' will start a timer and take you to the images.",
                                   font=self.HEADER_FONT)
        self.text_begin.grid(row=0, column=0, sticky="s")
        self.button_begin_experiment = tk.Button(self.frame_begin_screen, text="Begin Experiment", width=25, height=5, command=self.begin_experiment)
        self.button_begin_experiment.grid(row=1, column=0, sticky="n")
        self.button_back = tk.Button(self.frame_begin_screen, text="Back", width=25, height=5, command=self.guide)
        self.button_back.grid(row=2, column=0, sticky="n")

    def begin_experiment(self):
        root.destroy()
    
    #def animation(self): # for gif
    #    if self.frames:
    #        self.gif_guide.config(image=self.photoimage_objects[self.current_frame])
    #        self.current_frame = self.current_frame + 1 if self.current_frame != self.frames else 0
    #        self.frame_guide.after(50, self.animation)

root = tk.Tk()
annotator(root)
root.mainloop()